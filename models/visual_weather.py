from dataclasses import dataclass, field


def verbose_name(name):
    return field(metadata={"verbose_name": name})


@dataclass
class Weather:
    datetime: str = verbose_name("Data i czas")
    temp: float = verbose_name("Temperatura")
    feelslike: float = verbose_name("Odczuwalna temperatura")
    dew: float = verbose_name("Punkt rosy")
    humidity: float = verbose_name("Wilgotność")
    precip: float = verbose_name("Opad")
    precipprob: float = verbose_name("Prawdopodobieństwo opadu")
    preciptype: list = verbose_name("Rodzaj opadu")
    snow: float = verbose_name("Śnieg")
    snowdepth: float = verbose_name("Głębokość śniegu")
    windgust: float = verbose_name("Poryw wiatru")
    windspeed: float = verbose_name("Prędkość wiatru")
    pressure: float = verbose_name("Ciśnienie")
    cloudcover: float = verbose_name("Zachmurzenie")
    visibility: float = verbose_name("Widoczność")
    solarradiation: float = verbose_name("Promieniowanie słoneczne")
    uvindex: float = verbose_name("Indeks UV")
    sunrise: str = verbose_name("Wschód słońca")
    sunset: str = verbose_name("Zachód słońca")
    moonphase: float = verbose_name("Faza księżyca")
    icon: str = verbose_name("Ikona")


@dataclass
class FutureWeather(Weather):
    tempmax: float = verbose_name("Maksymalna temperatura")
    tempmin: float = verbose_name("Minimalna temperatura")
    feelslikemax: float = verbose_name("Maksymalna odczuwalna temperatura")
    feelslikemin: float = verbose_name("Minimalna odczuwalna temperatura")
    precipcover: float = verbose_name("Pokrycie opadami")
    severerisk: float = verbose_name("Ryzyko silnych zjawisk")
    hours: list = verbose_name("Pogoda według godzin")
    conditions: str = verbose_name("Warunki pogodowe")
    description: str = verbose_name("Opis")
