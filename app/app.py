from fastapi import FastAPI,Body,Response, Request,Depends,HTTPException, status
from database.db import metadata, database, engine
from database.signupQuery import addToNewsletterTable, checkEmail,listAllEmails
from database import crud_Users
from app.models import FormModels
from app.routes import contactUS,donate,users
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html,get_redoc_html
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.utils import get_openapi
from starlette.responses import Response, JSONResponse
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import secrets
from datetime import datetime, timedelta
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

app = FastAPI(
    title="FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url = None,
)

app.include_router(contactUS.router)
app.include_router(donate.router)
app.include_router(users.router)

security = HTTPBasic()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def docs_access(credentials:  HTTPBasicCredentials = Depends(security)):
    user = crud_Users.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.on_event("startup")
async def db_connect():
    await database.connect()

@app.on_event("shutdown")
async def close_connection():
    await database.disconnect()


@app.get("/", tags=["Home Page"])
async def homepage():
    return{"Message" : "Welcome We are awesome"}

# current_user: FormModels.UserSchema = Depends(crud_Users.get_current_active_user)
@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(docs_access)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(docs_access)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(docs_access)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

@app.post("/signup", tags=["SignUpfestiveNews"])
async def receiveNews(email: FormModels.newsLetterShema= Body(...)):
    newemail = await checkEmail(email)
    if newemail:
        return {"Message" : "Email aleady exists"}
    await addToNewsletterTable(email)
    return {"Message" : "signup successful"}

@app.get("/get_email", tags=["GetEmail"])
async def get_email():
    userEmail= await listAllEmails()
    return {"List": userEmail}
