
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
    
    