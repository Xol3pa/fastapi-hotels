import pytest


async def test_get_me(auth_ac):
    response = await auth_ac.get(
        "/auth/me"
    )

    assert response.status_code in [200, 201]
    assert response.json() == {'id': 1, 'email': 'test@mail.ru'}


@pytest.mark.parametrize(
    "email, password, register_status_code",
    [
        ("test1@mail.ru", "12345678", 200),
        ("test2@mail.ru", "12345678", 200),
        ("test3@mail.ru", "12345678", 200),
        ("test1@mail.ru", "12345678", 409),
    ]
)
async def test_authorisation_flow(
        email, password, register_status_code,
        ac,
):
    register_response = await ac.post(
        "/auth/register",
        json={
            'email': email,
            'password': password,
        }
    )
    assert register_response.status_code == register_status_code
    if register_status_code != 200:
        return

    response_login = await ac.post(
        "/auth/login",
        json={
            'email': email,
            'password': password,
        }
    )
    assert response_login.status_code == 200
    assert "access_token" in response_login.cookies


    response_me = await ac.get(
        "/auth/me",
    )
    assert response_me.status_code == 200
    assert response_me.json()["email"] == email

    response_logout = await ac.post(
        "/auth/logout",
    )

    assert response_logout.status_code == 200
    assert "access_token" not in response_logout.cookies

