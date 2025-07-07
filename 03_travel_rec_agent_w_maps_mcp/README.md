# Travel Recommendation agent

This agent uses a local [Google Maps MCP server](https://www.npmjs.com/package/@modelcontextprotocol/server-google-maps) to give travel recommendations to the user.  The user can ask about restaurants, hotels, etc. that are near a given primary location.

**ATTENTION:** I've noticed that this implementation sometimes has bugs regarding calculating distance and/or travel time. Sometimes the directions are wrong too.  This doesn't line up with what's on Google Maps so I can deduce this to be a logic issue in the MCP server code itself, so don't trust this for directions for now.  This is especially true if one of your locations is a school campus where different buildings across the campus may have the same address and this affects how the route is planned.

**NOTE:** Recently, I decided to create and maintain my very own [Google Maps MCP server (written in Python)](https://github.com/Neutrollized/google-maps-mcp-server) as the modelcontextprotocol.io one has been removed in the most recent release and hence won't be maintained.  I'm going to leave this particular example agent to use the mcp.io one to show the different implementation/deployment options that are available.

**REMINDER:** When you ask places within a certain *radius*, remember that this is a straight line distance between the two points, so your actually travel distance will be greater.

## Setup
For this example, you will need a Google Maps Platform API key.  I restricted my APIs to the following:
- Directions API
- Distance Matrix API
- Geocoding API
- Places API

You may need to expand on this if you wish to add more functionality.  Here is the [Google Maps Platform API Picker](https://developers.google.com/maps/documentation/api-picker) to help you decided what you need.  You will also need an set an additional environment variable, `GOOGLE_MAPS_API_KEY`.

Of course, there will be a [cost](https://mapsplatform.google.com/pricing) to using the Maps API as well.  It's got a pretty generous free-tier, depending on what you're using, just don't go crazy with it ;)


## Running Agent
- ADK dev UI (http://localhost:8000):
```
adk web
```

- ADK cli/terminal:
```
adk run travel_rec_agent
```

- sample terminal output from `adk run weather_time_agent`:
```console
Running agent travel_rec_agent, type exit to exit.
[user]: i'm going to be at the engineering 7 building in waterloo.  what are some nearby hotels I can stay at?
Google Maps MCP Server running on stdio
[travel_rec_agent]: Here are some hotels near Engineering 7 building, Waterloo:

*   **Delta Hotels Waterloo** - 110 Erb St W, Waterloo, ON N2L 0C6, Canada (Rating: 4.4)
*   **Waterloo Suites Hotel - Trademark Collection by Wyndham** - 547 King St N, Waterloo, ON N2L 5Z7, Canada (Rating: 3.8)
*   **The Laundry Rooms - Waterloo** - 181 King St S, Waterloo, ON N2J 0E7, Canada (Rating: 4.8)
*   **Hampton Inn & Suites by Hilton Waterloo St. Jacobs** - 55 Benjamin Rd, Waterloo, ON N2V 0C6, Canada (Rating: 4.3)
*   **Homewood Suites by Hilton Waterloo/St. Jacobs, Ontario, Canada** - 45 Benjamin Rd, Waterloo, ON N2V 2G8, Canada (Rating: 4.4)
*   **Holiday Inn Express & Suites Waterloo - St. Jacobs Area by IHG** - 14 Benjamin Rd, Waterloo, ON N2V 2J9, Canada (Rating: 4)
*   **Courtyard Waterloo St. Jacobs** - 50 Benjamin Rd, Waterloo, ON N2V 2J9, Canada (Rating: 4.2)
*   **Staybridge Suites Waterloo - St. Jacobs Area by IHG** - 10 Benjamin Rd, Waterloo, ON N2V 2J9, Canada (Rating: 4.4)
[user]: I have a marriott bonvoy membership, which hotels accept that?
[travel_rec_agent]: Based on your Marriott Bonvoy membership, these hotels near Engineering 7 building in Waterloo accept Marriott Bonvoy:

*   **Delta Hotels Waterloo** - 110 Erb St W, Waterloo, ON N2L 0C6, Canada (Rating: 4.4)
*   **Courtyard Waterloo St. Jacobs** - 50 Benjamin Rd, Waterloo, ON N2V 2J9, Canada (Rating: 4.2)
[user]: thanks. are you able to tell me the phone number of delta hotels waterloo?
[travel_rec_agent]: The phone number for Delta Hotels Waterloo is (519) 514-0404.
```
