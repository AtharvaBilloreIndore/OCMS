from fastapi.testclient import TestClient
from OCMSmain import app
client = TestClient(app)

def test_create_student_valid():
    payload = {"name":"Dhruv Patel",
               "education":"UG",
               "email":"dhruv@abc.com"}
    response = client.post("/students", json = payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["student_id"],int)
    assert isinstance(data["name"],str)

def test_read_student():
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_student_valid():
    response = client.patch("/students/1",json = {"education":"PG","email":"patel@abc.com"})
    assert response.status_code == 200
    assert "education" in response.json() 
    assert "email" in response.json()

def test_update_student_invalid():
    response = client.patch("/students/20", json = {"education":"PG","email":"pawar@abc.com"} )
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_delete_student_valid():
    response = client.delete("/students/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Student soft-deleted successfully"

def test_delete_student_invalid():
    response = client.delete("/students/21")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"