from models.visual_weather import Weather, FutureWeather


def get_weather(location=None, dates=None):
    from data.weather import data

    location = data["resolvedAddress"]
    alerts = data["alerts"]
    current_weather: Weather = Weather(**{key: val for key, val in data[
        "currentConditions"].items() if key in Weather.__dataclass_fields__})
    future_weather: list = []
    for day in data["days"]:
        data = {key: val for key, val in day.items() if key in
                FutureWeather.__dataclass_fields__}
        future_weather.append(FutureWeather(**data))

    return location, alerts, current_weather, future_weather

