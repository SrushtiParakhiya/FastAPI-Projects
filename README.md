# FastAPI JWT Auth & RBAC Example

A simple RESTful API using FastAPI, SQLModel, PostgreSQL, JWT authentication, and Role-Based Access Control (RBAC).

## Features
- User registration and login with hashed passwords
- JWT-based authentication
- Role-based access control (admin/user)
- CRUD for projects (admin: full access, user: read-only)

## Tech Stack
- FastAPI
- SQLModel
- PostgreSQL
- python-jose (JWT)
- passlib (bcrypt)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/SrushtiParakhiya/FastAPI-Projects.git
cd app
```

### 2. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Edit `app/database.py` and set your PostgreSQL connection string:
```python
DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<database>"
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

### 5. API Usage

#### Register a User
```
POST /register
{
  "username": "admin",
  "password": "adminpass",
  "role": "admin"
}
```

#### Login
```
POST /login
Content-Type: application/json
username=admin&password=adminpass
```
Response:
```
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

#### Authenticated Requests
Add header:
```
Authorization: Bearer <JWT_TOKEN>
```

#### Get Projects (all users)
```
GET /projects
```

#### Create Project (admin only)
```
POST /projects
{
  "name": "Project A",
  "description": "Description of project"
}
```

#### Update Project (admin only)
```
PUT /projects/{project_id}
{
  "name": "New Name",
  "description": "Updated description"
}
```

#### Delete Project (admin only)
```
DELETE /projects/{project_id}
```

## Video Demo
```
video link
```

---

## License
MIT