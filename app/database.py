from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://<username>:<password>@<host>:<port>/<database>")
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session