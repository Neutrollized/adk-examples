# Travel Recommendation agent

This agent uses a local [Google Maps MCP server](https://www.npmjs.com/package/@modelcontextprotocol/server-google-maps) to give travel recommendations to the user.  The user can ask about restaurants, hotels, etc. that are near a given primary location.

**NOTE:** I've noticed that it doesn't always honor the correct distance restrictions (i.e. within a given radius).


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
