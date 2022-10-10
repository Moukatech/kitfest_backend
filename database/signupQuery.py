from database.db import toreceiveNews, database
# from models.newsletterModel import newsLetterShema

async def addToNewsletterTable(payload):

    query = toreceiveNews.insert().values(email= payload.email)
    return await database.execute(query=query)

async def checkEmail(payload):
    query = toreceiveNews.select().where(payload.email == toreceiveNews.c.email)
    selected_user= await database.fetch_one(query=query)
    return selected_user

async def listAllEmails():
    query = toreceiveNews.select()
    data = await database.fetch_all(query = query)
    return data