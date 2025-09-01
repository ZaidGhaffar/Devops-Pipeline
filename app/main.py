from fastapi import FastAPI,HTTPException,Depends,Request
from auth import router as authrouter
from sqlalchemy.orm import Session

import uvicorn

app = FastAPI(title="Devops App")
app.include_router(authrouter,prefix="/auth",tags=["auth"])


@app.get("/")
async def home():
    return {"Hello":"world"}



if __name__ == "__main__":
    uvicorn.run("main:app",reload=True,port=8080,host='0.0.0.0')