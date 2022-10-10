from database.db import database,donatations
from app.models.FormModels import DonateQuerySchema

async def add_donation_query(payload:DonateQuerySchema):
    query =  donatations.insert().values(FirstName = payload.firstname,LastName=payload.lastname, 
                                         Email= payload.email,Message=payload.message,QueryType=payload.queryType)
    return await database.execute(query=query)