def test_home_route(client, h_student_1):
    response = client.get(
        '/',
        headers=h_student_1
    )

    assert response.status_code == 200
    