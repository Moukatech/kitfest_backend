import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile



emailTemplate = os.path.join(os.path.dirname(__file__), '.', 'templates')
credentials =load_dotenv('.env')
conf = ConnectionConfig(
    MAIL_USERNAME= os.getenv('Email'),
    MAIL_PASSWORD= os.getenv("password"),
    MAIL_FROM= "kitfest@kitfest.co.ke",
    MAIL_PORT= 587,
    MAIL_SERVER= "smtp.gmail.com",
    MAIL_FROM_NAME= "New Application",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    
)

async def send_application_email(user_data,technical_rider_files,trainerProfile,recipient):
    html = f"""
    <html>
        <body style="margin-left: auto;
                    margin-right: auto;
                    margin-top: 22px;
                    margin-bottom: 22px;
                    padding: 0;
                    box-sizing: inherit;
                    font-family: "Montserrat", sans-serif;
                    background-color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 80vw;" >
            <div>
                <div style= "background-color: #037a0b;
                    color: white;
                    padding: 12px 12px 12px 12px; border-radius: 6px;
                    font-size: 1rem;"class="title">
                    <h1>New application for #KITFest2023 from <br>{user_data.get("companyName")} - {user_data.get("Country")}</h1>
                </div>
                <hr>
                <h2 style="color: #8E0000">PERSONAL DETAILS</h2>
                <div>First Name</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("FirstName")}</div>
                <div>Last Name</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("LastName")}</div>
                <div>Email</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("Email")}</div>
                <div>Phone Number</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("PhoneNumber")}</div>
                <div>Role in Organisation</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("role")}</div>
                <div>Country</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("Country")}</div>
                <div>County (Kenyans)</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("county")}</div>
                <hr>
                <h2 style="color: #8E0000;">PERFORMANCE DETAILS</h2>
                <div>Company Name</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"class="datapreview">{user_data.get("companyName")}</div>
                <div>Performance Title</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("performanceTitle")}</div>
                <div>Number of Performers</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("numberOfperformers")}</div>
                <div>Synopsis</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;"  class="datapreview">{user_data.get("synopsis")}</div>
                <div>Performance Type</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("performancetype")}</div>
                <div>Performance Duration</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("performanceDuration")}</div>
                <div>Intermission Duration</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("intermissionDuration")}</div>
                <div>Performance Language</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("performancelanguage")}</div>
                <div>Technical Rider: Check attachments</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{technical_rider_files.filename}</div>
                <div>Technical Rehearsal & Setup Time</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("setupTime")}</div>
                <div>Take Down Time</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("takeDownTime")}</div>
                <div>Required Stage Space</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("stageSpace")}</div>
                <div>Audience Type</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("audienceType")}</div>
                <div>Social Media Handles</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("socialHandles")}</div>
                <div>Performance Images (link)</div>
                <div  style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("imagesLink")}</div>
                <div>Performance Video (link)</div>
                <div  style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("videoLinks")}</div>
                <hr>
                <h2 style="color: #8E0000;">AVAILABLE WORKSHOPS & TRAINING SKILL SET</h2>
                <div>Knowledge Sharing Topics</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("Topics")}</div>
                <div>Trainer Profile(s) if available: Check attachments</div>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{trainerProfile.filename}</div>
                <hr>
                <h2 style="color: #8E0000;">NOTES</h2>
                <div style="background-color: rgb(223, 223, 223);
                    border: 0.5px solid rgb(188, 188, 188);
                    padding: 6px;
                    margin-top: 6px;
                    margin-bottom: 6px;
                    border-radius: 4px;" class="datapreview">{user_data.get("Notes")}</div>
                <hr>
                <br><br>
        </body>

        </html> techRider.pdf
    """
    # with open(f"{filename}", 'rb') as f:
    #     data = f.file
    #     file_name= f.name
    #     print(data)
    #     print(file_name)
    # file1= open(f"{filename}", 'rb')
    # upload_file = UploadFile(filename=file_name, file=data, content_type="application/pdf")
    message = MessageSchema(
        subject="Application #KITFest2023",
        recipients=recipient,
        html=html,
        subtype="html",
        attachments=[technical_rider_files,trainerProfile])

    fm = FastMail(conf)

    await fm.send_message(message)

async def send_email_async(email,subject,recipient):
    html = f"""
    <html>
    <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
    <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
     <div style="margin: 0 auto; width: 90%; text-align: center;">
        <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">KITFest Queries</h1>
        <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
         <h3 style="margin-bottom: 100px; font-size: 24px;">{subject}</h3>
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
        subject="KITFest Inquiries",
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