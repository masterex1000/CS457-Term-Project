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


## Web Client **`HIGHLY RECOMMENDED`**

The web client relies on a [websockify](https://github.com/novnc/websockify)
server running to forward websocket connections to the tcp server.

This allows the web-client to natively talk to the python tcp server using the
same message protocol the terminal client does, while also taking care of
hosting the client files.

### Install `websockify`

To run the web client you'll first need to install `websockify`. 

1. *recommended* Install using the `requirements.txt` file, then run using
   `python3 -m websockify`
- If you're using Debian (or any other OS setup to use an externally managed python environment) and you want to install `websockify` globally you can install it with `sudo apt install python3-websockify`
- If you're using another setup you should be able to run `pip3 install websockify`.
- If that doesn't work look at [their repository](https://github.com/novnc/websockify) for other installation options.

### Running web client

You can start the web client server using the `run_web_client.sh` script in the
root of the repository. This takes the same arguments as the deliverables
mentions, plus a couple extra.

```
./run_web_client.sh -i localhost -p 57054 -w 0.0.0.0 -n 8080
```

The client will automatically connect to the websocket hosted by the web server.

#### Running the web client manually

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

```bash
python3 client.py -i localhost -p 57054
```

**Additional resources:**
* https://www.python.org/doc/
* https://realpython.com/python-sockets/


## Extra Screenshots

![alt](assets/main_page.png)
![alt](assets/question.png)
![alt](assets/winner.png)
