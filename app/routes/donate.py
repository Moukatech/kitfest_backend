from fastapi import APIRouter, FastAPI,Body,BackgroundTasks
from database.db import metadata, database, engine
from database.donateQueries import add_donation_query
from ..models.FormModels import *
from ..utilities.email import send_email_background, send_email_async

router = APIRouter(tags=["Donate"], prefix='/donate')
recipient= ["trust@kitfest.co.ke"]
@router.post("/create_donation_query")
async def createDonation(background_tasks: BackgroundTasks,donationData:DonateQuerySchema=Body(...)):
    await add_donation_query(donationData)
    send_email_background(background_tasks,donationData, "Donation Query",recipient)
    return {"Message": "Created a new donationQuery Suceessfully"}
