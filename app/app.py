from fastapi import FastAPI,Body
from database.db import metadata, database, engine
from database.signupQuery import addToNewsletterTable, checkEmail,listAllEmails
from app.models.FormModels import newsLetterShema
from app.routes import contactUS,donate
from fastapi.middleware.cors import CORSMiddleware


metadata.create_all(engine)
app = FastAPI()
app.include_router(contactUS.router)
app.include_router(donate.router)

origins = [
    "http://127.0.0.1:5500",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def db_connect():
    await database.connect()

@app.on_event("shutdown")
async def close_connection():
    await database.disconnect()


@app.get("/", tags=["Home Page"])
async def homepage():
    return{"Message" : "Welcome We are awesome"}

@app.post("/signup", tags=["SignUpfestiveNews"])
async def receiveNews(email: newsLetterShema= Body(...)):
    newemail = await checkEmail(email)
    if newemail:
        return {"Message" : "Email aleady exists"}
    await addToNewsletterTable(email)
    return {"Message" : "signup successful"}

@app.get("/get_email", tags=["GetEmail"])
async def get_email():
    userEmail= await listAllEmails()
    return {"List": userEmail}