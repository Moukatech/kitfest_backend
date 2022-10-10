from database.db import database,normal_queries
from app.models.FormModels import NormalQuerySchema

async def add_normal_query(payload:NormalQuerySchema):
    query =  normal_queries.insert().values(FirstName = payload.firstname,LastName=payload.lastname, 
                                         Email= payload.email,Message=payload.message,QueryType=payload.queryType)
    return await database.execute(query=query)