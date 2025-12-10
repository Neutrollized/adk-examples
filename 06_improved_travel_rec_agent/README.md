# Improved Travel Agent

Leverages some changes since v1.17.0 to the agent which allows the built-in Google Search to be used with other tools.

> [!NOTE]
> `maps_agent/server.py` is from [Google Maps MCP server](https://github.com/Neutrollized/google-maps-mcp-server)


- example interaction:
```console
Running agent travel_rec_agent, type exit to exit.
[user]: I'm going to Scotiabank Arena to watch a Raptors game, what hotel nearby do you recommend?
...
...
[travel_rec_agent]: Here are some hotel recommendations near Scotiabank Arena:

*   **One King West Hotel & Residence**
    *   Rating: 4.4
    *   Address: 1 King St W, Toronto, ON M5H 1A1, Canada

*   **Toronto Marriott City Centre Hotel**
    *   Rating: 4.4
    *   Address: 1 Blue Jays Way, Toronto, ON M5V 1J3, Canada
...
...
*   **Chelsea Hotel, Toronto**
    *   Rating: 3.8
    *   Address: 33 Gerrard St W, Toronto, ON M5G 1Z4, Canada

*   **The Clarence Park**
    *   Rating: 3.8
    *   Address: 7 Clarence Square, Toronto, ON M5V 1H1, Canada
[user]: I have a marriott and hyatt membership
[travel_rec_agent]: Given your Marriott and Hyatt memberships, here are the hotels near Scotiabank Arena that belong to those chains:

**Marriott Hotels:**

*   **Toronto Marriott City Centre Hotel**
    *   Rating: 4.4
    *   Address: 1 Blue Jays Way, Toronto, ON M5V 1J3, Canada
*   **Courtyard by Marriott Toronto Downtown**
    *   Rating: 4.1
    *   Address: 475 Yonge St, Toronto, ON M4Y 1X7, Canada
[user]: I think i'll stay at courtyard
[travel_rec_agent]: Great choice! The Courtyard by Marriott Toronto Downtown is a good option.

To help you make the most of your trip, are there any particular types of local events you're interested in (e.g., concerts, museums, festivals, dining experiences)? Also, could you please let me know the dates you'll be staying so I can look for events happening during that time?
[user]: are there any concerts happening? I'm going to be staying dec 12 to 21st, 2025
[travel_rec_agent]: Here's a list of concerts and music events happening in Toronto between December 12th and December 21st, 2025:

### **Friday, December 12, 2025**
*   **An Andrean Christmas** at Roy Thomson Hall.
*   **Inoi Music Festival** at Rebel (formerly Sound Academy) starting at 4:00 PM.
*   **The Flatliners w/ Fucked Up, Samiam, Dead Broke** at The Danforth Music Hall starting at 6:00 PM.
*   **Shawn Desman - Back to Life** at History starting at 7:00 PM.
*   **grandson - INERTIA Tour** at Phoenix Concert Theatre at 7:00 PM.
*   **David Tao - Soul Power II World Tour** at Coca-Cola Coliseum starting at 8:00 PM.
*   **Marcellus Pittman and Special Guests** presented by roam x Standard Time at Standard Time.
*   **Asha Banks - How Real Was It Tour** at Drake Underground.
*   **REJOICE! Jubilee Celebration – 60 Years at Massey Hall** at Massey Hall.
*   **Noize MC, Monetochka, Ivan Dorn, AIGEL** at Rebel.
*   **Nils Hoffmann, Jesse Mac Cormack** at The Opera House at 10:00 PM.
*   **Ben Caplan** at Lee's Palace.
*   **Dark Thoughts, Béton Armé** at The Garrison.
*   **Jane Inc., Moon King** at The Baby G.
*   **Ayla, Singhara** at Story Toronto.
*   **Hank Collective, Steve Tidy & The Unkempt, Jo Snyder** at The Sound Garage.
*   **Taplin, The Stankonya Funktet, Lady Marge** at Rivoli.

### **Saturday, December 13, 2025**
*   **Christmas With The Salvation Army** at Roy Thomson Hall.
*   **David Tao - Soul Power II World Tour** at Coca-Cola Coliseum starting at 8:00 PM.
*   **iheartluster: evilgiane, AL-P & luster** at The Mod Club (formerly known as The Axis Club) starting at 9:00 PM.
*   **REJOICE! Jubilee Celebration – 60 Years at Massey Hall** at Massey Hall.
*   **Kurtis Conner: The Goodfellow World Tour** at The Danforth Music Hall.

### **Sunday, December 14, 2025**
*   **Toronto Children's Chorus** at Roy Thomson Hall.
*   **The Tallis Scholars, Director Peter Phillips** at TO Live.

### **Tuesday, December 16, 2025**
*   **TSO - Messiah** at Roy Thomson Hall, with performances continuing until December 21.
*   **Ms. Lauryn Hill** at Massey Hall.

### **Wednesday, December 17, 2025**
*   **Burna Boy: No Sign of Weakness Tour** at Scotiabank Arena.
*   **Good Lovelies Holiday Concert** at Massey Hall.
*   **Bankrol Hayden** at The Mod Club (formerly known as The Axis Club) starting at 7:00 PM.
*   **Air Supply: 50th Anniversary Celebration** at Great Canadian Toronto starting at 8:00 PM.

### **Thursday, December 18, 2025**
*   **Classic Albums Live: Pink Floyd** at Massey Hall.

### **Friday, December 19, 2025**
*   **Orpheus Choir of Toronto** at Roy Thomson Hall.
*   **Christmas Hour with Noah Reid** at Massey Hall.

### **Saturday, December 20, 2025**
*   **CHOIR! CHOIR! CHOIR!** at Massey Hall.

### **Sunday, December 21, 2025**
*   **'Twas On A Night Like This** at Young Centre for the Performing Arts - Michael Young.
*   **4AM LAST CALL - Sunday SerVice: Holiday Fam Jam & TOY DRIVE** at Wiggle Room.
*   **Candlelight: Christmas Classics** at Toronto Marriott Markham.
*   **Candlelight: Tribute to Céline Dion** at Metropolitan Community Church of Toronto.
*   **Sing-Along Messiah** at Massey Hall.
*   **TSO - Messiah** at Roy Thomson Hall (final day).

Please note that event details are subject to change, and it is recommended to check official websites or social media pages for the latest information and ticket availability.
```
