import os
from curses import meta
from databases import Database 

from sqlalchemy import (create_engine, MetaData, Column, String, DateTime,func, Table, Integer )
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

database = Database(database_url)