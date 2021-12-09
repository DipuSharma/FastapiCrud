from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import databases
from dbconfig import DATABASE_URL
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import os

load_dotenv()

EMAIL = os.getenv('EMAIL')
PASS = os.getenv('PASS')


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL,  ## Enter Your Gmail Id
    MAIL_PASSWORD=PASS,  ## Enter Your Password
    MAIL_FROM=EMAIL,  ## Enter Again Your Gmail Id
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

tags = [{"name": "Create", "description": "This are my user creation routes"},
        {"name": "Get_All", "description": "This are my all Data fetch routes"},
        {"name": "Get_One", "description": "This are my Single data fetch routes"},
        {"name": "Update", "description": "This are my Single Data Updating routes"},
        {"name": "Delete", "description": "This are Single Data Deletion routes"},
        {"name": "Send-Mail", "description": "Send Mail Using Fastapi routes, Please mention your gmail, pass in code"}]

app = FastAPI(title='My App',
              version="0.0.0.1",
              contact={"name": "Dipu Kumar Sharma",
                       "email": "dipu.s@dreamztech.com"},
              openapi_tags=tags,
              docs_url='/dipu')

html = """
<p>dfgdfgdf</p> 
<h1>dgdfgdfg</h1>
"""


metadata = _sql.MetaData()
database = databases.Database(DATABASE_URL)
register = _sql.Table(
    "Student",
    metadata,
    _sql.Column("id", _sql.Integer, primary_key=True),
    _sql.Column("name", _sql.String(500)),
    _sql.Column("date_created", _sql.DateTime())

)


metadata.create_all(engine)


@app.on_event("startup")
async def connect():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class StudentIn(BaseModel):
    name: str = Field(...)


class Student(BaseModel):
    id: int
    name: str
    date_created: datetime


@app.post('/Student/', response_model=Student, tags=['Create'])
async def create(r: StudentIn = Depends()):
    query = register.insert().values(
        name=r.name,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@app.get('/Student/{id}', response_model=Student, tags=['Get_One'])
async def get_one(id: int):
    query = register.select().where(register.c.id == id)
    user = await database.fetch_one(query)
    if user:
        return {**user}
    if not user:
        return {'message': f'Data Not found of this Id {id}'}


@app.get('/Student/', response_model=List[Student], tags=['Get_All'])
async def get_all():
    query = register.select()
    all_get = await database.fetch_all(query)
    return all_get


@app.put('/Student/{id}', response_model=Student, tags=['Update'])
async def update(id: int, r: StudentIn = Depends()):
    query = register.update().where(register.c.id == id).values(
        name=r.name,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@app.delete("/Student/{id}", response_model=Student, tags=['Delete'])
async def delete(id: int):
    query = register.delete().where(register.c.id == id)
    delete_id = await database.execute(query)
    if not delete_id:
        return {'messages': f"No details found of this Id{id}"}


@app.post("/email", tags=['Send-Mail'])
async def simple_send(email: EmailSchema) -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
