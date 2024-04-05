# The server program for 
# Server Game

import socketserver
import time
import json 
import datetime
import threading 
import sys

# Local Imports
from config import HOST, PORT
from common_funcs import bite
from classes.serverthread import ServerThread


# CREDIT TO https://docs.python.org/3/library/socketserver.html
class MyUDPHandler(socketserver.BaseRequestHandler):

    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    # def serve_forever(self):
    #     while self.running:
    #         self.handle()

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

            game_server.update_player(req_dict['hwid'], req_dict['pos'], req_dict['color'], req_dict['name'], self.client_address)
            self.socket.sendto(bite(json.dumps(game_server.get_players(req_dict['hwid']))), self.client_address)


global server 
server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)

global players
players = {}

global game_server
game_server = ServerThread()

# From https://stackoverflow.com/a/57387909
# This is what will allow me to get keyboard input while also printing new chat messages!
class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.running = True
        self.start()

    def run(self):

        while self.running:
            self.input_cbk(input()) #waits to get input + Return
        return


def my_callback(inp):
    global game_server
    global server
    if str(inp).lower() == "list":
        users = game_server.get_users()

        for user in users:
            print(f"[{user.hwid}] {'online' if user.logged_in else 'offline'}")
    
    if str(inp).lower() == "stopall":
        
        server.shutdown()
        server.server_close()   
        game_server.running = False
        game_server.join(.1)
        keyboardthread.running = False
        # This thread must be forced to shut down
        try:
            keyboardthread.join(.1)
        except:
            pass
        sys.exit()

if __name__ == "__main__":
    
    keyboardthread = KeyboardThread(my_callback)
    print("SERVER STARTING")
    server.serve_forever()
    print("SERVER ENDED")


