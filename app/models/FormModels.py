
from email import message
from pydantic import BaseModel, EmailStr, Field

class newsLetterShema(BaseModel):
    email : EmailStr =Field(...)

class DonateQuerySchema(BaseModel):
    firstname : str = Field(...)
    lastname : str= Field(...)
    email : EmailStr = Field(...)
    queryType:str= Field(...)
    message: str = Field(...)

class NormalQuerySchema(BaseModel):
    firstname : str = Field(...)
    lastname : str= Field(...)
    email : EmailStr = Field(...)
    queryType:str= Field(...)
    message: str = Field(...)

class UserLoginSchema(BaseModel):
    email : EmailStr =Field(...)
    password : str = Field(...)

class UserEmailschema(BaseModel):
    email : EmailStr =Field(...)
    
class UserSchema(BaseModel):
    fullname: str = Field(...)
    email : EmailStr =Field(...)
    password : str = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None

class UserInDB(UserSchema):
    password: str