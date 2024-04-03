# The server program for 
# Server Game

import socketserver
import time
import json 
import datetime
import threading 

# Local Imports
from config import HOST, PORT
from common_funcs import bite
from classes.serverthread import ServerThread
#from classes.checker import CheckerThread

global players
players = {}

global game_server
game_server = ServerThread()

            


# CREDIT TO https://docs.python.org/3/library/socketserver.html
class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global game_server

        self.data = self.request[0].strip()
        self.socket = self.request[1]
        try:
            
            data = str(self.data).replace("'", "")
            data = data[1:]
        
            req_dict = json.loads(data)

        except Exception as e:

            # I do this to weed out probe requests from interrupting the IRC.
            print(f"ERROR FROM {self.client_address[0]} WITH DATA {str(self.data)}")
            return

        
        if req_dict['cmd'] == 'PING_INFO':

            game_server.update_player(req_dict['hwid'], req_dict['pos'], req_dict['color'])
            self.socket.sendto(bite(json.dumps(game_server.get_players(req_dict['hwid']))), self.client_address)


if __name__ == "__main__":


    
    # This will create the server on HOST:PORT 
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C]
        print("Server Started..")
        server.serve_forever()
        
