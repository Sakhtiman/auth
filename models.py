from sqlalchemy import Column, Enum, Integer, String,Boolean
from database import Base

class User(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    scopes = Column(Enum("admin", "user", name="user_scope"))  # Define predefined scope values

    def __init__(self, username: str, password: str, scopes: str):
        self.username = username
        self.password = password
        self.scopes = scopes


    
