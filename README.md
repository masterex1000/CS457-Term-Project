# CS457 Fall 2024 Term Project

A simple real-time multiplayer competitive quiz game coded in python and
JavaScript.

This project is built on a client-server architecture and allows multiple
players to compete with each other by answering quiz questions.

**Technologies used:**
* Python
* Sockets

![alt](assets/multiple_clients.png)

## **How to play:**

1. **Start The Server:** From the `src/game_code` directory run the `server.py` script

```
python3 server.py -p 57054
```

2. **Start a client:** You can either choose between the web or terminal client. The web client is fully-featured and recommended, but the terminal client should work if you can't get it running for some reason.

 - [Web Client Instructions](#web-client-highly-recommended)
 - [Terminal Client Instructions](#terminal-client)

3. **Play the game:** Enter a username and start answering t/f questions. First to 10 points wins!


## Web Client **HIGHLY RECOMMENDED**

### Install `websockify`

To run the web client you'll first need to install `websockify`. 

This is a bridge program that allows a browser's websocket connections to be forwarded to a traditional tcp socket, meaning our web client uses the same protocol the terminal client does.

- If you're using Debian (which uses an externally managed environment) you can install it with `sudo apt install python3-websockify`
- If you're using another setup you should be able to run `pip3 install websockify`.
- If that doesn't work look at [their repository](https://github.com/novnc/websockify) for other installation options.

The end result should be that you can run the `websockify` command from your terminal.

### Running web client

From the `src/web_client` directory run the command...

```bash
websockify 8080 127.0.0.1:57054 --web=./
```

This sets up a web server and web socket bridge that servers the client's files and forwards client connections.

NOTE: you can run this on another port, but you'll have to modify the line at the top of the `script.js` file to point to the correct server.

Make sure the server is running at the `127.0.0.1:57054` address

## Terminal Client

From the `src/game_code` directory run the `client.py` script on two different machines or terminals.

NOTE: This client was used earlier in development, so the web-client is considered the "proper" way to use the application

**Additional resources:**
* https://www.python.org/doc/
* https://realpython.com/python-sockets/


## Extra Screenshots

![alt](assets/main_page.png)
![alt](assets/question.png)
![alt](assets/winner.png)
