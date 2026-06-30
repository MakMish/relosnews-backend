import smtplib
import redis
from SRC.Utils.model import setting
from fastapi.responses import JSONResponse
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
        # Email setup
        msg = EmailMessage()
        msg['Subject'] = "OTP Verification"
        msg['From'] = "newsrelos@gmail.com"  # Verify ye email Brevo mein "Sender" domain mein added ho
        msg['To'] = email
        msg.set_content(f"Hello, your OTP for Relos News is: {otp}")
        a= datetime.now(UTC)
        # SMTP Connection to Brevo
        print("1")
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        print("2")
        server.starttls()
        print("3")
        server.login(setting.Login, setting.smtp_key) 
        print("4")
        server.send_message(msg)
        print("5")
        server.quit()
        print("6")
        # Redis set
        b=datetime.now(UTC)
        print(f'///// yeh rha \n {b-a}')
        r.setex(email, 60, otp)
        return {"status": "sent"}
        
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

