import unittest
from models import Models, Model
from requests import Requests


class TestRequests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.models = Models()
        self.model = {
            "path": "/users/info",
            "method": "GET",
            "query_params": [
                {
                    "name": "with_extra_data",
                    "types": ["Boolean"],
                    "required": False
                },
                {
                    "name": "user_id",
                    "types": ["String", "UUID"],
                    "required": True
                }
            ],
            "headers": [
                {
                    "name": "Authorization",
                    "types": ["String", "Auth-Token"],
                    "required": True
                }
            ],
            "body": []
        }
        model = Model(**self.model)
        self.models.add_model(model)
        self.requests = Requests(self.models)

    def test_validate_required_fields_with_single_missing_required(self):
        request = {
            "path": "/users/info",
            "method": "GET",
            "query_params": [
                {
                    "name": "with_extra_data",
                    "value": False
                }
            ],
            "headers": [
                {
                    "name": "Authorization",
                    "value": "Bearer 56ee9b7a-da8e-45a1-aade-a57761b912c4"
                }
            ],
            "body": []
        }
        expected_result = [{'field_name': 'user_id', 'param_type': 'query_params', 'reason': 'missing required'}]
        result = self.requests._validate_required_fields(self.model, request, "query_params")
        assert result == expected_result

    def test_validate_fields_types_with_single_invalid_type(self):
        request = {
            "path": "/users/info",
            "method": "GET",
            "query_params": [
                {
                    "name": "with_extra_data",
                    "value": 123
                }
            ],
            "headers": [],
            "body": []
        }
        expected_result =\
            [{'field_name': 'with_extra_data', 'param_type': 'query_params', 'reason': "invalid types ['Boolean']"}]
        result = self.requests._validate_fields_types(self.model, request, "query_params")
        assert result == expected_result

    async def test_validate_request_with_invalid_type_and_missing_required(self):
        request = {
            "path": "/users/info",
            "method": "GET",
            "query_params": [
                {
                    "name": "with_extra_data",
                    "value": False
                }
            ],
            "headers": [
                {
                    "name": "Authorization",
                    "value": "Bearero 56ee9b7a-da8e-45a1-aade-a57761b912c4"
                }
            ],
            "body": []
        }
        result = await self.requests.validate_request(request)
        expected_result = {
            'status': 'invalid',
            'abnormal_fields':
                [{'field_name': 'user_id', 'param_type': 'query_params', 'reason': 'missing required'},
                 {'field_name': 'Authorization', 'param_type': 'headers', 'reason': "invalid types ['Auth-Token']"}]
        }
        assert result == expected_result
