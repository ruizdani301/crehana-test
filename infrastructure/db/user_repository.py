from passlib.context import CryptContext
from sqlalchemy.orm import Session
from infrastructure.db.models import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def create_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = UserModel(username=username, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
