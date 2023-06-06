import jwt
from fastapi import APIRouter
from fastapi.security import HTTPBasicCredentials

from config import SECRET_KEY
from services import authenticate_employee, generate_token

router = APIRouter()

@router.post("/get_token")
async def login(credentials: HTTPBasicCredentials):
    username = authenticate_employee(credentials)
    token = generate_token(username)
    return {"access_token": jwt.encode(token, SECRET_KEY, algorithm="HS256")}