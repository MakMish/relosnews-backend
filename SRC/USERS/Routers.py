from fastapi import APIRouter,Depends,BackgroundTasks,HTTPException,Request
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
r=redis.Redis.from_url(url=setting.redis_url,decode_responses=True)
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


@router.post("/register")
async def gets2(request1:Request,data:register,bgts:BackgroundTasks=BackgroundTasks()):
    x=r.get(f"{request1.client.host}")
    print("2")
    print("1")
    if x is None:
        print("2")
        try:
                otp = random.randint(100000, 999999)   
                bgts.add_task(sed,request1,data.emai,otp,)
                return{
                    "status":"otp added"
                    }
    
        except Exception as e:
                raise HTTPException(status_code=427,detail=f"{e}") 
            
    else:
        raise HTTPException(status_code=433,detail="otp already sent")

@router.post("/login",response_model=(user))
async def sef(data:login,dba:AsyncSession=Depends(get_db)):
    return await gets(data=data,dba=dba)

@router.post("/{email1}/{otp}")
async def votp(request2:Request,otp:int,data1:register,dba1:AsyncSession=Depends(get_db)):
    return await ver(request1=request2,otp=otp,data=data1,dba=dba1)
@router.get("/send")
async def fafa():
     return JSONResponse(
          content={
               "status":"accepted"
          },
          status_code=200
     )