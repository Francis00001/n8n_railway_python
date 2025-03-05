from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡FastAPI está corriendo en Railway!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}
