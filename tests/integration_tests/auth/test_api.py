


async def test_get_me(auth_ac):
    response = await auth_ac.post(
        "/auth/me"
    )

    assert response.status_code in [200, 201]
    assert response.json() == {'id': 1, 'email': 'test@mail.ru'}