import json


def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']

def test_grade_assignment(client, h_teacher_1):
    """
    success case: grade an assignment
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 200
    data = response.json

    assert data['data']['grade'] == 'A'

def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'



def test_get_teacher_detail_does_not_exist(client):
    """
    failure case: If a teacher does not exists check and throw 404
    """
    response = client.get(
        '/teacher/detail',
        headers= {
        'X-Principal': json.dumps({
            'teacher_id': 10000000,
            'user_id': 1
        })
        }
    )

    assert response.status_code == 404


def test_get_teacher_detail(client, h_teacher_1):
    """
    success case: get teacher detail
    """
    response = client.get(
        '/teacher/detail',
        headers=h_teacher_1
    )

    assert response.status_code == 200
    data = response.json

    assert data['data']['id'] == 1


def test_create_teacher(client):
    """
    success case: create a new teacher
    """
    response = client.post(
        '/teacher/create',
        json={
            "email": "test@gmail.com",
            "username": "test",
        })
    
    assert response.status_code == 200


def test_create_teacher_with_existing_email(client):
    """
    failure case: create a new teacher with existing email
    """
    response = client.post(
        '/teacher/create',
        json={
            "email": "test@gmail.com",
            "username": "test1",
        })
    


    assert response.status_code == 500


def test_create_teacher_with_existing_username(client):
    """
    failure case: create a new teacher with existing username
    """
    response = client.post(
        '/teacher/create',
        json={
            "email": "new@gmail.com",
            "username": "test",
        })


    assert response.status_code == 500
    