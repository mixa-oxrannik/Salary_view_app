from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials

from database import employees
from config import SECRET_KEY


def generate_token(username: str):
    expiration_time = str(datetime.utcnow() + timedelta(minutes=20))  # токен действует 20 минут
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
    if not token:
        raise HTTPException(status_code=400, detail="Token is missing")
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_token["username"] != username:
            raise HTTPException(status_code=401, detail="Invalid token")
        if datetime.fromisoformat(decoded_token["expires"]) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return decoded_token
