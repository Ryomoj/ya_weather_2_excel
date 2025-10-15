from datetime import datetime

from fastapi import APIRouter
from starlette.responses import FileResponse

from src.database import add_new_stats
from src.utils.excel import save_forecast_2_excel
from src.utils.weather import get_coordinates_by_city_name, get_weather_forecast_by_lat_lon, get_weather_details

router = APIRouter(prefix="/weather", tags=["Прогноз погоды"])

@router.get("/{city_name}", summary="Получить прогноз погоды")
async def get_weather_by_city_name(
        city_name: str,
        days: int = 7
):
    coordinates = get_coordinates_by_city_name(city_name)
    if coordinates is None:
        add_new_stats(input_data=city_name, date=datetime.now(), status="Ошибка получения координат")
        return {"STATUS": "geocoder error"}

    raw_weather_data = get_weather_forecast_by_lat_lon(coordinates["lat"], coordinates["lon"], days=days)
    if raw_weather_data is None:
        add_new_stats(input_data=city_name, date=datetime.now(), status="Ошибка доступа к сервису Яндекс.Погода")
        return {"STATUS": "yandex.weather error"}

    weather_data = get_weather_details(raw_weather_data)
    daily_forecast = weather_data["daily_forecast"]

    try:
        save_forecast_2_excel(daily_forecast)
    except PermissionError:
        return {"STATUS": "denied", "INFO": "Файл уже открыт"}

    add_new_stats(input_data=city_name, date=datetime.now(), status="Успешно")

    return FileResponse(path='weather_forecast.xlsx', filename='Прогноз погоды.xlsx', media_type='multipart/form-data')

