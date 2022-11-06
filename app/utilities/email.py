import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv


emailTemplate = os.path.join(os.path.dirname(__file__), '.', 'templates')
credentials =load_dotenv('.env')
conf = ConnectionConfig(
    MAIL_USERNAME= os.getenv('Email'),
    MAIL_PASSWORD= os.getenv("password"),
    MAIL_FROM= "kitfest@kitfest.co.ke",
    MAIL_PORT= 587,
    MAIL_SERVER= "smtp.gmail.com",
    MAIL_FROM_NAME= "Kitfest Inquery",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    
)

async def send_email_async(email):
    recipient= ["lacreme.ke@gmail.com"]
    html = f"""
    <html>
    <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
    <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
     <div style="margin: 0 auto; width: 90%; text-align: center;">
        <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">KitFest Queries</h1>
        <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
         <h3 style="margin-bottom: 100px; font-size: 24px;">Donation Inqury</h3>
        <p style="margin-bottom: 30px;">A new Inqury has been sent</p>
        <p>Name: {email.firstname} {email.lastname}</p>
        <p>Email: {email.email}</p>
        <p>QueryType: {email.queryType}</p>
        <p>Description: {email.message}</p>
      </a>
    </div>
    </div>
    </div>
    </body>
    </html>
    """
    message = MessageSchema(
        subject="KitFest Inquries",
        recipients=recipient,
        html=html,
        subtype="html")

    fm = FastMail(conf)

    await fm.send_message(message)


def send_email_background(background_tasks: BackgroundTasks, email,subject,recipient):
    html = f"""
    <html>
    <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
    <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
     <div style="margin: 0 auto; width: 90%; text-align: center;">
        <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">KitFest Queries</h1>
        <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
         <h3 style="margin-bottom: 100px; font-size: 24px;">{subject}</h3>
        <p style="margin-bottom: 30px;">A New Inqury has been sent.Below are the details.</p>
        <p>Name: {email.firstname} {email.lastname}</p>
        <p>Email: {email.email}</p>
        <p>Query Type: {email.queryType}</p>
        <p>Description: {email.message}</p>
      </a>
    </div>
    </div>
    </div>
    </body>
    </html>
    """
    message = MessageSchema(
        subject="KitFest Inquries",
        recipients=recipient,
        html=html,
        subtype="html")

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)