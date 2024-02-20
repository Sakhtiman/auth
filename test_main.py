from fastapi.testclient import TestClient
from main import app
from database import engine, Base, SessionLocal
from models import User
from main import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Initialize the test client
client = TestClient(app)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define unit tests for the /register endpoint
def test_register_user():
    # Test registering a new user
    response = client.post(
        "/register?username=ss&password=123&scopes=user"
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

    # Check if the user is present in the database
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "testuser").first()
    db.close()
    assert user is not None

    # Test registering a user with an existing username
    response = client.post(
        "/register?username=test&password=test&scopes=user"
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


def test_login_for_access_token():
    # Attempt to log in with correct credentials
    login_response = client.post(
        "/token?username=kk&password=$2b$12$v.8IHVIHJDp5EbHyYjsyN.M906oQKYdpdD73nDSETw4uYLZPMUW.S&scope=admin"
    )
    print("Login response status code:", login_response.status_code)
    print("Login response content:", login_response.text)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"

    # Attempt to log in with incorrect password
    incorrect_password_response = client.post(
        "/token?username=testuser&password=incorrectpassword&scope=user"
    )
    assert incorrect_password_response.status_code == 400

    # Attempt to log in with incorrect username
    incorrect_username_response = client.post(
        "/token?username=nonexistentuser&password=testpassword&scope=user"
    )
    assert incorrect_username_response.status_code == 400

    # Attempt to log in with incorrect scope
    incorrect_scope_response = client.post(
        "/token?username=testuser&password=testpassword&scope=admin"
    )
    assert incorrect_scope_response.status_code == 400
