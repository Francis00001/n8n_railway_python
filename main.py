from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡FastAPI está corriendo en Railway!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/data")
async def receive_data(request: Request):
    data = await request.json()
    return {"received_data": data}

