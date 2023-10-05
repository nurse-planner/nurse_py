from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
import JsonParser
import NurseDao

app = FastAPI()


@app.post("/")
async def service(request: Request):
    nursesDataString = await request.body()
    nursesDataJson = JsonParser.getJson(nursesDataString)
    nurseDto = JsonParser.getValues(nursesDataJson)
    result = NurseDao.nurse_scheduling(nurseDto)
    return result
