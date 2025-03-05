from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DataInput(BaseModel):
    name: str
    message: str

@app.post("/data")
async def receive_data(data: DataInput):
    return {"received_data": data}

