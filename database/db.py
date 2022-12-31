import os
from curses import meta
from databases import Database 

from sqlalchemy import (create_engine, MetaData, Column, String, DateTime,func, Table, Integer,LargeBinary,ForeignKey )
from sqlalchemy.sql import func

database_url = "postgresql://mocha:Nyangau92@localhost:5432/kitfest"
# database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(database_url)
metadata = MetaData()



toreceiveNews = Table(
    "receiveNews",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

normal_queries = Table(
    "normal_queries",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("FirstName", String(50)),
    Column("LastName", String(50)),
    Column("Email", String(50)),
    Column("QueryType", String(50)),
    Column("Message", String(500)),
    Column("Query_date", DateTime, default=func.now(), nullable=False),
)

donatations = Table(
    "donatations_Query",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("FirstName", String(50)),
    Column("LastName", String(50)),
    Column("Email", String(50)),
    Column("QueryType", String(50)),
    Column("Message", String(500)),
    Column("Query_date", DateTime, default=func.now(), nullable=False),
)
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("fullname", String(50)),
    Column("email", String(50)),
    Column("password", String(250)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

personalData = Table(
    "personalData",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("userID", Integer,ForeignKey("users.id")),
    Column("FirstName", String(50)),
    Column("LastName", String(50)),
    Column("Email", String(50)),
    Column("Country", String(50)),
    Column("PhoneNumber", String(50)),
    Column("role", String(250)),
    Column("county", String(250)),
    Column("DateCreated", DateTime, default=func.now(), nullable=False),
)
performanceDetails = Table(
    "performanceDetails",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("userID", Integer,ForeignKey("users.id")),
    Column("companyName", String(250)),
    Column("socialHandles", String(500)),
    Column("performanceTitle", String(250)),
    Column("synopsis", String(1000)),
    Column("performanceDuration", Integer()),
    Column("performancetype", String(250)),
    Column("performancelanguage", String(50)),
    Column("audienceType", String(250)),
    Column("setupTime", Integer()),
    Column("takeDownTime", Integer()),
    Column("stageSpace", String(250)),
    Column("numberOfperformers", Integer()),
    Column("intermissionDuration", Integer()),
    Column("Notes", String(1000)),
    Column("acceptedTerms", String(50)),
    Column("DateCreated", DateTime, default=func.now(), nullable=False),
)
TechnicalRiderFiles = Table(
    "TechnicalRiderFiles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("userID", Integer,ForeignKey("users.id")),
    Column("imagesLink", String(500)),
    Column("videoLinks", String(500)),
    Column("filesData", LargeBinary(10000000)),
    Column("DateCreated", DateTime, default=func.now(), nullable=False)
)

KnowledgeSharing = Table(
    "KnowledgeSharing",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("userID", Integer,ForeignKey("users.id")),
    Column("Topics", String(250)),
    Column("TrainerProfiles", LargeBinary(10000000)),
    Column("DateCreated", DateTime, default=func.now(), nullable=False)
)

database = Database(database_url)