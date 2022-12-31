from fastapi import APIRouter,File, UploadFile,Depends,Form
from ..models import FormModels
from database.application import *
from typing import List
import shutil
from database.crud_Users import *
import json
from ..utilities.email import *
import io

router = APIRouter(tags=["applications"], prefix="/applications")

@router.get("/get_user_data")
async def get_user_data(user:str =Depends(get_current_user)):
    if user is None:
        return {"Error": "token is expired"}
    user_details=await select_user_data(user.id)
    return user_details

@router.put("/update_personal_data")
async def update_user_data(personal_data: FormModels.PersonalInfomation,user:str =Depends(get_current_user)):
    await update_personal_info(personal_data,user)
    return {"Message": "User added successfully"}



@router.post("/performance_details")
async def performance_details(performance_data: FormModels.PerformaceDetails,user:str =Depends(get_current_user)):
    await add_performance_details(performance_data,user)
    return {"Message": "performance Details added successfully"}

@router.post("/technical_files_upload")
async def technical_files_upload(Performance_Links=Form(...),technical_rider_files:List[UploadFile]=File(...),user:str =Depends(get_current_user)):
    ###save files on project dir
    # for file in technical_rider_file:
    #     try:
    #         with open(file.filename, 'wb') as f:
    #             shutil.copyfileobj(file.file, f)
    #     except Exception:
    #         return {"message": "There was an error uploading the file(s)"}
    #     finally:
    #         file.file.close()

    # return {"message": f"Successfuly uploaded {[file.filename for file in technical_rider_file]}"}  
    #### save file to db##
    data =json.loads(Performance_Links)
    for file in technical_rider_files:
        pdfFile =await file.read()
        await upload_technical_rider_details(data,pdfFile,user)
        return {"Message": "Technical files added successfully"}


@router.post("/knowledge_sharing")
async def knowledge_sharing(trainer_profiles:List[UploadFile],KnowledgeSharingTopics=Form(),user:str =Depends(get_current_user)):
    
    data =json.loads(KnowledgeSharingTopics)
    for file in trainer_profiles:
        pdffile=await file.read()
        await create_Knowledge_Sharing_details(data,pdffile,user)
    return {"Message": "Profiles added successfully"}

@router.put("/add_notes")

async def add_notes(notes:FormModels.NotesScheme,user:str =Depends(get_current_user)):
    await update_notes(notes,user)
    return {"Message": "Added notes successfully"}

@router.get("/user_application_data")
async def user_application_data(user:str =Depends(get_current_user)):
    return await get_user_application_data(user)

@router.post("/send_email")
async def send_email(technical_rider_files:UploadFile= File(...),trainerProfile:UploadFile= File(...),user:str =Depends(get_current_user)):
    recipient= ["lewismocha@gmail.com","kitfest@kitfest.co.ke"]
    application_data= await get_user_application_data(user)
    technicalData= await select_technical_files(user)
    knowledgeData= await select_knowledge_files(user)
    apply_data  = {}
    for data in application_data:
        apply_data.update(data)
    
    for data in technicalData:
        apply_data.update(data)
    
    for data in knowledgeData:
        apply_data.update(data)
    await send_application_email(apply_data,technical_rider_files,trainerProfile,recipient)
    return  {"Message": "Email Sent successfully"}
