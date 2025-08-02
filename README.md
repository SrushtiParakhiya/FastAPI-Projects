# FastAPI JWT Auth & RBAC Project

A robust FastAPI application with JWT authentication, role-based access control (RBAC), and project management capabilities. Features secure password validation, comprehensive error handling, and support for both local development and cloud deployment.

## 🌐 Live Demo

**API Documentation**: https://codingsphere-crud-assignment.onrender.com/docs#

**Base URL**: https://codingsphere-crud-assignment.onrender.com/

> **Note**: The API is deployed on Render and may take a few seconds to wake up on the first request.

## 🎥 Project Demo Video

**Watch the complete setup and usage demonstration:**

**Usage Video Link**: https://drive.google.com/file/d/1EqMeKT8reunDFQnfgC3fUjbmy-HBeTjU/view?usp=sharing

**Video Contents:**
- ✅ Complete project setup and configuration
- ✅ Local development environment setup
- ✅ Interactive API testing with Swagger UI
- ✅ User registration and authentication
- ✅ JWT token-based security demonstration
- ✅ Role-based access control (Admin/User)
- ✅ Project CRUD operations
- ✅ Error handling and validation
- ✅ Production deployment showcase

> **Duration**: ~18 minutes | **Format**: MP4

## 🚀 Features

- 🔐 **JWT-based authentication** with secure token management
- 👥 **Role-based access control** (Admin/User roles)
- 📁 **Project CRUD operations** with proper authorization
- 🛡️ **Strong password validation** (8+ chars, uppercase, lowercase, numbers, special chars)
- 📊 **Database support** for PostgreSQL and SQLite
- 🚨 **Comprehensive error handling** with try-catch blocks
- 📝 **Detailed logging** for debugging and monitoring
- ☁️ **Cloud deployment ready** for Render platform
- 🔧 **Environment-based configuration**

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLModel, SQLAlchemy
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: JWT (python-jose), bcrypt (passlib)
- **Validation**: Pydantic
- **Deployment**: Render
- **Environment**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL (for production)
- Git
- Render account (for deployment)

## 🏗️ Project Structure

```
app/
├── main.py              # FastAPI application and API endpoints
├── auth.py              # Authentication and authorization logic
├── models.py            # SQLModel database models
├── schemas.py           # Pydantic schemas for request/response
├── database.py          # Database configuration and session management
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🚀 Quick Start

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/SrushtiParakhiya/FastAPI-Projects.git
cd FastAPI-Projects/app
```

#### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration

Create a `.env` file in the app directory:

```bash
# Copy the example (if available) or create manually
touch .env
```

Add the following environment variables to `.env`:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/database_name"

# JWT Configuration
SECRET_KEY="your-super-secret-key-change-this-in-production"
ALGORITHM="HS256"
```

#### 5. Database Setup

**Option A: PostgreSQL (Recommended)**
1. Install PostgreSQL and create a database
2. Update `DATABASE_URL` in `.env` with your credentials
3. The application will automatically create tables on startup

**Option B: SQLite (Development)**
- Leave `DATABASE_URL` empty or comment it out
- The application will automatically use SQLite

#### 6. Run the Application
```bash
uvicorn main:app --reload
```

The API will be available at: http://127.0.0.1:8000

## 📚 API Documentation

### Local Development
- **Interactive API Docs**: http://127.0.0.1:8000/docs#
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc

### Production (Deployed)
- **Interactive API Docs**: https://codingsphere-crud-assignment.onrender.com/docs
- **ReDoc Documentation**: https://codingsphere-crud-assignment.onrender.com/redoc

## 🔐 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register a new user | No |
| POST | `/login` | Login and get JWT token | No |

### Projects (Requires Authentication)
| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/projects` | List all projects | Any |
| POST | `/projects` | Create a new project | Admin |
| GET | `/projects/{id}` | Get a specific project | Any |
| PUT | `/projects/{id}` | Update a project | Admin |
| DELETE | `/projects/{id}` | Delete a project | Admin |

## 🔒 Password Requirements

When registering a user, passwords must meet these criteria:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)
- ✅ At least one number (0-9)
- ✅ At least one special character (!@#$%^&*()_+-=[]{}|;':",./<>?)

**Example valid passwords:**
- `Admin123!`
- `MyPass@2024`
- `Secure#Pass1`

## 🧪 Testing the Deployed API

### Quick Test with curl

#### 1. Register a new user
```bash
curl -X POST "https://codingsphere-crud-assignment.onrender.com/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!",
    "role": "user"
  }'
```

#### 2. Login to get JWT token
```bash
curl -X POST "https://codingsphere-crud-assignment.onrender.com/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

#### 3. Use the token to access protected endpoints
```bash
# Replace YOUR_JWT_TOKEN with the token from login response
curl -X GET "https://codingsphere-crud-assignment.onrender.com/projects" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Testing with Postman or Browser

1. Visit https://codingsphere-crud-assignment.onrender.com/docs#
2. Use the interactive Swagger UI to test all endpoints
3. Register a user first, then login to get your JWT token
4. Click the "Authorize" button and enter your token
5. Test all the protected endpoints

