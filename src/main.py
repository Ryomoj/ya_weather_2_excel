from fastapi import FastAPI
import uvicorn

from api.weather import router as weather_router

app = FastAPI()

app.include_router(weather_router)


@app.get("/", summary="root")
def welcome():
    return {"detail": "Для перехода в Swagger-документацию к url добавьте /docs#"}

if __name__ == "__main__":
    uvicorn.run("main:app")