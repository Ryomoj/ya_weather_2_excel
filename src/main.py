from fastapi import FastAPI
import uvicorn

from src.api.weather import router as weather_router

app = FastAPI()

app.include_router(weather_router)



if __name__ == "__main__":
    uvicorn.run("main:app")