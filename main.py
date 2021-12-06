from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import List
import databases
import sqlalchemy
from datetime import datetime
tags = [{"name": "Create", "description": "This are my user creation routes"},
        {"name": "Get_All", "description": "This are my all Data fetch routes"},
        {"name": "Get_One", "description": "This are my Single data fetch routes"},
        {"name": "Update", "description": "This are my Single Data Updating routes"},
        {"name": "Delete", "description": "This are Single Data Deletion routes"}]
app = FastAPI(title='My App',
              contact={"name": "Dipu Kumar Sharma",
                       "email": "dipu.s@dreamztech.com"},
              openapi_tags=tags,
              docs_url='/dipu')

DATABASE_URL = "sqlite:///./Student.db"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
register = sqlalchemy.Table(
    "Student",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("date_created", sqlalchemy.DateTime())

)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
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
