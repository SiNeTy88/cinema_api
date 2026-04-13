from fastapi import FastAPI

from app.api import router

app = FastAPI(
    title="Cinema API",
    description="Бекенд для бронювання квитків у кіно"
)

app.include_router(router)