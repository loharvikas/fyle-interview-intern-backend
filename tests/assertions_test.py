

def test_assert_auth(client):
    response = client.get(
        '/principal/assignments',
    )

    assert response.status_code == 401
    assert response.json['message'] == 'principal not found'




def test_assert_true(client, h_principal):
    response = client.get(
        '/student/assignments',
        headers=h_principal
    )

    assert response.status_code == 403
    assert response.json['message'] == 'requester should be a student'