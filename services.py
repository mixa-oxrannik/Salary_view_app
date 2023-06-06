from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from database import employees



def authenticate_employee(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password
    if username not in employees or employees[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return username