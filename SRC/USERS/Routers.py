from fastapi import APIRouter,Depends,BackgroundTasks,HTTPException
import random
from passlib.context import CryptContext
import redis
from fastapi.responses import JSONResponse
from SRC.Utils.verify import sed
from SRC.Utils.model import setting
from sqlalchemy.ext.asyncio import AsyncSession
from SRC.USERS.Models import user,register,login
from SRC.Utils.verify import sed
from SRC.Utils.dbutils import get_db
from SRC.USERS.Service import gets,ver
from SRC.USERS.Schemas import User
router=APIRouter(prefix="/users")
r=redis.Redis.from_url(url=setting.redis_url)
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


@router.post("/register")
async def gets2(data:register,dba:AsyncSession=Depends(get_db),bgts:BackgroundTasks=BackgroundTasks()):
    x=r.get(f"{data.emai}")
    print("1")
    if x is None:
        print("2")
        try:
                d=User(
                name=data.name,
                email=data.emai,
                hash_pass=pwd_context.hash(data.password)
                )
                dba.add(d)
                await dba.commit()
                await dba.refresh(d)
                otp = random.randint(100000, 999999)   
                bgts.add_task(sed,data.emai,otp)
                return{
                    "status":"registeration successfull"
                    }
    
        except Exception as e:
                raise HTTPException(status_code=427,detail=f"{e}") 
            
    else:
        raise HTTPException(status_code=433,detail="otp already sent")

@router.post("/login",response_model=(user))
async def sef(data:login,dba:AsyncSession=Depends(get_db)):
    return await gets(data,dba,BackgroundTasks())

@router.post("/{email1}/{otp}")
async def votp(otp:int,email1:str):
    return  ver(email=email1,otp=otp)
@router.get("/send")
async def fafa():
     return JSONResponse(
          content={
               "status":"accepted"
          },
          status_code=200
     )