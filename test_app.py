from datetime import datetime, timedelta

import jwt
from starlette.testclient import TestClient

from main import app
from services import generate_token
from config import SECRET_KEY

client = TestClient(app)


# Тестирование метода get_token на получения токена при корректных данных
def test_authenticate_employee():
    credentials = {"username": "alice", "password": "password123"}
    response = client.post("/get_token", json=credentials)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"]


# Проверка работы метода get_token при неправельном пароле
def test_authenticate_employee_with_wrong_password():
    credentials = {"username": "alice", "password": "wrongpassword"}
    response = client.post("/get_token", json=credentials)
    assert response.status_code == 401
    assert "detail" in response.json()


# Проверка метода salary при корректных данных
def test_verify_token():
    username = "alice"
    token = jwt.encode(
        {"username": username, "expires": str(datetime.utcnow() + timedelta(minutes=30))},
        SECRET_KEY,
        algorithm="HS256"
    )
    response = client.post("/salary", json={"name": "alice", "password": "password123", "token": token})
    assert response.status_code == 200
    assert "salary" in response.json()
    assert "next_raise" in response.json()


# Проверка для невалидного токена
def test_user_authentication():
    data = generate_token("alice")
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    response = client.post("/salary", json={"name": "alice", "password": "password123",
                                            "token": token + "123"
                                            })  # прибавляем к верному токену строку
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
