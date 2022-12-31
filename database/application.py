from .db import database,performanceDetails,TechnicalRiderFiles,KnowledgeSharing,personalData
import psycopg2
from sqlalchemy.sql import select
from io import BytesIO
import base64

async def add_performance_details(perfomanceData,current_user):
    query =  performanceDetails.insert().values(userID=current_user.id,companyName=perfomanceData.company_name,socialHandles=perfomanceData.social_media_handles, performanceTitle=perfomanceData.performace_title, synopsis=perfomanceData.synopsis, performanceDuration=perfomanceData.performace_duration,
                                                performancetype=perfomanceData.performace_type,performancelanguage=perfomanceData.performace_language,audienceType=perfomanceData.appropriate_audience,setupTime=perfomanceData.setup_time,takeDownTime=perfomanceData.take_Down_time,
                                                stageSpace=perfomanceData.stage_space,numberOfperformers=perfomanceData.numberOfperfomers,intermissionDuration = perfomanceData.intermissionDuration)
    return await database.execute(query=query)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with BytesIO(filename) as file:
        blobData = file.read()
    return blobData

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(f"{filename}", 'wb') as file:
        pdffile=file.write(data)
    return pdffile

async def upload_technical_rider_details(payload,file,current_user):
    pdfFile = convertToBinaryData(file)
    query =  TechnicalRiderFiles.insert().values(userID=current_user.id,imagesLink=payload.get("performance_Images"),videoLinks=payload.get("performance_Videos"),filesData= pdfFile)
    return await database.execute(query=query)

async def create_Knowledge_Sharing_details(payload,files,current_user):
    pdfFile = convertToBinaryData(files)
    query =  KnowledgeSharing.insert().values(userID=current_user.id,Topics=payload.get("topics"), TrainerProfiles= pdfFile)
    return await database.execute(query=query)


async def update_personal_info(payload,current_user):
    query = (personalData.update().where(current_user.id == personalData.c.userID).values(role =payload.role,county=payload.county))
    return await database.execute(query=query)

async def select_user_data(user_id):
    query = personalData.select().where(user_id == personalData.c.userID)
    return await database.fetch_one(query=query)

async def update_notes(payload,current_user):
    query = performanceDetails.update().where(current_user.id == performanceDetails.c.userID).values(Notes=payload.notes, acceptedTerms=payload.terms)
    return await database.execute(query=query)

async def get_user_application_data(current_user):
    query = select(personalData,performanceDetails).where(current_user.id == personalData.c.userID)
    data=await database.fetch_all(query=query)
    return data

async def select_technical_files(current_user):
    query = select(TechnicalRiderFiles.c.imagesLink,TechnicalRiderFiles.c.videoLinks).where(current_user.id == TechnicalRiderFiles.c.userID)
    data = await database.fetch_all(query=query)
    return data
    
async def select_knowledge_files(current_user):
    query = select(KnowledgeSharing.c.Topics).where(current_user.id == KnowledgeSharing.c.userID)
    data = await database.fetch_all(query=query)
    return data
    