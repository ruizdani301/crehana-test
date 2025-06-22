from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.schemas import UserCreate, UserLogin, Token, CreatedUser
from infrastructure.db.database import get_db
from infrastructure.db import user_repository
from utils.jwt_handler import create_access_token

router_users = APIRouter(prefix="/users", tags=["Usuarios"])


@router_users.post("/register", response_model=CreatedUser)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.

    Args:
        user (UserCreate): User data (username and password).
        db (Session): Database session (Dependency injection).

    Returns:
        dict: Success message if the user is created.

    Raises:
        HTTPException (400): If the username already exists.
    """
    existing_user = user_repository.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user_repository.create_user(db, user.username, user.password)

    return {"message": "user created successfully"}


@router_users.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return an access token.

    Args:
        user (UserLogin): User credentials (username and password).
        db (Session): Database session (Dependency injection).

    Returns:
        Token: JWT access token (bearer type) for authenticated requests.

    Raises:
        HTTPException (401): If username or password is invalid.
    """
    db_user = user_repository.get_user_by_username(db, user.username)
    if not db_user or not user_repository.verify_password(
        user.password, db_user.password_hash
    ):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
