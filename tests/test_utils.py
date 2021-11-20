import unittest
from utils import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()

    def test_valid_date(self):
        assert Utils._validate_date("14-02-1986")

    def test_invalid_date_format(self):
        assert not Utils._validate_date("02-14-1986")
        assert not Utils._validate_date("1986-14-02")
        assert not Utils._validate_date("14-02-86")
        assert not Utils._validate_date("")
        assert not Utils._validate_date(33)  # should throw TypeError

    def test_valid_email(self):
        assert Utils._validate_email("alon.galant@gmail.com")
        assert Utils._validate_email("alongalant@gmail.com")

    def test_invalid_email(self):
        assert not Utils._validate_email("alon.galant@gmailcom")
        assert not Utils._validate_email("alongalantgmail.com")
        assert not Utils._validate_email("")
        assert not Utils._validate_email(33)  # should throw TypeError

    def test_valid_uuid(self):
        assert Utils._validate_uuid("46da6390-7c78-4a1c-9efa-7c0396067ce4")
        assert Utils._validate_uuid("46")

    def test_invalid_uuid(self):
        assert not Utils._validate_uuid("46da6390-7c78-4a1c-9efa-7c0396067ce4_")
        assert not Utils._validate_uuid("")
        assert not Utils._validate_uuid(34)  # should throw TypeError

    def test_valid_auth_token(self):
        assert Utils._validate_auth_token("Bearer ebb3cbbe938c4776bd22a4ec2ea8b2ca")
        assert Utils._validate_auth_token("Bearer 2")

    def test_invalid_auth_token(self):
        assert not Utils._validate_auth_token("Bearerebb3cbbe938c4776bd22a4ec2ea8b2ca")
        assert not Utils._validate_auth_token("Bearer ")
        assert not Utils._validate_auth_token("46da6390-7c78-4a1c-9efa-7c0396067ce4_")
        assert not Utils._validate_auth_token("")
        assert not Utils._validate_auth_token(34)  # should throw TypeError
