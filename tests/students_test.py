def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2





def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    """
    success case: create an assignment
    """
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    """
    success case: submit an assignment
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2,
            "content": "ABCD TESTPOST"
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    """
    failure case: assignment cannot be resubmitted
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'


def test_update_assignment_that_does_not_exist(client, h_student_1):
    """
    failure case: update an assignment that does not exist.
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id":1000,
            'content': "Testing"
        })

    assert response.status_code == 404

def test_post_assignment_not_in_draft(client, h_student_1):
    """
    failure case: content cannot be null
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id":2,
            'content': "Testing"
        })

    assert response.status_code == 400


def test_update_assignment(client, h_student_1):
    """
    success case: update an assignment
    """
    # create new assignment
    assignment = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "content": "ABCD TESTPOST"
        }
    )

    # update assignment
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id": assignment.json['data']['id'],
            "content": "ABCD TESTPOST"
        }
    )

    assert response.status_code == 200
    data = response.json

    assert data['data']['content'] == 'ABCD TESTPOST'