from src.services.auth import AuthService


def test_create_access_token():
    data = {"userid": 1}
    encoded_jwt = AuthService().create_access_token(data)

    assert encoded_jwt
    assert isinstance(encoded_jwt, str)
