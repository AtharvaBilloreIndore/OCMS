from fastapi.testclient import TestClient
from OCMSmain import app
client = TestClient(app)

def test_enrollment_valid_studentid_courseid():
    payload = {"student_id":"1","course_id":"1"}
    response = client.post("/enrollments", json = payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["enrollment_id"],int)
    assert isinstance(data["student_id"],int)
    assert isinstance(data["course_id"],int)
    assert isinstance(data["enrollment_date"],str)

def test_enrollment_invalid_studentid():
    payload = {"student_id": "62","course_id":"2"}

    response = client.post("/enrollments", json=payload)
    assert response.status_code == 404
    assert "Student not found" in response.json()["detail"]

def test_enrollment_invalid_courseid():
    payload = {"student_id": "1","course_id":"62"}

    response = client.post("/enrollments", json=payload)
    assert response.status_code == 404
    assert "Course not found" in response.json()["detail"]

def test_enrollment_already_exist():
    payload = {"student_id":"1","course_id":"1"}
    response = client.post("/enrollments", json = payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Enrollment already exists"

def test_enrollment_valid_studentid():
    response = client.get("/enrollments/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["enrollment_id"],int)
    assert isinstance(data["enrollment_date"],str)

def test_instructor_invalid_studentid():
    response = client.get("/enrollments/6")
    assert response.status_code == 404
    assert response.json()["detail"] == "Enrollment not found"  