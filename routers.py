from fastapi.security import HTTPBasicCredentials

from services import authenticate_employee
from fastapi import APIRouter


router = APIRouter()

@router.post("/login")
async def login(credentials: HTTPBasicCredentials):
    username = authenticate_employee(credentials)
    return username