import requests

weather_access_key = "1f1e1cfa-2644-48ff-902d-2f71aa0d9477"
geocoder_api_key = "pk.3eefeb00697e051f63652e977e277866"


def get_coordinates_by_city_name(city_name: str) -> dict:
    url = f"https://us1.locationiq.com/v1/search.php"

    params = {
        'key': geocoder_api_key,
        'q': city_name,
        'format': 'json',
        'limit': 1
    }

    response = requests.get(url, params=params)
    response_data = response.json()

    lat = response_data[0]["lat"]
    lon = response_data[0]["lon"]

    return {"lat": lat, "lon": lon}



def get_weather_forecast_by_lat_lon(lat: float, lon: float, days: int = 7) -> dict:
    url = "https://api.weather.yandex.ru/v2/forecast"

    headers = {
        'X-Yandex-Weather-Key': weather_access_key
    }

    params = {
        "lat": lat,
        "lon": lon,
        "limit": days,
        "hours": True,
        "lang": "ru_RU"
    }

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    return response_data



def get_weather_details(weather_row_data: dict):
    result = {
        "daily_forecast": []
    }

    for forecast in weather_row_data['forecasts']:
        date = forecast['date']

        day_forecast = {
            "date": date,
            "day_average_temp": int,
            "magnetic_field_forecast": int,
            "pressure_warning": str,
            "day_periods": {}
        }

        magnetic_field_index = forecast.get('biomet', {}).get('index', 0)
        day_forecast["magnetic_field_forecast"] = magnetic_field_index

        temperatures_per_day_parts = []
        pressures_per_day_parts = []

        parts = forecast.get('parts', {})
        for part_name, part_data in parts.items():
            if part_name in ['morning', 'day', 'evening', 'night']:
                day_forecast["day_periods"][part_name] = {
                    "temperature_avg": part_data.get('temp_avg'),
                    "condition": part_data.get('condition', ''),
                    "pressure": part_data.get('pressure_mm'),
                    "humidity": part_data.get('humidity')
                }

                part_pressure = part_data.get("pressure_mm")
                pressures_per_day_parts.append(part_pressure)

            if part_name in ['morning', 'day', 'evening']:
                part_temperature = part_data.get("temp_avg")
                temperatures_per_day_parts.append(part_temperature)

        min_pressure = min(pressures_per_day_parts)
        max_pressure = max(pressures_per_day_parts)
        if max_pressure - min_pressure >= 5:
            min_index = pressures_per_day_parts.index(min_pressure)
            max_index = pressures_per_day_parts.index(max_pressure)

            if max_index < min_index:
                day_forecast["pressure_warning"] = "ожидается резкое падение атмосферного давления"
            elif max_index > min_index:
                day_forecast["pressure_warning"] = "ожидается резкое увеличение атмосферного давления"
        else:
            day_forecast["pressure_warning"] = ""

        average_temp = round(sum(temperatures_per_day_parts) / len(temperatures_per_day_parts), 2)
        day_forecast["day_average_temp"] = average_temp

        result["daily_forecast"].append(day_forecast)

    return result

