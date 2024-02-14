from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError,jwt
# import python_jwt as jwt
from typing import Optional
from sqlalchemy.orm import Session
from models import User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
        token_data = {"username": username, "scopes": payload.get("scopes")}
    except JWTError:
        return None
    return token_data

def authenticate_user(db: Session, username: str, password: str, password_hash: str, scope: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False  # User does not exist
    if user.is_active:
        # Check if the provided password matches the hashed password
        if pwd_context.verify(password, password_hash):
            # Check if the provided scope matches the user's scope
            if user.scopes == scope:
                return True
            else:
                return False  # Scope mismatch
        elif password == user.password_hash:
            # Check if the provided scope matches the user's scope
            if user.scope == scope:
                return True
            else:
                return False  # Scope mismatch
    return False
