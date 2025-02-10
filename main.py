# main.py
from fastapi import FastAPI
from api.api_routes import router as api_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

app.include_router(api_router)