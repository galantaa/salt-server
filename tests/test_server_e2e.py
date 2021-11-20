import unittest
import json
import os
from models import Model
from httpx import AsyncClient

from main import app, models


class TestServerE2e(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._add_models_from_file()

    @staticmethod
    def _add_models_from_file():
        dirname = os.path.dirname(__file__)
        models_filename = os.path.join(dirname, 'models.json')
        models_file = open(models_filename)
        models_list = json.load(models_file)
        for model in models_list:
            models.add_model(Model(**model))
        models_file.close()
        print("Done adding models from file")
        print(f'The models {models.get_models()}')

    async def test_server_e2e_with_requests_file(self):
        """
        Load all the models from the example file and run validations for all the example requests.
        Making sure it won't crash and that results looks ok
        """
        dirname = os.path.dirname(__file__)
        requests_filename = os.path.join(dirname, 'requests.json')
        requests_file = open(requests_filename)
        requests = json.load(requests_file)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            for request in requests:
                print(f'sending request {request}')
                response = await ac.post("/requests/validate", json=request)
                print(f'got response {response.text}')
                assert response.status_code == 200
        requests_file.close()
