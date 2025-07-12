from weather_agentengine.tools.tools import (
    get_geocoding,
    find_current_weather,
    convert_c2f,
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

def test_convert_c2f():
    c_temp = 0
    result = convert_c2f(c_temp)
    assert isinstance(result, float)
    assert result == 32.0
