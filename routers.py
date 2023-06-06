import jwt
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials

from config import SECRET_KEY
from services import authenticate_employee, generate_token, verify_token
from database import employees

router = APIRouter()

@router.post("/get_token")
async def login(credentials: HTTPBasicCredentials):
    username = authenticate_employee(credentials)
    token = generate_token(username)
    return {"access_token": jwt.encode(token, SECRET_KEY, algorithm="HS256")}


@router.post("/salary")
async def get_salary(token: str = Depends(verify_token)):
    username = token["username"]
    return {
        "salary": employees[username]["salary"],
        "next_raise": employees[username]["next_raise"]
    }