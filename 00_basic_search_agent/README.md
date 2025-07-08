# Basic Search agent

This agent is a very basic agent that leverages the built-in Google Search tool to help answer user's questions.


## Running Agent
- ADK dev UI (http://localhost:8000):
```
adk web
```

- ADK cli/terminal:
```
adk run basic_search_agent
```

- sample terminal output from `adk run basic_search_agent`:
```console
Running agent search_agent, type exit to exit.
[user]: hi there!  what can you do?

[search_agent]: Hi there! I can answer your questions by searching the internet. Just tell me what you'd like to know!

[user]: what can you tell me about the google developer experts program?

[search_agent]: The Google Developer Experts (GDE) program is a global initiative that recognizes and supports highly experienced technology experts, influencers, and thought leaders in various Google technologies. These individuals are not Google employees but are acknowledged for their deep expertise and significant contributions to the developer community.

**What GDEs Do:**
GDEs are passionate professionals who actively share their knowledge and make an impact on the community. Their contributions can include:
*   Creating YouTube tutorials and writing blogs.
*   Contributing to open-source projects.
*   Speaking at events, conferences, and meetups.
*   Mentoring other developers and companies.

**Areas of Expertise:**
GDEs possess expertise in a wide array of Google technologies, including but not limited to:
*   Android
*   Angular
*   Flutter and Firebase
*   Google

[user]: exit
```
