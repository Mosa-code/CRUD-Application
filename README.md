# CRUD-Application

A simple CRUD API built with **FastAPI**, **PostgreSQL**, **Docker**, and **Docker Compose**.
This application allows creating, reading, updating, and deleting users, each defined by their `name`, `age`, and `birth_state`.

## Features

* RESTful API with all CRUD operations (`Create`, `Read`, `Update`, `Delete`)
* PostgreSQL database
* Dockerized backend and database
* Postman and terminal testing support
* Ready to expand with even more integration testing

---

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
### postgres

Of course we want to be able to connect directly to our database. we can do that easily like so:

```powershell
docker exec -it postgres psql -U postgres -d postgres

psql (15.13 (Debian 15.13-1.pgdg120+1))                                                                                    
Type "help" for help.

postgres=# 
```

here we can simply test some sql queries to ensure everything is running. here are some results

```powershell
postgres=# SELECT * FROM users;
 id |   name   | age | birth_state 
----+----------+-----+-------------
  2 | Noah     |  18 | IL
  3 | Mio      |  19 | IL
  4 | TestUser |  99 | ZZ
  5 | Updated  |  21 | BB
  7 | TestUser |  99 | ZZ
  8 | Updated  |  21 | BB
(6 rows)

postgres=# SELECT name, age FROM users WHERE age = 99;
   name   | age 
----------+-----
 TestUser |  99
 TestUser |  99
(2 rows)

postgres=# SELECT name, age FROM users WHERE name = 'Mio';
 name | age 
------+-----
 Mio  |  19
(1 row)

postgres=# DELETE FROM users WHERE id NOT IN (SELECT MIN(id) from users GROUP BY name, age, birth_state);
DELETE 2
postgres=# SELECT * FROM users;
 id |   name   | age | birth_state 
----+----------+-----+-------------
  2 | Noah     |  18 | IL
  3 | Mio      |  19 | IL
  4 | TestUser |  99 | ZZ
  5 | Updated  |  21 | BB
(4 rows)

```
We showed here that we are both able to query and alter the table through raw sql if need be. 

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
|   └── test_database.py
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt

```

---

## Integration Tests

This project includes automated tests to verify API functionality using pytest and FastAPI's TestClient.

### Testing Stack

- pytest: Test runner
- httpx: for async request simulation
- pytest-asyncio: supports async test functions
- FastAPI TestClient: makes sync test simple
- SQLAlchemy: scoped session for isolated DB access

### how it works
The tests use a custom testing database session to override the production DB. This is handled by overriding FastAPI's get_db dependency with TestingSessionLocal:

```python
app.dependency_overrides[get_db] = override_get_db
```

### running tests
This is the command I used to rest the project

```powershell
$env:PYTHONPATH="."; $env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"; pytest
```
### Current Coverage

- POST /users/ - create a user and checks response data
- GET /users/ - retrieves user list and validates format
- PUT /users/{id} - updates a user and asserts changes
- DELETE /users/{id} - deletes a user and confirmes removal

These test cases can be found in test_users.py. It should be noted that these tests hit a lical PostgreSQL instance. Make sure its running, or adjust DATABASE_URL in your test config
---

## Author

Mosa Abdelnabi