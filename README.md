# CS457 Fall 2024 Term Project

This is a simple multiplayer quiz game built with python and sockets.

Its built on a client-server architecture and allows multiple players to compete to complete
quiz questions against each other.


**How to play:**
1. **Start the server:** From the `src/just_in_case` directory run the `server.py` script

`python3 server.py`


2. **Setup a client:** You can either choose between the web or terminal client. The web client is fully-featured and recommended. See web-client or terminal-client sections
3. **Play the game:** Simply enter a username and start answering t/f questions. First to 10 points wins!

## Terminal Client

From the `src/just_in_case` directory run the `client.py` script on two different machines or terminals.

NOTE: This client was used earlier in development, so it isn't concidered to be functional

## Web Client

### Install `websockify`

To run the web client you'll first need to install `websockify`. 

This is a bridge program that allows a browser's websocket connections to be forwarded to a traditional tcp socket, meaning our web client uses the same protocol the terminal client does.

- If you're using debian (which uses an externally managed enviroment) you can install it with `sudo apt install python3-websockify`
- If you're using another setup you should be able to run `pip3 install websockify`.
- If that doesn't work look at [their repository](https://github.com/novnc/websockify) for other installation options.

The end result should be that you can run the `websockify` command from your terminal.

### Running web client

From the `src/web_client` directory run the command...

```bash
websockify 8080 127.0.0.1:57054 --web=./
```

This sets up a webserver and websocket bridge that servers the client's files and forwards client connections.

NOTE: you can run this on another port, but you'll have to modify the line at the top of the `script.js` file to point to the correct server.

Make sure the server is running at the `127.0.0.1:57054` address

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* https://www.python.org/doc/
* https://realpython.com/python-sockets/
