from fastapi import FastAPI
<<<<<<< HEAD
from app.routers import users, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
=======
from .routers import applications

app = FastAPI()

app.include_router(applications.router)
>>>>>>> 6fc1753cb6e552a8d0f1ae9425aeda19402e0d4d

@app.get("/")
async def index():
    return f"Hello World"
