# CRUD-Application

A simple CRUD API built with **FastAPI**, **PostgreSQL**, **Docker**, and **Docker Compose**.
This application allows creating, reading, updating, and deleting users, each defined by their `name`, `age`, and `birth_state`.

## Features

* RESTful API with all CRUD operations (`Create`, `Read`, `Update`, `Delete`)
* PostgreSQL database
* Dockerized backend and database
* Postman and terminal testing support
* Ready to expand with integration testing

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

* Docker
* Docker Compose

### Running the Application

To spin up the backend and database:

```bash
docker-compose up --build
```

The API will be live at:

```
http://localhost:8000
```

FastAPI docs:

```
http://localhost:8000/docs
```

---

## Initial Testing

I tested my files in Postman, but I added Invoke-RestMethod commands to show that it can be done in the terminal as well.

### POST

You can create users by sending a POST request.

**PowerShell**:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/users/ -Method POST -Body '{"name":"Alice","age":30,"birth_state":"NY"}' -ContentType "application/json"
Invoke-RestMethod -Uri http://localhost:8000/users/ -Method POST -Body '{"name":"Noah","age":18,"birth_state":"IL"}' -ContentType "application/json"
```

**Postman**:

* URL: `http://localhost:8000/users/`
* Method: POST
* Body (JSON):

```json
{
    "name": "Mio",
    "age": 18,
    "birth_state": "IN"
}
```

Successful response:

```json
{
    "name": "Mio",
    "age": 18,
    "birth_state": "IN",
    "id": 3
}
```

IDs are assigned in order, and once deleted, IDs are not reused (e.g., deleting user 1 means the next added user will be 4).

### DELETE

To remove a user:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/users/1 -Method DELETE
```

### GET

To retrieve all users:

```bash
GET http://localhost:8000/users/
```

Response:

```json
[
    {
        "name": "Noah",
        "age": 18,
        "birth_state": "IL",
        "id": 2
    },
    {
        "name": "Mio",
        "age": 18,
        "birth_state": "IN",
        "id": 3
    }
]
```

### PUT

Update a user completely by ID. For example, to update Mio (ID 3):

* URL: `http://localhost:8000/users/3`
* Method: PUT
* Body:

```json
{
  "name": "Mio",
  "age": 19,
  "birth_state": "IL"
}
```

Updated response:

```json
{
    "name": "Mio",
    "age": 19,
    "birth_state": "IL",
    "id": 3
}
```

---

## Project Structure

```
.
├── app
│   ├── main.py            # FastAPI app and endpoints
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # DB engine/session
│   ├── schemas.py         # Pydantic schemas
│   └── crud.py             # Optional: CRUD operations (if separated)
├── tests
│   └── test_users.py      # Integration tests (to be implemented)
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Integration Tests

*To be implemented.*
Tests will live in the `/tests` directory and use a test DB.

---

## Author

Mosa Abdelnabi