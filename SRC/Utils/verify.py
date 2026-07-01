import redis
from fastapi import HTTPException
from fastapi import Request
from SRC.Utils.model import setting
from email.message import EmailMessage
from SRC.Utils.model import Setting
from datetime import datetime,UTC
import httpx
mas=Setting()
r=redis.Redis.from_url(url=mas.redis_url,decode_responses=True)

async def sed(request:Request,email: str, otp: int):
    if r.exists(email):
        raise HTTPException(status_code=409,detail="already sent")

    # Brevo API Endpoint
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": setting.smtp_key, 
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"email": "newsrelos@gmail.com", "name": "relos"},
        "to": [{"email": email}],
        "subject": "OTP Verification",
        "htmlContent": f"<p>Your OTP is <strong>{otp}</strong></p>"
    }
    a=datetime.now(UTC)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
        if response.status_code in [200, 201, 202]:
            r.setex(name=request.client.host,value=otp,time=60)
            print(f"Email sent successfully via HTTP API and \n {r.get(email)}")
            b=datetime.now(UTC)
            print(f"///here///\n {b-a}")
            return {"status": "sent"}
        else:
            print(f"Brevo API Error: {response.status_code} - {response.text}")
            return {"error": response.text}
            
    except Exception as e:
        print(f"Network Error: {e}")
        return {"error": str(e)}

def verify2(request:Request, otp: int):
    try:
        print("upar")
        print("redis mein gya hai")
        stored_otp = r.get(request.client.host)
        print("redis mein gya hai")
        if stored_otp is None:
            return 2   # expired
        
        if stored_otp == str(otp):
            return 0   # success
        
        return 1 
    except Exception as e:
        print(f"{e}")      # wrong otp

