from fastapi.testclient import TestClient
from OCMSmain import app
client = TestClient(app)

def test_create_instructor_valid():
    payload = {"name":"Prakash choubey",
               "email":"prakash@abc.com",
               "expertise":"Frontend Development"}
    response = client.post("/instructors/register",json=payload) 
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["instructor_id"],int)
    assert isinstance(data["name"],str)

def test_read_instructor():
    response = client.get("/instructors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_instructor_valid_courseid():
    response = client.get("/instructors/1")
    assert response.status_code == 200
    assert "instructors" in response.json()

def test_instructor_invalid_courseid():
    response = client.get("/instructors/50")
    assert response.status_code == 404
    assert "Course not found" in response.json()["detail"]        

def test_update_instructor_valid():
    update_response = client.patch(f"/instructors/1", json={"expertise":"Frontend development, Backend Development"})
    assert update_response.status_code == 200
    assert "expertise" in update_response.json()

def test_update_instructor_invalid():
    response = client.patch("/instructors/25", json={"expertise":"Frontend development, Backend Development"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Instructor not found"

def test_delete_instructor_valid():
    response = client.delete("/instructors/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Instructor soft-deleted successfully"


def test_delete_instructor_invalid():
    response = client.delete("/instructors/15")
    assert response.status_code == 404
    assert response.json()["detail"] == "Instructor not found"
