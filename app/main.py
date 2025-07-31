import logging
import re
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List
from models import User, Project
from schemas import UserCreate, UserRead, ProjectCreate, ProjectRead
from database import engine, get_session
from auth import hash_password, verify_password, create_access_token, get_current_user, require_admin, require_user, validate_password_strength
from pydantic import BaseModel, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created (if not exist)")

# User Registration
@app.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(request: Request, user: UserCreate = None, session: Session = Depends(get_session)):
    try:
        if request.method != "POST":
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        if user is None or not user.username or not user.password or not user.role:
            raise HTTPException(status_code=422, detail="Missing required user registration fields.")
        
        # Validate role
        if user.role not in ["admin", "user"]:
            raise HTTPException(
                status_code=406,
                detail="Role must be 'admin' or 'user'"
            )
        
        # Validate password strength
        if not validate_password_strength(user.password):
            raise HTTPException(
                status_code=422, 
                detail= "Password must be at least 8 characters long and contain uppercase letters, lowercase letters, numbers, and special characters."
            )
        
        logger.info(f"Registration attempt for username: {user.username}")
        existing = session.exec(select(User).where(User.username == user.username)).first()
        if existing:
            logger.warning(f"Registration failed: Username '{user.username}' already exists.")
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_pw = hash_password(user.password)
        db_user = User(username=user.username, password=hashed_pw, role=user.role)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        logger.info(f"User registered successfully: {user.username} (role: {user.role})")
        return db_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Registration failed", "message": str(e)})

# Login request model
class LoginRequest(BaseModel):
    username: str
    password: str

# User Login
@app.post("/login")
def login(request: Request, login_request: LoginRequest = None, session: Session = Depends(get_session)):
    try:
        if request.method != "POST":
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        if login_request is None or not login_request.username or not login_request.password:
            raise HTTPException(status_code=422, detail="Missing username or password.")
        logger.info(f"Login attempt for username: {login_request.username}")
        user = session.exec(select(User).where(User.username == login_request.username)).first()
        if not user or not verify_password(login_request.password, user.password):
            logger.warning(f"Login failed for username: {login_request.username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token({"sub": str(user.id), "role": user.role})
        logger.info(f"Login successful for username: {login_request.username} (role: {user.role})")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Login failed", "message": str(e)})

# Get all projects (any authenticated user)
@app.get("/projects", response_model=List[ProjectRead])
def get_projects(request: Request, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        if request.method != "GET":
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        logger.info(f"User {user.username} (role: {user.role}) requested all projects.")
        projects = session.exec(select(Project)).all()
        logger.info(f"Returned {len(projects)} projects.")
        return projects
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Get projects error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch projects", "message": str(e)})

# Create project (admin only)
@app.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(request: Request, project: ProjectCreate = None, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    try:
        if request.method != "POST":
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        if project is None or not project.name or not project.description:
            raise HTTPException(status_code=422, detail="Missing required project fields.")
        logger.info(f"Admin {user.username} is creating a project: {project.name}")
        db_project = Project(name=project.name, description=project.description, user_id=user.id)
        session.add(db_project)
        session.commit()
        session.refresh(db_project)
        logger.info(f"Project created: {db_project.name} (id: {db_project.id}) by admin {user.username}")
        return db_project
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Create project error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Project creation failed", "message": str(e)})

# Get single project (any authenticated user)
@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(request: Request, project_id: int = None, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        if request.method != "GET":
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        if project_id is None:
            raise HTTPException(status_code=422, detail="Project ID is required.")
        logger.info(f"User {user.username} (role: {user.role}) requested project id {project_id}.")
        project = session.get(Project, project_id)
        if not project:
            logger.warning(f"Project id {project_id} not found.")
            raise HTTPException(status_code=404, detail="Project not found")
        logger.info(f"Project returned: {project.name} (id: {project.id})")
        return project
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Get project error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch project", "message": str(e)})

# Update project (admin only)
@app.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(request: Request, project_id: int = None, project: ProjectCreate = None, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    try:
        if request.method != "PUT":
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        if project_id is None or project is None or not project.name or not project.description:
            raise HTTPException(status_code=422, detail="Missing required fields for project update.")
        logger.info(f"Admin {user.username} is updating project id {project_id}.")
        db_project = session.get(Project, project_id)
        if not db_project:
            logger.warning(f"Update failed: Project id {project_id} not found.")
            raise HTTPException(status_code=404, detail="Project not found")
        db_project.name = project.name
        db_project.description = project.description
        session.add(db_project)
        session.commit()
        session.refresh(db_project)
        logger.info(f"Project updated: {db_project.name} (id: {db_project.id}) by admin {user.username}")
        return db_project
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Update project error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Project update failed", "message": str(e)})

# Delete project (admin only)
@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(request: Request, project_id: int = None, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    try:
        if request.method != "DELETE":
            raise HTTPException(status_code=405, detail="Method Not Allowed")
        if project_id is None:
            raise HTTPException(status_code=422, detail="Project ID is required for deletion.")
        logger.info(f"Admin {user.username} is deleting project id {project_id}.")
        db_project = session.get(Project, project_id)
        if not db_project:
            logger.warning(f"Delete failed: Project id {project_id} not found.")
            raise HTTPException(status_code=404, detail="Project not found")
        session.delete(db_project)
        session.commit()
        logger.info(f"Project deleted: id {project_id} by admin {user.username}")
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Delete project error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Project deletion failed", "message": str(e)})