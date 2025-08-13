from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routes import post
from auth import otp_auth

# Load .env
load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "FastAPI App"))

# Include routes
app.include_router(post.router, prefix="/api", tags=["Students"])
app.include_router(otp_auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI App"}
