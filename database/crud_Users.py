from .db import users, database
from app.models import FormModels
from passlib.context import CryptContext
from app.auth import newAuth

from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

oauth2_scheme = newAuth.OAuth2PasswordBearerCookie(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # used to hash passwords

async def create_user(payload):
    hash_password=pwd_context.hash(payload.password)
    query =  users.insert().values(fullname = payload.fullname, email= payload.email, password = hash_password)
    return await database.execute(query=query)

async def check_user(user):
    
    query = users.select().where(user.email == users.c.email)
    selected_user= await database.fetch_one(query=query)
    
    return {"data":selected_user}

async def authenticate_user(email,password):
    # return await check_user(user_data)
    user= await check_user(email)
    verify_password=pwd_context.verify(password, user.password)
    if user.email == email and  verify_password==True:
        return user
    return False   

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = newAuth.decodeJWT(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = FormModels.TokenData(email=username)
    except PyJWTError:
        raise credentials_exception
    user = check_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: FormModels.UserSchema = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user