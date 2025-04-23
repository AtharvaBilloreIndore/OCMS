from fastapi.testclient import TestClient
from OCMSmain import app
client = TestClient(app)

def test_create_course_valid():
    payload = {
        "title": "Data Structures",
        "description": "Core CS topic",
        "instructor_ids": [1]
    }
    response = client.post("/courses", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Course created successfully"
    assert isinstance(data["course_id"], int)
    assert data["instructor_ids"] == [1]

def test_create_course_invalid_instructor():
    payload = {
        "title": "Invalid Course",
        "description": "Should fail",
        "instructor_ids": [99]  
    }

    response = client.post("/courses", json=payload)
    assert response.status_code == 400
    assert "Instructors {99} not found" in response.json()["detail"]

def test_read_course():
    response = client.get("/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_course_valid():

    update_response = client.put(f"/courses/1", json={
        "title": "Updated Title",
        "description": "Updated Desc",
        "instructor_ids": [1]
    })

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["message"] == "Course updated successfully"
    assert data["course"]["title"] == "Updated Title"
    assert data["course"]["description"] == "Updated Desc"

def test_update_course_invalid_courseid():
    response = client.put("/courses/99", json={
        "title": "Backend development",
        "description": "Backend development course for beginners.",
        "instructor_ids": [1]
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"

def test_delete_course_valid():

    create_response = client.post("/courses", json={
        "title": "Delete Me",
        "description": "To be deleted",
        "instructor_ids": [2]
    })
    course_id = create_response.json()
    
    delete_response = client.delete("/courses/2")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Course soft-deleted successfully"

    all_courses = client.get("/courses").json()
    assert all(course["course_id"] != course_id for course in all_courses)


def test_delete_course_invalid():
    response = client.delete("/courses/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"

