from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import List
import databases
import sqlalchemy
from datetime import datetime

app = FastAPI()

DATABASE_URL = "sqlite:///./Student.db"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
register = sqlalchemy.Table(
    "register",
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


@app.post('/Student/', response_model=Student)
async def create(r: StudentIn = Depends()):
    query = register.insert().values(
        name=r.name,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@app.get('/Student/{id}', response_model=Student)
async def get_one(id: int):
    query = register.select().where(register.c.id == id)
    user = await database.fetch_one(query)
    return {**user}


@app.get('/Student/', response_model=List[Student])
async def get_all():
    query = register.select()
    all_get = await database.fetch_all(query)
    return all_get


@app.put('/Student/{id}', response_model=Student)
async def update(id: int, r: StudentIn = Depends()):
    query = register.update().where(register.c.id == id).values(
        name=r.name,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@app.delete("/Student/{id}", response_model=Student)
async def delete(id: int):
    query = register.delete().where(register.c.id == id)
    delete_id = await database.execute(query)
    if not delete_id:
        return {'messages': f"No details found of this Id{id}"}
    return {'messages': f"Data Successfully deleted of Id{id}"}

