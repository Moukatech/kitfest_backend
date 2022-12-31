from .db import users, database,personalData
from app.models import FormModels
from passlib.context import CryptContext
from app.auth import newAuth
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from jose import JWTError, jwt
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security import OAuth2PasswordBearer
import pytz

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # used to hash passwords

def hashPassword(password):
    return pwd_context.hash(password)

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(payload):
    hashed_Password=hashPassword(payload.password)
    fullName = payload.firstname +" "+ payload.lastname
    query =  users.insert().values(fullname = fullName, email= payload.email, password = hashed_Password)
    return await database.execute(query=query)

async def addUserInfo(payload):
    user=await check_user(payload)
    query =  personalData.insert().values(userID=user.id,FirstName=payload.firstname,LastName=payload.lastname, Email=payload.email, Country=payload.country, PhoneNumber=payload.phonenumber)
    return await database.execute(query=query)

async def check_user(user):
    
    query = users.select().where(user.email == users.c.email)
    selected_user= await database.fetch_one(query=query)
    
    return selected_user

async def check_admin(email):
    
    query = users.select().where(email == users.c.email)
    selected_user= await database.fetch_one(query=query)
    if selected_user is None:
        raise HTTPException(status_code=401, detail="Username not found")
    return FormModels.UserInDB(**selected_user)

async def authenticate_admin(username,password):
    # return await check_user(user_data)
    user= await check_admin(username)
    verify_password=pwd_context.verify(password, user.password)
    if user.email == username and  verify_password==True:
        return user
    return False   

async def authenticate_user(Payload):
    user= await check_user(Payload)
    verify_password=pwd_context.verify(Payload.password, user.password)
    if user.email == Payload.email and  verify_password==True:
        return user
    return False  
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = newAuth.decodeJWT(token)
        username: str = payload.get("sub")
        expires = payload.get("exp")
        if username is None:
            raise credentials_exception
        token_data = FormModels.TokenData(username=username,  expires=expires)
    except JWTError:
        return {"Error": "Could not authenticate_admin"}
    user = await check_admin(email=token_data.username)
    if user is None:
        # return {"Error": "Could not authenticate_admin"}
        raise credentials_exception
    if expires is None:
        raise credentials_exception
    if datetime.now(tz=pytz.utc) > token_data.expires:
        return {"Error": "token is expired"}
    return user


async def get_current_active_user(current_user: FormModels.UserSchema = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user