import pytest
import logging

from weather_time_agent.tools.tools import (
    get_geocoding_v2,
    get_timezone,
    find_current_weather_v2,
    find_current_time_in_tz,
    convert_c2f,
)

# Configure logging for the test file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_get_geocoding_v2():
    city = "Toronto"
    country = "Canada"
    result = await get_geocoding_v2(city, country)
    assert isinstance(result, dict)
    assert result == {
        "latitude": 43.70643,
        "longitude": -79.39864
    }

# I can only assert that the function returns a float
# as the temperature is live/dynamic value
@pytest.mark.asyncio
async def test_find_current_weather_v2():
    latitude = 43.70643
    longitude = -79.39864
    result = await find_current_weather_v2(latitude, longitude)
    assert isinstance(result, float)

@pytest.mark.asyncio
async def test_get_timezone():
    latitude = 43.70643
    longitude = -79.39864
    result = await get_timezone(latitude, longitude)
    assert isinstance(result, str)
    assert result == "America/Toronto"

@pytest.mark.asyncio
async def test_find_current_time_in_tz():
    timezone_name = "America/Toronto"
    result = await find_current_time_in_tz(timezone_name)
    assert isinstance(result, str)  # only strings can be ISO formatted date/times

@pytest.mark.asyncio
async def test_convert_c2f():
    c_temp = 0
    result = await convert_c2f(c_temp)
    assert isinstance(result, float)
    assert result == 32.0
