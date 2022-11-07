from fastapi import APIRouter, FastAPI,Body,BackgroundTasks
from database.db import metadata, database, engine
from database.donateQueries import add_donation_query
from ..models.FormModels import *
from ..utilities.email import send_email_background, send_email_async

router = APIRouter(tags=["Donate"], prefix='/donate')
recipient= ["trust@kitfest.com","lacreme.ke@gmail.com",]
@router.post("/create_donation_query")
async def createDonation(donationData:DonateQuerySchema=Body(...)):
    await add_donation_query(donationData)
    send_email_async(donationData, "Donation Query",recipient)
    return {"Message": "Created a new donationQuery Suceessfully"}
