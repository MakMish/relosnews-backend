import redis
import aiosmtplib
from SRC.Utils.model import setting
from email.message import EmailMessage
from SRC.Utils.model import Setting
from datetime import datetime,UTC
mas=Setting()
r=redis.Redis.from_url(url=mas.redis_url)
async def sed(email: str, otp: int):
    # Check if OTP already exists in Redis
    if r.exists(email):
        return {"status": "already sent"}

    try:
            msg = EmailMessage()
            msg["Subject"] = "OTP Verification"
            msg["From"] = "newsrelos@gmail.com"
            msg["To"] = email

            msg.set_content(f"Your OTP is {otp}")
            a=datetime.now(UTC)
            await aiosmtplib.send(
                msg,
                hostname="smtp-relay.brevo.com",
                port=587,
                start_tls=True,
                username=setting.Login,
                password=setting.smtp_key,
                timeout=30,
            
            )
            b=datetime.now(UTC)
            print(f"{b-a}")
        
    except Exception as e:
        print(f"Brevo Error: {e}")
        return {"error": str(e)}
def verify2(email: str, otp: int):
    print(r.get(email))
    print(r.get(email))
    print("upar")
    stored_otp = r.get(email)
    if stored_otp is None:
        return 2   # expired
    
    if stored_otp == str(otp):
        return 0   # success
    
    return 1       # wrong otp

