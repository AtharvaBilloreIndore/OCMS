# Online Course Management System (OCMS)

## Overview

The Online Course Management System (OCMS) is a backend application built with FastAPI, SQLAlchemy, and MySQL. It offers an easy way to manage courses, students, instructors, and enrollments using RESTful APIs. The system maintains data integrity with relational mappings, supports soft deletions, and has data validations. We use pytest for unit testing and Postman for API testing.

---

## Features

* Course Management: Create, update, fetch, and soft delete courses.
* Student Management: Register, update, fetch, and soft delete student records.
* Instructor Management: Manage instructors and their course assignments.
* Enrollment Handling: Enroll students in courses with validations.
* Soft Deletion: Mark records as inactive without losing data.
* Data Validation: Pydantic schemas ensure strict validation of request and response payloads.
* Unit Testing: Extensive test coverage with pytest for positive, negative, and edge cases.
* API Testing: All APIs are tested with Postman.

---

## Tech Stack

* Framework: FastAPI
* ORM: SQLAlchemy
* Database: MySQL
* Validation: Pydantic
* Testing: pytest, Postman
* Version Control: Git & GitHub

---

## Project Structure

```
OCMS/
├── .vscode/            # VS Code configurations
├── routers/            # Contains route files for courses, students, instructors, enrollments
├── tests/              # Unit tests for APIs
├── .gitignore          # Ignored files and folders
├── OCMSdb.py           # Database connection setup
├── OCMSmain.py         # Entry point of the application
├── OCMSmodels.py       # SQLAlchemy models for all entities
├── schemas.py          # Pydantic schemas for request/response validation
└── test_debug.db       # SQLite database used for testing
```

---

## Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/AtharvaBilloreIndore/OCMS.git
cd OCMS
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure the Database

* Update OCMSdb.py with your MySQL credentials:

```python
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://<username>:<password>@localhost/<database_name>"
```

### Run the Application

```bash
uvicorn OCMSmain:app --reload
```

By default, the app will run at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## API Endpoints

### Courses

* `GET /courses` → Fetch all available courses
* `POST /courses` → Create a new course
* `PUT /courses/{id}` → Update a course
* `DELETE /courses/{id}` → Soft delete a course

### Students

* `GET /students` → Fetch all students
* `POST /students` → Register a student
* `PUT /students/{id}` → Update a student
* `DELETE /students/{id}` → Soft delete a student

### Instructors

* `GET /instructors` → Fetch all instructors
* `POST /instructors` → Register an instructor
* `PUT /instructors/{id}` → Update an instructor
* `DELETE /instructors/{id}` → Soft delete an instructor

### Enrollments

* `GET /enrollments` → Fetch enrollment details
* `POST /enrollments` → Enroll a student in a course

For detailed API usage and payloads, refer to the Postman collection.

---

## Running Tests

Run the test suite using pytest:

```bash
pytest
```

By default, tests run against a SQLite test database (`test_debug.db`) to avoid affecting production data.

---

## Git Workflow

* Create feature branches for new tasks.
* Commit changes with meaningful messages.
* Open Pull Requests (PRs) for review before merging.

---

## Contributing

Contributions are welcome! Please fork the repo and create a pull request for any enhancements or fixes.

---

## License

This project is licensed under the MIT License.

---

## Author

**Atharva Billore**
[GitHub Profile](https://github.com/AtharvaBilloreIndore)
