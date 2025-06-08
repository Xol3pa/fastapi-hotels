from src.services.auth import AuthService


def test_create_access_token():
    data = {'userid': 1}
    encoded_jwt = AuthService().create_access_token(data)

    assert encoded_jwt
    assert isinstance(encoded_jwt, str)

    decoded_jwt = AuthService().decode_access_token(encoded_jwt)

    assert decoded_jwt
    assert decoded_jwt.get('exp')
    assert decoded_jwt.get('userid') == data.get('userid')