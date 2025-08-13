from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random
import time
import os

router = APIRouter()

otp_store = {}  # phone -> (otp, expiry)

class PhoneNumberInput(BaseModel):
    phone: str

class OTPVerifyInput(BaseModel):
    phone: str
    otp: str

@router.post("/send-otp")
def send_otp(data: PhoneNumberInput):
    otp = str(random.randint(100000, 999999))
    expiry = time.time() + int(os.getenv("OTP_EXPIRY", 300))
    otp_store[data.phone] = (otp, expiry)
    print(f"OTP for {data.phone} is {otp}")  # Dev only
    return {"message": "OTP sent successfully (check terminal)"}

@router.post("/verify-otp")
def verify_otp(data: OTPVerifyInput):
    stored = otp_store.get(data.phone)
    if not stored:
        raise HTTPException(status_code=400, detail="OTP not found")
    otp, expiry = stored
    if time.time() > expiry:
        raise HTTPException(status_code=400, detail="OTP expired")
    if otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"message": "OTP Verified. Login successful!"}
