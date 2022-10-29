from fastapi import APIRouter, FastAPI,Body
from database.db import metadata, database, engine
from database.contactQuery import add_normal_query
from ..models.FormModels import *

router = APIRouter(tags=["ContactUS"], prefix='/contactUs')

@router.post("/newQuery")
async def createContact(contactData: NormalQuerySchema= Body(...)):
    await add_normal_query(contactData)
    ##add send email notification
    return {"Message": "Create a normal query Suceessfully"}

