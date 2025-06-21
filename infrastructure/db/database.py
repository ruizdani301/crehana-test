from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# URL de la base de datos (SQLite en archivo local)
DATABASE_URL = "sqlite:///./todo_app.db"

# Configuración del engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # solo para SQLite
)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa (usada en models.py)
Base = declarative_base()

# Función que se inyecta como dependencia en FastAPI
# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()