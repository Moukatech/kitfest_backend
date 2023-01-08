
from email import message
from pydantic import BaseModel, EmailStr, Field,SecretStr
from typing import List, Optional
from datetime import datetime
from fastapi import File, UploadFile

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
    password : SecretStr = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    expires: Optional[datetime]

class UserInDB(UserSchema):
    id: int
    password: str

class PersonalInfomation(BaseModel):
    firstname : str = Field(...)
    lastname : str= Field(...)
    email : EmailStr = Field(...)
    country : str = Field(...)
    phonenumber: str= Field(...)
    role: str = Field(...)
    county: str = Field(...)

class RegistrationSchema(BaseModel):
    firstname : str = Field(...)
    lastname : str= Field(...)
    email : EmailStr = Field(...)
    country : str = Field(...)
    phonenumber: str= Field(...)
    password : str= Field(...)

class PerformaceDetails(BaseModel):
    company_name: str = Field(...)
    social_media_handles: str = Field(...)
    performace_title: str = Field(...)
    synopsis: str = Field(...)
    performace_duration: int = Field(...)
    performace_type: str = Field(...)
    performace_language: str = Field(...)
    appropriate_audience: str = Field(...)
    setup_time:int = Field(...)
    take_Down_time:int= Field(...)
    stage_space: str = Field(...)
    numberOfperfomers :int = Field(...)
    intermissionDuration: int | None = Field(...)

class FileUpload(BaseModel):
    file: UploadFile = File(...)

class PerformanceLinks(BaseModel):
    performance_Images : str = Field(...)
    performance_Videos : str = Field(...)

class NotesScheme(BaseModel):
    notes :str | None = Field(...)
    terms : str = Field(...)
    

