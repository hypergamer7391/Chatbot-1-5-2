import python_weather
import tracemalloc
import random

async def get_weather_forecast(location):
    async with python_weather.Client() as client:
        try:
            weather = await client.get(location)
            weather_descrip = weather.current.description.lower()
            return f"In {location}, ist es  {weather.current.temperature}°C und {weather_descrip}."
        except python_weather.exceptions.BadApiKeyError:
            return "API key is invalid."
        except python_weather.exceptions.NotFoundError:
            return f"Could not find weather information for {location}."
async def get_current_temp(location):
    async with python_weather.Client() as client:
        weather = await client.get(location)
        return f"The temperature is {weather.current.temperature}°C in {location}."
