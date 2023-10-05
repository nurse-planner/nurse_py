from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import JsonParser
import NurseDao

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.post("/")
async def service(request: Request):
    nursesDataString = await request.body()
    nursesDataJson = JsonParser.getJson(nursesDataString)
    nurseDto = JsonParser.getValues(nursesDataJson)
    result = NurseDao.nurse_scheduling(nurseDto)
    return result
