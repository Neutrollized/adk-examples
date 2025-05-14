# FastMCP & ngrok

## FastMCP
This part is pretty straightforward:
```sh
python ./server.py
```
or
```sh
fastmcp run server.py --transport sse
```

**NOTE:** if you use the `fastmcp` option, it ignores the `if __name__ == "__main__"`, so you need to pass `--transport` and `--port`

```console
INFO:     Started server process [33440]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

Now that it's running, it's only accessible locally on port 8080.  To simulate a publicly hosted MCP server, I turned to a tool called `ngrok`.


## ngrok
I started using [ngrok](https://ngrok.com/) recently for some development work surrounding Dialogflow CX / Conversational AI, and thought it would be perfect for local testing and making local MCP servers publicly available for testing purposes.

You'll have to sign up for a free account and once you log in, there will be instructions on how to authenticate (i.e. `ngrok config add-authtoken YOUR_TOKEN_HERE`), but afterwards it's also pretty straightforward.

In a separate terminal window, run:
```sh
ngrok http http://localhost:8080
```

```console
Session Status                online
Account                       USERNAME_HERE (Plan: Free)
Version                       3.22.1
Region                        United States (us)
Latency                       47ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://0737-173-230-183-237.ngrok-free.app -> http://localhost:8080

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

As you can see in the above output, it created a secure tunnel from a randomly generated public URL to my localhost, and now I can pass this URL as an environment variable to my agent.
