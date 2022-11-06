from fastapi import APIRouter, FastAPI,Body,BackgroundTasks
from database.db import metadata, database, engine
from database.contactQuery import add_normal_query
from ..models.FormModels import *
from ..utilities.email import send_email_background, send_email_async

router = APIRouter(tags=["ContactUS"], prefix='/contactUs')
recipient= ["lewismocha@gmail.com"]
@router.post("/newQuery")
async def createContact(background_tasks: BackgroundTasks,contactData: NormalQuerySchema= Body(...)):
    await add_normal_query(contactData)
    ##add send email notification
    send_email_background(background_tasks,contactData, "Normal Query",recipient)
    return {"Message": "Created a normal query Suceessfully"}

