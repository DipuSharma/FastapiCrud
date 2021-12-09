from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, EmailStr
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


app = FastAPI()