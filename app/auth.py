from fastapi import APIRouter,HTTPException,Depends
from database import SessionLocal,Users
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from dotenv import load_dotenv
from typing import Annotated
from pydantic import BaseModel
from datetime import datetime,timedelta
from jose import JWTError,jwt
import os
load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
bycrypt = CryptContext(schemes=["bcrypt"],deprecated="auto")
oath2_schema = OAuth2PasswordBearer(tokenUrl="/token")

class UserRequestCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str
    token_type:str = "bearer"
    
router = APIRouter()


@router.post("/", status_code=201)
async def create_user(userrequest: UserRequestCreate,db: db_dependency):
    user = Users(
        username= userrequest.username,
        hashed_password = bycrypt.hash(userrequest.password)
    )
    db.add(user)
    db.commit()
    
    
@router.post("/token",response_model=Token)
async def login_for_acess_token(formdata: Annotated[OAuth2PasswordRequestForm,Depends()],
                                db: db_dependency):
    user = authenticate_user(formdata.username,formdata.password,db)
    token = create_user_token(user.username)
    return {"token":token,"token_type":"bearer"}
    

def authenticate_user(username: str, password: str, db:db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bycrypt.verify(password,user.hashed_password):
        return False
    return user

def create_user_token(username:str) -> str:
    exipire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub":username,"exp":exipire}
    return jwt.encode(data,JWT_SECRET_KEY,ALGORITHM)

    
    
async def get_current_user(token: Annotated[str,oath2_schema]):
    payload = jwt.decode(token,JWT_SECRET_KEY,ALGORITHM)
    try:
        username:str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="unauthorize")
        return {"username":username}
    except Exception as e:
        raise HTTPException(status_code=401,detail="unauthorize")