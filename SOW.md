## Project Title:

Battleship

## Team:

Collin Conrad
Jeff Jernberg

## Project Objective:

[Briefly describe the goal of the project. What problem are you trying to solve or what functionality are you aiming to achieve?]

Create a networked battleship game using a client-server architecture. To start
with, we're only aiming of a terminal based client, however we are leaving room
open for a graphical interface.

## Scope:

### Inclusions:

 - A fully functional battleship game where users can play each other.

[List the specific tasks, features, or components that will be included in the project.]

### Exclusions:

 - No variations, just standard battleship. Initially just a terminal based ui.
 - Just player versus player, no tournament modes or anything else.

[List any tasks, features, or components that will not be included in the project.]

## Deliverables:

[List the expected outputs or deliverables from the project, such as a working Python script, documentation, or presentations.]

 - Server python script
 - Client terminal python script
 - A how to play guide

## Timeline:

### Key Milestones:

Required Milestones

 - October 6th, Have client/server that can connect to each other.
 - October 20th, Have networking protocol figured out
 - Nov 3th, Multi-player functionality, and be able to synchronize game state
between games.
 - Nov 17th, Have fully functional base game, and potentially graphical client.
 - Dec 6th, Fully vetted error handling.

Our Milestones (In kindof order)

 - Have base game logic implemented (so we can run automated game tests etc)
 - Standardize basic networking protocol
 - Base server implementation
 - Base client implementation
 - Fully implement terminal based client and server
 - Potentially work on graphical client

### Task Breakdown:

[Create a detailed breakdown of tasks, assigning estimated hours or days to each.]

 - Implement base battleship game logic (should me modular so we can build
server on top)
 - Build out and design message protocol
 - Implement basic server/client on top of game logic module
 - Polish
 - Extend, maybe implement web UI and graphical interface
## Technical Requirements:

### Hardware:

 - Server (running on a computer)
 - Clients (at least two) (also running on computer)
 - Networking connection between them

### Software:

 - Python (Standard library should be enough for tui)
 - Code editor
 - Git
 - GitHub
 - *Possibly* graphics library if needed, *Possibly* cryptography library

## Assumptions:

[State any assumptions that are being made about the project, such as network connectivity or availability of resources.]

 - We assume there is a server and client, that the clients have a valid network
connection to the server, and that all systems can run python/listen on ports
and make connections.

## Roles and Responsibilities:

[Define the roles of team members, including project manager, developers, testers, etc., and their responsibilities.]

Since we're a team of two, we don't have a very specified management structure.
Most of the project will be done via pair programming, with other task being
well defined by talking to each other and completed on our own.

## Communication Plan:

 - We're planning on communicating via teams with text messaging an emergency
   backup.
 - We're hoping to set some standard meetings throughout the week/project time
   to meet and discuss project goals/requirements, as well as complete some
coding.  This will change throughout


## Additional Notes:

N/A
