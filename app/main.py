from typing import Annotated
from fastapi import Depends, FastAPI
from app.routers import auth, applications
from app.routers.auth import auth_scheme
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth.router)
app.include_router(applications.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Fix this in future
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def index(token : Annotated[str, Depends(auth_scheme)]):
    return f"Hello World"
