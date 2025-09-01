from fastapi import FastAPI,HTTPException,Depends,Request
from auth import router as authrouter
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from auth import get_current_user
import uvicorn

app = FastAPI(title="Devops App")
app.include_router(authrouter,prefix="/auth",tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
user_dpendency = Annotated[dict,Depends(get_current_user)]

@app.get("/",status_code=200)
async def login(user:user_dpendency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail=" Sorry no Username like this Exists")
    return {"User": user}



if __name__ == "__main__":
    uvicorn.run("main:app",reload=True,port=8080,host='0.0.0.0')