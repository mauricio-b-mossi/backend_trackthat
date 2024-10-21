from typing import Annotated
from fastapi import Depends, FastAPI
from app.routers import auth, applications
from app.routers.auth import auth_scheme

app = FastAPI()

app.include_router(auth.router)
app.include_router(applications.router)

@app.get("/")
async def index(token : Annotated[str, Depends(auth_scheme)]):
    return f"Hello World"
