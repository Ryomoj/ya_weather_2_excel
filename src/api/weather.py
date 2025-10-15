from fastapi import APIRouter

from utils.weather import get_coordinates_by_city_name, get_weather_forecast_by_lat_lon, get_weather_details

router = APIRouter(prefix="/weather")

@router.get("/{city_name}")
async def get_weather_by_city_name(city_name: str):
    coordinates = get_coordinates_by_city_name(city_name)
    raw_weather_data = get_weather_forecast_by_lat_lon(coordinates["lat"], coordinates["lon"])
    weather_data = get_weather_details(raw_weather_data)

    daily_forecast = weather_data["daily_forecast"]

    return {"STATUS": "OK", "DATA": daily_forecast}
