from weather_time_agent.tools.tools import (
    get_geocoding,
    get_timezone,
    find_current_weather,
    find_current_time_in_tz,
)
import logging

# Configure logging for the test file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_get_geocoding():
    city = "Toronto"
    country = "Canada"
    result = get_geocoding(city, country)
    assert isinstance(result, dict)
    assert result == {
        "latitude": 43.70643,
        "longitude": -79.39864
    }

# I can only assert that the function returns a float
# as the temperature is live/dynamic value
def test_find_current_weather():
    latitude = 43.70643
    longitude = -79.39864
    result = find_current_weather(latitude, longitude)
    assert isinstance(result, float)

def test_get_timezone():
    latitude = 43.70643
    longitude = -79.39864
    result = get_timezone(latitude, longitude)
    assert isinstance(result, str)
    assert result == "America/Toronto"

def test_find_current_time_in_tz():
    timezone_name = "America/Toronto"
    result = find_current_time_in_tz(timezone_name)
    assert isinstance(result, str)  # only strings can be ISO formatted date/times
