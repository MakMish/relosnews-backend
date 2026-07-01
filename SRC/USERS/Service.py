from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Request
from sqlalchemy import select
import redis
from fastapi.responses import JSONResponse
from SRC.USERS.Schemas import User
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from SRC.USERS.Models import register,login
from SRC.Utils.verify import sed,verify2
import redis
from SRC.Utils.model import setting
r=redis.Redis.from_url(setting.redis_url,decode_responses=True)
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
async def gets(data: login, dba: AsyncSession):
    try:
        v=await dba.execute(select(User).where(User.email==data.emai))
        reslt=v.scalars().first()
        if reslt is None:
            return JSONResponse(
                status_code=419,
                content={
                    "status":"invalid"
                }
            )
        return {
        "id": reslt.id,
        "name": reslt.name,
        "email":reslt.email
         }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status":f"error is diff , {e}"
            }
        )
        
 

async def ver(request1:Request,data:register,otp:int,dba:AsyncSession):
    try:
        print("1")
        v=verify2(request=request1,otp=otp)
        print("1")
        if v==2:
            raise HTTPException(status_code=410, detail="OTP expired") 
        elif v==0:
            d=User(
                name=data.name,
                email=data.emai,
                hash_pass=pwd_context.hash(data.password)
                )
            dba.add(d)
            await dba.commit()
            await dba.refresh(d)
            return {
                "status": "success"
            }
        else:
            print(v)
            print("uoarr wala")
            raise HTTPException(status_code=408, detail="OTP invalid")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=434, detail="incorrect")
    

