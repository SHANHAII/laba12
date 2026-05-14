from fastapi import FastAPI

from app.database import Base, engine
from app.routers import accounts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking API",
    description="REST API для управления банковскими счетами. Вариант 10.",
    version="1.0.0",
)

app.include_router(accounts.router)


@app.get("/")
def root():
    return {"message": "Banking API работает", "docs": "/docs"}
