from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, Request, status
from pydantic import BaseModel, HttpUrl, validator
import requests
from typing import Optional
import os
from dotenv import load_dotenv

class APIRequest(BaseModel):
    url: HttpUrl
    navigation_goal: str
    data_extraction_goal: str
    webhook_callback_url: str
    navigation_payload: Optional[dict] = None

    @validator('navigation_payload')
    def validate_navigation_payload(cls, value):
        if value is None:
            return value
        if not isinstance(value, dict):
            raise ValueError('navigation_payload must be a dictionary')
        return value

def api_key_auth(request: Request) -> None:
    load_dotenv() 
    #TODO: switch to JWT authorization
    access_key_required = os.environ["GEENUITY_ACCESS_KEY_REQUIRED"]
    secret_key_required = os.environ["GEENUITY_SECRET_KEY_REQUIRED"]
    access_key = request.headers.get("access_key")
    secret_key = request.headers.get("secret_key")
    if access_key != access_key_required or secret_key != secret_key_required:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden, access prohibited.")

skyvern_app = FastAPI(dependencies=[Depends(api_key_auth)])

@skyvern_app.get("/")
async def getStatus():
    return {"response":"Welcome to geenuity-skyvern-api"}

@skyvern_app.post('/skyvern-api')
async def defineTask(request: APIRequest):
    load_dotenv()
    url = os.environ["GEENUITY_API_URL"]
    x_api_key = os.environ['SKYVERN_API_KEY']
    headers = {
    'Content-Type': 'application/json',
    'x-api-key': x_api_key,
    }   

    headers["Accept"] = "application/json"
    response = requests.post(url, headers=headers, json=request.dict())
    print(response)
    if response.status_code == 200:
        print("Task created successfully")
        return response.json()        
    else:
        return f"Error: {response.status} - {response.text()}"    
    
@skyvern_app.get('/skyvern-api/{taskid}')
async def getTaskResult(taskid: str):
    load_dotenv()
    url = os.environ["GEENUITY_API_URL"]
    x_api_key = os.environ['SKYVERN_API_KEY']
    headers = {
    'x-api-key': x_api_key,
    }
    response = requests.get(url+str(taskid), headers = headers) 
    return response.json()