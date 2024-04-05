# Client.py for ServerGame
# This is what the client runs to play the game.

# Global Imports
import socket
import json
import sys
import threading
import time 
import pygame
import random

# Local Imports 
from config import HOST, PORT
from common_funcs import bite, get_hwid

# Global Variables
global hwid
hwid = get_hwid()


class CommunicationThread(threading.Thread):

    def __init__(self, name='Communication-Thread'):
        super(CommunicationThread, self).__init__(name=name)
        self.color = (0,0,0)
        self.pos = (0,0)
        self.name = hwid
        self.data = {}
        self.running = True
        
        
        

    def run(self):
        
    
        while self.running:
            #time.sleep(.001)


            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                req_dict = {
                    "cmd": "PING_INFO",
                    "hwid": hwid,
                    "color": self.color,
                    "pos": self.pos,
                    "name": self.name
                }

                tosend = bite(json.dumps(req_dict))

                # Connect to server and send data
                host = (HOST, PORT)
                sock.sendto(tosend, host)

                received = str(sock.recv(1024), "utf-8")
                data = json.loads(received)
                self.data = data
            except:
                pass
            
        return
            
            
    def update_vars(self, pos, color):
        self.pos = pos
        self.color = color
    
    def set_name(self, name):
        self.name = name
    
    def returndata(self):
        return self.data
    

    def stop(self):
        self.running = False


class GamePlayer(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.name = "You"

    def render_player(self):
        global player_pos
        # Creating the player visuals
        player = pygame.Surface((50, 50))
        player.fill(self.color)
        
        my_font = pygame.font.SysFont('Arial', 12)
        text_surface = my_font.render(self.name, False, (255, 255, 255))

        screen.blit(player, player_pos)
        screen.blit(text_surface, player_pos)


    def update(self, event_list):
        global player_pos
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

        
        self.render_player()

class MultiPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 12)

    def render(self):
        server_info.update_vars(player_pos, mycolor)
        # Here we are attempting to obtain player data
        # from our server to then render the players onto our screen
        try:
            server_info.update_vars(player_pos, mycolor)
            newplayers = server_info.data


            
            for p in newplayers:
                newplayer = pygame.Surface((50,50))                      # Creating a block
                newplayer.fill(newplayers[p]['color'])                   # Filling them in the player's color
                screen.blit(newplayer, newplayers[p]['pos'])             # Adding them to the screen
                newplayer_name = self.font.render(newplayers[p]['name'], False, (255,255,255)) # "building" their name
                screen.blit(newplayer_name, newplayers[p]['pos'])        # Adding the name to the screen
        
        # This here is just passing any errors. The above code doesn't really return any errors
        except Exception as e:
            print(f"ERROR {e}")
            pass


    def update(self, event_list):
        self.render()

class TypingInput(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 12)

if __name__ == "__main__":
    
    # Pre-Game Initialization 
    mycolor = (random.randint(30,255), random.randint(30,255), random.randint(30,255))
    server_info = CommunicationThread()
    server_info.start()

    # Game Initialization
    pygame.init()
    pygame.font.init()

    # Screen
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ServerGame")
    



    # Player position
    global player_pos
    # This just starts the player in the middle of the screen
    player_pos = [WIDTH // 2 - 25, HEIGHT // 2 - 25]
    game_player = GamePlayer(mycolor)
    other_players = MultiPlayer()
   
    # Starting The Game
    group = pygame.sprite.Group(game_player, other_players)
    running = True
    typing = False
    while running:
        time.sleep(.001)


        # Check for events
        event_list = pygame.event.get()
        #print(event_list)
        for event in event_list:
            if event.type == pygame.QUIT:
                #sys.exit()
                server_info.stop() 
                server_info.join(1)
                running = False
                pygame.quit()
                sys.exit(1)
            
            if event.type == pygame.KEYDOWN:
                #print(event.__dict__)
                #print(event.key)
                #print(event.unicode)

                if typing is True:
                    typed_string += event.unicode

                if event.unicode == "/" and typing is False:
                    typing = True
                    typed_string = ""
                
                if event.key == 13 and typing is True:
                    typing = False
                    finished_string = typed_string[0:-1]
                    server_info.set_name(finished_string)
                    game_player.name = finished_string
                    typed_string = ""
            
            

        
        screen.fill((25,25,25))
        group.update(event_list)
        pygame.display.flip()

