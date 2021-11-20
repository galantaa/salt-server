from datetime import datetime
import re


class Utils:
    def __init__(self):
        self._primitive_types_map = {
            "Int": int,
            "String": str,
            "Boolean": bool,
            "List": list
        }
        self._special_types_validators_map = {
            "Date": self._validate_date,
            "Email": self._validate_email,
            "UUID": self._validate_uuid,
            "Auth-Token": self._validate_auth_token
        }

    def validate_type(self, field_value, legal_types: list) -> list:
        invalid_types = []
        for legal_type in legal_types:
            if legal_type in self._primitive_types_map.keys() and \
                    not isinstance(field_value, self._primitive_types_map.get(legal_type)):
                invalid_types.append(legal_type)
            elif legal_type in self._special_types_validators_map.keys() and not \
                    self._special_types_validators_map.get(legal_type)(field_value):
                invalid_types.append(legal_type)
        return invalid_types

    @staticmethod
    def _validate_date(value: str):
        try:
            date_format = "%d-%m-%Y"
            if value != datetime.strptime(value, date_format).strftime(date_format):
                return False
            return True
        except (ValueError, TypeError):
            return False

    # TODO: merge all the regex functions
    @staticmethod
    def _validate_email(value: str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        try:
            if re.fullmatch(regex, value):
                return True
            return False
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _validate_uuid(value: str):
        regex = '^[A-Za-z0-9-]+$'
        try:
            if re.fullmatch(regex, value):
                return True
            return False
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _validate_auth_token(value: str):
        regex = '^Bearer [A-Za-z0-9]+$'
        try:
            if re.fullmatch(regex, value):
                return True
            return False
        except (ValueError, TypeError):
            return False
