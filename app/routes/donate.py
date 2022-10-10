from fastapi import APIRouter, FastAPI,Body
from database.db import metadata, database, engine
from database.donateQueries import add_donation_query
from ..models.FormModels import *

router = APIRouter(tags=["Donate"], prefix='/donate')

@router.post("/create_donation_query")
async def createDonation(donationData:DonateQuerySchema=Body(...)):
    await add_donation_query(donationData)
    return {"Message": "Create a new donationQuery Suceessfully"}
