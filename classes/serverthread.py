# ServerThread.py
# This is the server-side Game Script
# This is where GAME-BASED LOGIC WILL HAPPEN

import sqlite3
import threading
import time 
from datetime import datetime

from .user import User

class ServerThread(threading.Thread):

    def __init__(self, name='server-thread'):

        super(ServerThread, self).__init__(name=name)

        self.players = {}
        self.running = True

        self.start()

    def run(self):
        
        while self.running:
            time.sleep(1)

            self.drop_players()
        return

    def get_players(self, subtract=None):

        templayers = {}
        for p in self.players:
            player = self.players[p]
            if player.logged_in and player.hwid != subtract:
                templayers[p] = self.players[p].info()
        return templayers
    
    def get_users(self):
        userlist = []
        for user in self.players:
            userlist.append(self.players[user])
        return userlist

    def update_player(self, hwid, pos, color, name, address):

        newcon = False
        if hwid not in self.players:
            newcon = True
            self.players[hwid] = User(hwid, address)

        elif self.players[hwid].logged_in is False:
            newcon = True

        if newcon:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Player ID: {hwid} CONNECTED")
            self.players[hwid].logged_in = True

        self.players[hwid].update(pos, color, newcon)
        self.players[hwid].name = name
        

    def drop_players(self):
        newtime = time.time()
        #players_copy = self.players # This prevents a size change during iteration error
        for p in self.players:
            player = self.players[p]
            if (newtime - player.last_update > 10) and player.logged_in is True:
                player.logged_in = False
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Player ID: {player.hwid} DISCONNECTED")
                
