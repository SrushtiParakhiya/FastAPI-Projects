# FastAPI JWT Auth & RBAC Project

A robust FastAPI application with JWT authentication, role-based access control (RBAC), and project management capabilities. Features secure password validation, comprehensive error handling, and support for both local development and cloud deployment.

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
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST="127.0.0.1"
PORT=8000
DEBUG=True
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

- **Interactive API Docs**: http://127.0.0.1:8000/docs#
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc

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

## ☁️ Render Deployment

### 1. Prepare for Deployment

#### Update Environment Variables for Production
Create a production `.env` file or use Render's environment variables:

```env
# Production Database (Render PostgreSQL)
DATABASE_URL="postgresql://username:password@host:port/database_name"

# Production JWT Settings
SECRET_KEY="your-production-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Production Server Settings
HOST="0.0.0.0"
PORT=8000
DEBUG=False
```

### 2. Deploy to Render

#### Step 1: Create a New Web Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository

#### Step 2: Configure the Service
- **Name**: `fastapi-jwt-auth` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Step 3: Set Environment Variables
In Render dashboard, add these environment variables:

```env
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Step 4: Deploy
1. Click "Create Web Service"
2. Render will automatically deploy your application
3. Your API will be available at: `https://your-app-name.onrender.com`

### 3. Database Setup on Render

#### Option A: Use Render PostgreSQL
1. Create a new PostgreSQL database in Render
2. Copy the connection string to your environment variables
3. The application will automatically create tables

#### Option B: Use External Database
1. Configure your external PostgreSQL database
2. Update `DATABASE_URL` in Render environment variables

## 🔧 Development

### Adding New Features
1. Add endpoints in `main.py`
2. Update models in `models.py` if needed
3. Add schemas in `schemas.py`
4. Test locally before deploying

### Database Migrations
- The application uses SQLModel which automatically creates tables
- For schema changes, update models and redeploy

### Error Handling
All endpoints include comprehensive error handling:
- ✅ Try-catch blocks
- ✅ Structured error responses
- ✅ Request validation
- ✅ Detailed logging

## 🐛 Troubleshooting

### Local Development Issues

#### Database Connection Problems
```bash
# Check if PostgreSQL is running
sudo service postgresql status  # Linux
brew services list | grep postgresql  # macOS

# Verify connection string
echo $DATABASE_URL
```

#### Import Errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

### Render Deployment Issues

#### Build Failures
- Check build logs in Render dashboard
- Verify `requirements.txt` is in the correct directory
- Ensure all dependencies are listed

#### Runtime Errors
- Check application logs in Render dashboard
- Verify environment variables are set correctly
- Ensure database connection string is valid

#### Database Connection Issues
- Verify PostgreSQL service is running
- Check connection string format
- Ensure database exists and is accessible

## 📝 Environment Variables Reference

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@host:port/db` | Yes |
| `SECRET_KEY` | JWT secret key | `your-secret-key` | Yes |
| `ALGORITHM` | JWT algorithm | `HS256` | No (default) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `30` | No (default) |
| `HOST` | Server host | `0.0.0.0` | No (default) |
| `PORT` | Server port | `8000` | No (default) |
| `DEBUG` | Debug mode | `False` | No (default) |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the application logs
3. Create an issue in the GitHub repository
4. Contact the maintainers

---

**Happy Coding! 🚀**