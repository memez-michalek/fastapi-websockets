from fastapi import APIRouter, HTTPException, WebSocket
from models import modelHandler
from handlers import handle
from typing import List
router = APIRouter()


@router.post("/login", response_model=modelHandler.UserOut)
async def login_user(login :modelHandler.UserIn):
    result = handle.LoginUser(login)
    if result[0] != True:
        raise HTTPException(status_code=result[2], detail=result[1])
    print(result)
    response = modelHandler.UserOut(ID=result[1] ,username=login.username, email=login.email)
    return response

@router.post("/register", response_model=modelHandler.UserOut)
async def register_user(register: modelHandler.UserIn):
    result = handle.RegisterUser(register)
    if result[0] == False:
        raise HTTPException(status_code=result[2], detail=result[1])
    print(result)
    response = modelHandler.UserOut(ID=result[1] ,username=register.username, email=register.email)
    print(response)
    return response


