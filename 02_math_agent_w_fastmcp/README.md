# Math Agent with MCP Server

SSE = Server-Sent Events


Alice brought 12 pizzas. Bob brought 8 pizzas. Charlie brought 5 pizzas. There are 8 slices per pizza. If there are 50 people sharing the pizzas, how many slices do each person get?
# Weather & Time agent

Agent that can tell you the date/time and weather of a given city, country. Uses sub-agents to handle weather and date/time separately. 


- sample terminal output from `adk run 02_math_agent_w_fastmcp`:
```console
Running agent math_agent, type exit to exit.
[user]: what's 6/2+9*9
[math_agent]: 6 / 2 = 3 and 9 * 9 = 81. Therefore, 6/2 + 9*9 = 3 + 81 = 84

[user]: Alice brought 12 pizzas. Bob brought 8 pizzas. Charlie brought 5 pizzas. There are 8 slices per pizza. If there are 50 people sharing the pizzas, how many slices do each person get?
[math_agent]: Alice brought 12 pizzas, Bob brought 8 pizzas, and Charlie brought 5 pizzas. So there are 12 + 8 + 5 = 25 pizzas in total.
There are 8 slices per pizza, so there are 25 * 8 = 200 slices of pizza.
There are 50 people sharing the pizzas, so each person gets 200 / 50 = 4 slices.

[user]: Frank has 5 cats and each cat has 2 ears, how many ears are there in total (including Frank)?
[math_agent]: Frank has 2 ears.
The 5 cats have 5 * 2 = 10 ears.
In total, there are 2 + 10 = 12 ears.

[user]: exit
```

(I tried to trick it with the last question)
