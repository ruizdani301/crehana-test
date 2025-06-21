from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.schemas import UserCreate, UserLogin, Token, CreatedUser
from infrastructure.db.database import get_db
from infrastructure.db import user_repository
from utils.jwt_handler import create_access_token

router_users = APIRouter(prefix="/users", tags=["Usuarios"])

@router_users.post("/register", response_model=CreatedUser)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_repository.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    user_repository.create_user(db, user.username, user.password)
    
    return {"message":"Se ha creado existosamente"}

@router_users.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_repository.get_user_by_username(db, user.username)
    if not db_user or not user_repository.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
