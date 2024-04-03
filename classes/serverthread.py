# ServerThread.py
# This is the server-side Game Script
# This is where GAME-BASED LOGIC WILL HAPPEN

import sqlite3
import threading
import time 
from datetime import datetime

class ServerThread(threading.Thread):

    def __init__(self, name='server-thread'):

        super(ServerThread, self).__init__(name=name)

        self.players = {}


        self.start()

    def run(self):
        
        while True:
            time.sleep(1)

            self.drop_players()

    def get_players(self, subtract=None):
        if subtract is None:
            return self.players
        else:
            templayers = {}
            for p in self.players:
                if p != subtract:
                    templayers[p] = {
                        "pos": self.players[p]['pos'],
                        "color": self.players[p]['color']
                    }
            return templayers
        
    def update_player(self, hwid, pos, color):

        if hwid not in self.players:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Player ID: {hwid} CONNECTED")

        self.players[hwid] = {
            "pos": pos,
            "color": color,
            "time": time.time()
        }

    def drop_players(self):
        newtime = time.time()
        #players_copy = self.players # This prevents a size change during iteration error
        for player in list(self.players):
            if newtime - self.players[player]['time'] > 10:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Player ID: {player} DISCONNECTED")
                del self.players[player]
