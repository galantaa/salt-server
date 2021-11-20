from pydantic import BaseModel
from models import Models
from utils import Utils


class Request(BaseModel):
    path: str
    method: str
    query_params: list
    headers: list
    body: list


QUERY_PARAMS = 'query_params'
HEADERS = 'headers'
BODY = 'body'


class Requests:
    def __init__(self, models: Models):
        self._models = models
        self._utils = Utils()
        self._param_types = [QUERY_PARAMS, HEADERS, BODY]

    async def validate_request(self, request: dict):
        result = {}
        # TODO: add validations for no path / method
        matching_model = await self._get_matching_model(request)
        if not matching_model:
            result['status'] = 'valid'
            result['message'] = 'missing-model'
            return result
        abnormal_fields = self._get_abnormal_fields(matching_model, request)
        if len(abnormal_fields) == 0:
            result['status'] = 'valid'
        else:
            result['status'] = 'invalid'
            result['abnormal_fields'] = abnormal_fields
        return result

    def _get_abnormal_fields(self, matching_model, request):
        abnormal_fields = []
        for param_type in self._param_types:
            abnormal_fields.extend(self._validate_required_fields(matching_model, request, param_type))
            abnormal_fields.extend(self._validate_fields_types(matching_model, request, param_type))
        return abnormal_fields

    async def _get_matching_model(self, request):
        try:
            request_key = f"({request.get('path')}, {request.get('method')})"
            matching_model = self._models.get_model_by_key(request_key)
            return matching_model
        except Exception:
            print('error fetching model')
            return None

    def _validate_required_fields(self, model, request, param_type):
        try:
            missing_required_fields = []
            request_fields_names = [field.get('name') for field in request.get(param_type, [])]
            for model_field in model.get(param_type, []):
                if model_field.get('required') and model_field.get('name') not in request_fields_names:
                    missing_required_fields.append(model_field.get('name'))
            return self._build_missing_required_fields_dict(missing_required_fields, param_type)
        except Exception:
            print('error in _validate_required_fields')
            return []

    @staticmethod
    def _build_missing_required_fields_dict(missing_required_fields: list, param_type: str):
        return [{'field_name': field, 'param_type': param_type, 'reason': 'missing required'}
                for field in missing_required_fields]

    def _validate_fields_types(self, model, request, param_type):
        try:
            invalid_types_fields = []
            # TODO: add this when indexing a model!
            legal_types_dict = {field.get('name'): field.get('types') for field in model.get(param_type, [])}
            for request_field in request.get(param_type, []):
                field_legal_types = legal_types_dict.get(request_field.get('name'))
                invalid_types = self._utils.validate_type(request_field.get('value'), field_legal_types)
                if field_legal_types and len(invalid_types) > 0:
                    invalid_type_dict = \
                        self._build_invalid_types_fields_dict(request_field.get('name'), param_type, invalid_types)
                    invalid_types_fields.append(invalid_type_dict)
            # TODO: add validations for no headers body query
            return invalid_types_fields
        except Exception:
            print('error in _validate_fields_type')
            return []

    @staticmethod
    def _build_invalid_types_fields_dict(invalid_field: str, param_type: str, invalid_types: list):
        return {'field_name': invalid_field, 'param_type': param_type, 'reason': f'invalid types {invalid_types}'}
