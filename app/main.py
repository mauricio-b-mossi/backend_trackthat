from fastapi import FastAPI
from app.routers import auth, applications

app = FastAPI()

app.include_router(auth.router)
app.include_router(applications.router)

@app.get("/")
async def index():
    return f"Hello World"
