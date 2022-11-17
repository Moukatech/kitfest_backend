from fastapi import APIRouter, HTTPException, Body, Depends
from database.crud_Users import *
from ..models import FormModels
from ..auth import auth_hundler, auth_bearer, newAuth
from datetime import datetime, timedelta
import base64

from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.responses import RedirectResponse, Response, JSONResponse
from starlette.requests import Request


router = APIRouter(tags=["Users"], prefix="/user")
basic_auth = newAuth.BasicAuth(auto_error=False)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
@router.post("/add_user",dependencies=[Depends(auth_bearer.JWTBearer())])
async def add_new_user(userData: FormModels.UserSchema):
    add= await create_user(userData)
    return {"Message": "User added successfully"}

@router.post("/login")
async def user_login(user:FormModels.UserLoginSchema):
    # userData = await check_login(user)
    # return  userData
    if await authenticate_user(user):
        return auth_hundler.signJWT(user.email)
    return{
        "Error": "Wrong login credentials"
    }

@router.post("/token", response_model=FormModels.Token)
async def route_login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = newAuth.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain="127.0.0.1")
    return response


@router.get("/login_basic")
async def login_basic(auth: newAuth.BasicAuth = Depends(basic_auth)):
    if not auth:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response

    try:
        decoded = base64.b64decode(auth).decode("ascii")
        username, _, password = decoded.partition(":")
        user = await authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = newAuth.create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        token = jsonable_encoder(access_token)

        response = RedirectResponse(url="/docs")
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            domain="127.0.0.1",
            httponly=True,
            max_age=1800,
            expires=1800,
        )
        return response

    except:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response
