# server-game
A PyGame that is networked using UDP to connect players on the same screen
This project also uses multithreading to manage connections, and a game-loop.

<img src="./images/2024-04-05%2014-06-44.gif" width="500" height="300" />

## Running the Script
You first need to edit the config.py to contain the active ip and port that the server will be running on.
Then updating the client to have the same config.py on their end.

Once that is complete running the server.py file on the server is all that is needed. typing "stopall" will trigger 
the server.py to stop running.

Running the client.py script will open a pygame with a square in the middle called "You" and other players will show up as their UUID as their name.
To change your name, press / and type the desired name and hit enter. it should update what is rendered on the screen on your square with what you typed out.

Movement is as simple as the arrow keys. You are not able to leave the bounds of the screen.


## How It Communicates
Each client has a thread sending their game data in a continuous while-loop as a json that contains their UUID or HWID as it is referred to in the code, position of character, color, and desired name. 
The server also replies with a json of other player's UUIDs, colors, positions, and names.

with this data the client's are able to render a square with text onto each client's screen where each player is on their own client end.

The server tracks requests from users to determine whether or not the player has disconnected. Disconnected players are removed from what is sent to each client that is actively connected.
