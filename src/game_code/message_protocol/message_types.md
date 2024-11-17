# Message Types

We'll need to define several message types for this assignment.

## What messages do we need to pass?
    - Client <--- signal messages ---> Server
    - Client --- request available game lobbies ---> Server
    - Client <-- list available game lobbies --- Server
    - Client --- join lobby request ---> Server
    - Client <--- join lobby response --- Server
    - Client --- leave lobby request ---> Server
    - Client <--- leave lobby response --- Server
    - Client <--- lobby message ---> Server
    - Client --- guess request ---> Server
    - Client <--- update board state ---> Server

## How are messages passed?
    - Messages are passed between Clients and the Server as data objects using sockets (TCP)
    - Messages subclass the abstract class Event which defines an event type field and a data field plus an on_event method
    - Serialization will be as handled cleanly and efficiently as possible
    -- Json based

## How are messages handled?
    - These messages will go into an event queue and be processed by the respective server or client as events
    - Client and Server will consistently poll their event queue and take action depending on the event recieved

## General Message Format

Every message type extends the abstract Event class sent using the json packet system described in our example code.
We'll use the `action` field as the specifier for what the packet is doing, which will then
route it internally. 

Every one of the following actions are prefixed with their "category" name, 
eg. the lobby packet "get_lobby_list" will have the action name of `"action":"lobby.get_lobby_list"`. 
This makes it possible to quickly route packets to various functions/handlers 
just by testing for the `lobby.` substring.

# Lobby : `lobby.*`
 - get_lobby_list (c->s)
 - lobby_list (s->c)
    - Lobby[] lobby_ids
 - join_lobby (c->s)
    - returns lobby_ticket
 - leave_lobby (c->s)
    - lobby_ticket
 - chat_message (c->s, s->c)
    - lobby_ticket
    - String message
 - start_game (c->s)
    - lobby_ticket

# Game `game.*`

NOTE: every game message *must* have an associated lobby_id param included. This is how
the server knows where to route the message

 - game_start (server -> client)
 - game_id
 - submit_board (c->s) - Used during setup of the game, e.g. ship placement
 - begin_turn (s->c) - Tells client their turn is beginning
 - make_guess (c->s)  - Implicit End of turn
 - end_turn (c->s) - Telling the server the client is done with their move
 - update_board (s->c) - Updating client side board with new data
 - game_end (s->c)
    - who won?
