from fastapi import FastAPI,Body,Response, Request
from database.db import metadata, database, engine
from database.signupQuery import addToNewsletterTable, checkEmail,listAllEmails
from app.models.FormModels import newsLetterShema
from app.routes import contactUS,donate
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:5500",
    "https://kitfest.co.ke",
    "https://kitfest.co.ke/",
]

# middleware = [
#     Middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_methods=['*'],
#         allow_headers=['*']
#     )
# ]

metadata.create_all(engine)
app = FastAPI()
app.include_router(contactUS.router)
app.include_router(donate.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.middleware("http")
# async def allowAllDomains(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     return response

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