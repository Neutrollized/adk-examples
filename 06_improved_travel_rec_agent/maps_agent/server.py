"""This module defines a FastMCP server for Google Maps Platform operations."""

import os
from typing import Any

import googlemaps
from fastmcp import FastMCP

# ---------------
# settings
# ---------------
# these host, port, transport settings only apply if run using python
host = os.environ.get("FASTMCP_HOST", "0.0.0.0")
port = os.environ.get("FASTMCP_PORT", "8080")
transport = os.environ.get("FASTMCP_TRANSPORT", "stdio")  # stdio, streamable-http, sse

google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=google_maps_api_key)


# -------------
# helpers
# -------------
allowed_modes = ["driving", "walking", "bicycling", "transit"]


def assert_mode(mode: str):
    assert mode in allowed_modes, (
        f"ERROR: '{mode}' is not one of the allowed modes: {allowed_modes}"
    )


allowed_input_types = ["textquery", "phonenumber"]


def assert_input_type(input_type: str):
    assert input_type in allowed_input_types, (
        f"ERROR: '{input_type}' is not one of the allowed inpute types: {allowed_input_types}"
    )


DEFAULT_FIND_PLACE_FIELDS = [
    "place_id",
    "formatted_address",
    "name",
    "geometry",
    "types",
    "rating",
]
DEFAULT_PLACE_DETAILS_FIELDS = [
    "name",
    "formatted_address",
    "formatted_phone_number",
    "website",
    "types",
    "rating",
    "user_ratings_total",
]

# -----------------------
# initialize fastmcp
# -----------------------
# https://gofastmcp.com/servers/fastmcp#server-configuration
mcp = FastMCP(
    name="FastMCP Google Maps Platform Server",
    on_duplicate="error",
)


# -------------------
# direction tools
# -------------------
@mcp.tool()
async def get_directions(
    origin: str, destination: str, mode: str = "driving"
) -> dict[str, Any] | None:
    """Gives step-by-step instructions to get from origin to destination using a particular mode of transport
    Args:
        origin (str): originating address
        destination (str): destination address
        mode (str, optional): mode of transportation. Valid options are: driving, walking, bicycling, transit

    Returns:
        dictionary (JSON) of steps along with total distance and total duration
    """
    try:
        assert_mode(mode)
    except AssertionError as e:
        # print(e) # Replaced print with a return
        return {"error": str(e)}

    results = gmaps.directions(origin, destination, mode)

    if results:
        shortest_route = results[0]

        output = {
            "summary": shortest_route["summary"],
            "total_distance": shortest_route["legs"][0]["distance"]["text"],
            "total_duration": shortest_route["legs"][0]["duration"]["text"],
            "steps": [],
        }

        for leg in shortest_route["legs"]:
            for step in leg["steps"]:
                output["steps"].append(
                    {
                        "instruction": step["html_instructions"],
                        "distance": step["distance"]["text"],
                        "duration": step["duration"]["text"],
                    }
                )
        return output
    else:
        return "No directions found for the specified locations."


# --------------------------
# distance matrix tools
# --------------------------
@mcp.tool()
async def get_distance(
    origin: str, destination: str, mode: str = "driving"
) -> dict[str, Any] | None:
    """Finds the distance and travel time between two locations for a mode of transportation
    Args:
        origin (str): originating address
        destination (str): destination address
        mode (str): mode of travel (driving, walking, bicycling, transit)

    Returns:
        dictionary (JSON) of total distance, total travel time duration, and mode of travel
    """
    try:
        assert_mode(mode)
    except AssertionError as e:
        # print(e) # Replaced print with a return
        return {"error": str(e)}

    results = gmaps.distance_matrix(origin, destination, mode)

    if results:
        rows = results.get("rows", [])
        if not rows:  # Check if rows is empty
            return "No distance information found for the specified locations."  # More specific message

        shortest_distance_elements = rows[0].get("elements", [])
        if (
            not shortest_distance_elements
            or "distance" not in shortest_distance_elements[0]
            or "duration" not in shortest_distance_elements[0]
        ):
            return "No distance information found for the specified locations."  # More specific message

        # At this point, we expect elements[0] to have distance and duration
        element = shortest_distance_elements[0]

        # Additional check for status if available, e.g. "ZERO_RESULTS"
        if element.get("status") == "ZERO_RESULTS":
            return "No distance information found for the specified locations (ZERO_RESULTS)."

        output = {
            "total_distance": element["distance"]["text"],
            "total_duration": element["duration"]["text"],
            "mode": mode,
        }
        return output
    else:
        return "No distance information found for the specified locations."  # Generic message for no results


# -------------------
# geocoding tools
# -------------------
@mcp.tool()
async def get_geocode(address: str) -> dict[str, Any] | None:
    """
    Args:
        address (str): can be address or the name of a place

    Returns:
        dictionary (JSON) with the geocode (latitude & longitude) of the address
    """
    results = gmaps.geocode(address)

    if results:
        geocode = results[0]

        output = {
            "lat": geocode["geometry"]["location"]["lat"],
            "lng": geocode["geometry"]["location"]["lng"],
        }
        return output

    else:
        return "Address not found"


# -------------------
# places tools
# -------------------
@mcp.tool()
async def find_place(
    input: str, input_type: str = "textquery", fields: list[str] | None = None
) -> dict[str, Any]:
    """Find/query a place with the provided name
    Args:
        input (str): name of the place you're looking for. provide more details if possible (i.e. city, country, etc.) for better accuracy. can also be the establishment type (i.e. bakery, bank, etc.)
        input_type (str, optional): the type of query, it can be a textquery or phonenumber query
        fields (list, optional): list of fields to query for

    Returns:
        dictionary (JSON) of with basic information of the top result based on input query. basic information inclulde:
        - name
        - place_id
        - address
        - location (latitude, longitude)
        - establishment type
        - average rating
    """
    try:
        assert_input_type(input_type)
    except AssertionError as e:
        # print(e) # Replaced print with a return
        return {"error": str(e)}

    if fields is None:
        fields = DEFAULT_FIND_PLACE_FIELDS

    results = gmaps.find_place(input, input_type, fields)
    if not results:
        return {"message": "No such place found."}

    candidates = results.get("candidates", [])
    if not candidates:
        return {"message": "No such place found."}

    place = candidates[0]
    return {
        "name": place["name"],
        "place_id": place["place_id"],
        "formatted_address": place["formatted_address"],
        "location": place["geometry"]["location"],
        "types": place["types"],
        "rating": place.get("rating", None),
    }


@mcp.tool()
async def place_nearby(
    location: dict, radius: int, place_type: str
) -> dict[str, Any] | None:
    """Find types of places within a radius of a location (latitude, longitude)
    Args:
        location (dict): dictionary with 'lat' and 'lng' as keys and values are the latitude and longitude respectively
        radius (int): search area radius in meters (i.e. 2500 = 2.5km)
        place_type (str): type of place you're looking for (i.e. "italian restaurant", "hotel", etc.)

    Returns:
        dictionary (JSON) of establishment names (key) and their place_id (value)
    """
    results = gmaps.places_nearby(location, radius, place_type)
    if not results:
        return {"message": "Nothing nearby that matches the search criteria was found."}

    places_nearby = results.get("results", [])
    if not places_nearby:
        return {"message": "Nothing nearby that matches the search criteria was found."}

    output = {}
    for place in places_nearby:
        output[place["name"]] = place["place_id"]
    return output


@mcp.tool()
async def place_details(
    place_id: str, fields: list[str] | None = None
) -> dict[str, Any]:
    """
    Args:
        place_id (str): place_id of the place, which can be obtained via find_place() or place_nearby()
        fields (list, optional): list of fields to query for

    Returns:
        dictionary (JSON) of with details of provided place. details inclulde:
        - name
        - address
        - phone number
        - website
        - establishment type
        - average rating
        - total rating count
    """
    if fields is None:
        fields = DEFAULT_PLACE_DETAILS_FIELDS

    results = gmaps.place(place_id, fields)
    if not results:
        return {"message": "No such place found."}

    details = results.get("result", {})
    if not details:
        return {"message": "No details found for the specified place."}

    output = {
        "name": details.get("name"),
        "formatted_address": details.get("formatted_address"),
        "formatted_phone_number": details.get("formatted_phone_number"),
        "website": details.get("website"),
        "types": details.get("types"),
        "rating": details.get("rating"),
        "user_ratings_total": details.get("user_ratings_total", 0),
    }
    # Filter out None values to keep the payload clean
    output = {k: v for k, v in output.items() if v is not None}

    if not output.get("name"):
        return {"message": "Essential place details (e.g. name) are missing."}

    return output


# ----------------
# main
# ----------------
# https://gofastmcp.com/deployment/running-server
if __name__ == "__main__":
    try:
        mcp.run(transport=transport, host=host, port=port)
    except KeyboardInterrupt:
        print("> FastMCP Google Maps Server stopped by user.")
    except Exception as e:  # noqa: BLE001
        print(f"> FastMCP Google Maps Server encountered error: {e}")
    finally:
        print("> FastMCP Google Maps Server exiting.")
