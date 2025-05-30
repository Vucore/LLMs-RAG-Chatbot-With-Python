from fastapi import FastAPI
from .api import endpoints
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký router đúng cách
app.include_router(endpoints.router, prefix="/api")
