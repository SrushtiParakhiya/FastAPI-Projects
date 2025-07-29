import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from models import User, Project
from schemas import UserCreate, UserRead, ProjectCreate, ProjectRead
from database import engine, get_session
from auth import hash_password, verify_password, create_access_token, get_current_user, require_admin, require_user
from pydantic import BaseModel

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
def register(user: UserCreate, session: Session = Depends(get_session)):
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

# Login request model
class LoginRequest(BaseModel):
    username: str
    password: str

# User Login
@app.post("/login")
def login(request: LoginRequest, session: Session = Depends(get_session)):
    logger.info(f"Login attempt for username: {request.username}")
    user = session.exec(select(User).where(User.username == request.username)).first()
    if not user or not verify_password(request.password, user.password):
        logger.warning(f"Login failed for username: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    logger.info(f"Login successful for username: {request.username} (role: {user.role})")
    return {"access_token": access_token, "token_type": "bearer"}

# Get all projects (any authenticated user)
@app.get("/projects", response_model=List[ProjectRead])
def get_projects(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    logger.info(f"User {user.username} (role: {user.role}) requested all projects.")
    projects = session.exec(select(Project)).all()
    logger.info(f"Returned {len(projects)} projects.")
    return projects

# Create project (admin only)
@app.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    logger.info(f"Admin {user.username} is creating a project: {project.name}")
    db_project = Project(name=project.name, description=project.description, user_id=user.id)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    logger.info(f"Project created: {db_project.name} (id: {db_project.id}) by admin {user.username}")
    return db_project

# Get single project (any authenticated user)
@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    logger.info(f"User {user.username} (role: {user.role}) requested project id {project_id}.")
    project = session.get(Project, project_id)
    if not project:
        logger.warning(f"Project id {project_id} not found.")
        raise HTTPException(status_code=404, detail="Project not found")
    logger.info(f"Project returned: {project.name} (id: {project.id})")
    return project

# Update project (admin only)
@app.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, project: ProjectCreate, session: Session = Depends(get_session), user: User = Depends(require_admin)):
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

# Delete project (admin only)
@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    logger.info(f"Admin {user.username} is deleting project id {project_id}.")
    db_project = session.get(Project, project_id)
    if not db_project:
        logger.warning(f"Delete failed: Project id {project_id} not found.")
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(db_project)
    session.commit()
    logger.info(f"Project deleted: id {project_id} by admin {user.username}")
    return None