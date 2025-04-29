



def get_weather(city: str) -> dict:
    """ Retrieves current weather report for a specified city

    Args:
        city (str): The name of the city (e.g. "New York")

    Returns:
        dict: A dictionary containing the weather info
        Includes a 'status' key ('success' or 'error')
        If 'success', it will include a 'report' key with weather details
        If 'error', it will include an 'error_message' key
    """
    city_normalized = city.lower().replace(' ', '')
    print(f'\n   Getting weather for {city_normalized}')
    mock_weather_db = {
        "newyork": {
            "status": "success",
            "report": "The weather in NY is warm and sunny"
        },
        "nairobi": {
            "status": "success",
            "report": "The weather in Nairobi is warm and sunny"
        },
    }
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {
            "status": "error",
            "error_message": "Could not find the weather for that city, sorry!"
        }