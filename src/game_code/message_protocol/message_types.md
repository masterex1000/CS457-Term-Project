# Message Types

We'll need to define several message types for this assignment.

## What messages do we need to pass?
    - Client <--- signal messages ---> Server
    - Client --- guess ---> Server
    - Client <--- update board state ---> Server

## How are messages passed?
    - Messages are passed between Clients and the Server as data objects using sockets (TCP)
    - Serialization will be as handled cleanly and efficiently as possible
    -- Json based?

## How are messages handled?
    - These messages will go into an event queue and be processed by the respective server or client as events
    - Client and Server will consistently poll their event queue and take action depending on the event recieved

## General Message Format

Every message is sent using the json packet system described in our example code.
We'll use the `action` field as the specifier for what the packet is doing, which will then
route it internally. 

Every one of the following actions are prefixed with their "category" name, 
eg. the lobby packet "getLobbyList" will have the action name of `"action":"lobby.getLobbyList"`. 
This makes it possible to quickly route packets to various functions/handlers 
just by testing for the `lobby.` substring.

# Lobby : `lobby.*`
 - getLobbyList (c->s)
 - lobbyList (s->c)
    - Lobby[] lobby_ids
 - joinLobby (c->s)
    - returns lobby_ticket
 - leaveLobby (c->s)
    - lobbyTicket
 - chatMessage (c->s, s->c)
    - lobbyTicket
    - String message
 - startGame (c->s)
    - lobbyTicket

# Game `game.*`
 - gameStart (server -> client)
 - game_id
 - submitBoard (c->s)
 - beginTurn (s->c) - Tells client their turn is beginning
 - makeGuess (c->s)  - Implicit End of turn
 - endTurn (c->s) - Telling the server the client is done with their move
 - updateBoard (s->c) - Updating client side board with new data
 - gameEnd (s->c)
    - who won?
