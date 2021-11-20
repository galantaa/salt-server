from typing import Optional

from pydantic import BaseModel


# TODO: add validations to name, types, required
class Model(BaseModel):
    path: str
    method: str
    query_params: list
    headers: list
    body: list


class Models:
    def __init__(self):
        self.models = {}

    def add_model(self, model: Model):
        try:
            parsed_model = self.parse_model(model)
            self.models.update(parsed_model)
        except Exception as e:
            raise e

    @staticmethod
    def parse_model(model: Model):
        try:
            key = f"({model.path}, {model.method})"
            parsed_model = {
                key: {
                    "query_params": model.query_params,
                    "headers": model.headers,
                    "body": model.body
                }
            }
            return parsed_model
        except Exception as e:
            print('failed parsing model')
            raise e

    def get_models(self):
        return self.models

    def get_model_by_key(self, key: str) -> Optional[dict]:
        return self.models.get(key)
