from fastapi import FastAPI
from .routers import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def index():
    return f"Hello World"
