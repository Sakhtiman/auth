from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
from auth import create_access_token, authenticate_user, get_password_hash
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register_user(username: str, password: str, scope: str = "basic", db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    password_hash = get_password_hash(password)

    user = User(username=username, password_hash=password_hash, scopes=scope)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}


@app.post("/token")
def login_for_access_token(username: str, password: str, scopes: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not authenticate_user(db, username, password, user.password_hash, scopes):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username, "scopes": scopes})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
