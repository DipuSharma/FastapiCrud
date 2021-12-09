FROM python:3.9.6
RUN pip install fastapi uvicorn databases aiosqlite pydantic SQLAlchemy fastapi-mail starlette python-dotenv
COPY ./app /app
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]