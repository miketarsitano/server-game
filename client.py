# Client.py for ServerGame
# This is what the client runs to play the game.

import socket
import sys
import os 
import json
import threading
import time 
import datetime
import pygame
import random

# Local Imports 
from config import HOST, PORT
from common_funcs import bite, get_hwid

# Global Variables
global hwid
hwid = get_hwid()


class PositioningThread(threading.Thread):

    def __init__(self, name='Positioning-Thread'):
        super(PositioningThread, self).__init__(name=name)
        self.color = (0,0,0)
        self.pos = (0,0)
        self.data = {}
        self.running = True
        self.start()
        

    def run(self):
        
    
        while self.running:
            #time.sleep(.001)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            req_dict = {
                "cmd": "PING_INFO",
                "hwid": hwid,
                "color": self.color,
                "pos": self.pos
            }

            tosend = bite(json.dumps(req_dict))

            # Connect to server and send data
            host = (HOST, PORT)
            sock.sendto(tosend, host)

            received = str(sock.recv(1024), "utf-8")
            data = json.loads(received)
            self.data = data
            
            
            
    
    def update_vars(self, pos, color):
        self.pos = pos
        self.color = color
    
    def returndata(self):
        return self.data
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    
    # Pre-Game Initialization 
    mycolor = (random.randint(30,255), random.randint(30,255), random.randint(30,255))
    server_info = PositioningThread()
    
    # Game Initialization
    pygame.init()
    pygame.font.init()

    # Screen
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ServerGame")
    
    # Creating the player visuals
    player = pygame.Surface((50, 50))
    player.fill(mycolor)
    
    my_font = pygame.font.SysFont('Arial', 12)
    text_surface = my_font.render('You', False, (255, 255, 255))


    # Player position
    global player_pos
    # This just starts the player in the middle of the screen
    player_pos = [WIDTH // 2 - 25, HEIGHT // 2 - 25]


    # Starting The Game
    running = True
    while running:
        time.sleep(.001)


        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #sys.exit()
                server_info.stop() # This seems to be a little bit touchy...
                running = False
                sys.exit() # This should kill the program properly, it just returns "Killed"

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Update player position 
        # This funnily ties player movement to how fast they can render the game.
        # I know I can use time and proper physics programming to fix this,
        # however this project is not about that.
        if keys[pygame.K_UP]:
            player_pos[1] -= 1
        if keys[pygame.K_DOWN]:
            player_pos[1] += 1
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 1
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 1

        #print(f"[X] {player_pos[0]} [Y] {player_pos[1]}")
        # Keeps the player on screen
        if player_pos[0] > WIDTH-50:
            player_pos[0] = WIDTH-50
        elif player_pos[0] < 0:
            player_pos[0] = 0   
        if player_pos[1] > HEIGHT-50:
            player_pos[1] = HEIGHT-50
        elif player_pos[1] < 0:
            player_pos[1] = 0
        



        """STARTING THE RENDERING"""

        # Setting the background..
        screen.fill((20,20,20))

        # Draw the player at the new position
        screen.blit(player, player_pos)
        screen.blit(text_surface, player_pos)
        pygame.display.flip()

        # Here we are attempting to obtain player data
        # from our server to then render the players onto our screen
        try:
            server_info.update_vars(player_pos, mycolor)
            newplayers = server_info.data
            for p in newplayers:
                newplayer = pygame.Surface((50,50))                      # Creating a block
                newplayer.fill(newplayers[p]['color'])                   # Filling them in the player's color
                screen.blit(newplayer, newplayers[p]['pos'])             # Adding them to the screen
                newplayer_name = my_font.render(p, False, (255,255,255)) # "building" their name
                screen.blit(newplayer_name, newplayers[p]['pos'])        # Adding the name to the screen
        
        # This here is just passing any errors. The above code doesn't really return any errors
        except Exception as e:
            print(e)
            pass



    pygame.quit()

   