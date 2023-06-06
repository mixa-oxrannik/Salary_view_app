from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials

from database import employees
from config import SECRET_KEY

def generate_token(username: str):
    expiration_time = str(datetime.utcnow() + timedelta(minutes=30)) # токен действует 30 минут
    print(expiration_time)
    token = {"username": username, "expires": expiration_time}
    return token


def authenticate_employee(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password
    if username not in employees or employees[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return username


def verify_token(token: Optional[str] = None, username: Optional[str] = Depends(authenticate_employee)):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    return decoded_token