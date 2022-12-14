import random
import pygame
from neuralNetwork import * 
import os
import time

bouncerHeight = 64
bouncerSpeed = 1
bounceCount = 0
IsBallIn = True
bouncer1Img, bouncer2Img = pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0)
looser: int
def sgn(x):
    if x>0:return 1
    if x == 0: return 0
    return -1

class Ball:
    def __init__(self, y, xSpeed, ySpeed) -> None:
        self.x = 128
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed * 2
        #timeModifier speeds up the ball over time (time is measured in bounces)
        self.timeModifier = 1
        #bounceSpotModifier speeds up the ball based on where it hits bouncer
        self.bounceSpotModifier = 1

    def move(self):
        dx = round(self.xSpeed * self.timeModifier)
        dy = round(self.ySpeed * self.bounceSpotModifier) 
        preSimulationX = self.x
        preSimulationY = self.y
        preSimulationDX = dx
        preSimulationDY = dy
        
        self.x += dx
        self.y += dy

        #if ball is out of bounds, backtrack to the edge of the screen where it should bounce
        if self.x>253 or self.x<2 or self.y >254 or self.y<1:
            self.x -= dx
            self.y -= dy
            sdx = sgn(dx)
            sdy = sgn(dy)


            if not self.is_bouncing():
                #breaking velocity vector into smaller to implement collision
                while (abs(dx) + abs(dy)>0):
                    if abs(dx)>abs(dy):
                        v = (round(dx/abs(dy)),sgn(dy))
                        for i in range(abs(v[0])+1):
                            if i == v[0]//2:
                                self.y +=sdy
                            else:
                                self.x +=sdx
                            if self.is_bouncing():
                                break
                    elif abs(dx)<abs(dy):
                        v = (sgn(dx),round(dy/abs(dx)))
                        for i in range(abs(v[1])+1):
                            if i == v[1]//2:
                                self.x +=sdx
                            else:
                                self.y +=sdy
                            if self.is_bouncing():
                                break
                    else:
                        v = (sgn(dx),sgn(dy))
                        self.y +=sdy
                        if self.is_bouncing():
                            break
                        self.x +=sdx
                        if self.is_bouncing():
                            break

                    dx -= v[0]
                    dy -= v[1]

        leftoverDX = preSimulationDX - (self.x - preSimulationX)
        leftoverDY = preSimulationDY - (self.y - preSimulationY)
        self.x += sgn(self.xSpeed) * leftoverDY
        self.y += sgn(self.ySpeed) * leftoverDX 


    def is_bouncing(self):


        global bounceCount


        if self.y == 0 and  self.ySpeed < 0:
            tmp = self.ySpeed
            self.ySpeed = abs(self.xSpeed)
            self.xSpeed = abs(tmp) * sgn(self.xSpeed)
            return True

        if self.y == 255 and self.ySpeed > 0:
            tmp = self.ySpeed
            self.ySpeed = abs(self.xSpeed) * -1
            self.xSpeed = abs(tmp) * sgn(self.xSpeed)
            return True

        if self.x == 1 and self.xSpeed < 0:
            self.bounceSpotModifier = p1Bouncer.get_bounce_modifier(self.y)
            tmp = self.xSpeed
            self.xSpeed = abs(self.ySpeed)
            self.ySpeed = abs(tmp) * sgn(self.ySpeed)
            bounceCount += 1
            return True

        if self.x == 254 and self.xSpeed > 0:
            self.bounceSpotModifier = p2Bouncer.get_bounce_modifier(self.y)
            tmp = self.xSpeed
            self.xSpeed = abs(self.ySpeed) * -1
            self.ySpeed = abs(tmp) * sgn(self.ySpeed)
            bounceCount += 1
            return True

        return False

class Bouncer:
    def __init__(self, posX) -> None:
        self.posX = posX
        self.lowEnd = 128 + bouncerHeight//2
        self.highEnd = 128 - bouncerHeight//2
        self.middle = 128

    def up(self):
        self.lowEnd -= bouncerSpeed
        self.middle -= bouncerSpeed
        self.highEnd -= bouncerSpeed    

    def down(self):
        self.lowEnd += bouncerSpeed
        self.middle += bouncerSpeed
        self.highEnd += bouncerSpeed    

# bounce bounceSpotModifier changes the speed of ball, if bouncer misses the ball returns 0 
    def get_bounce_modifier(self, y):
        
        global looser
        if self.lowEnd >= y and self.highEnd <= y:
            distanceToY = abs(y-self.highEnd - bouncerHeight//2)
            if distanceToY < bouncerHeight//8:
                return 2
            if distanceToY < bouncerHeight//4:
                return 1.5
            return 1
        global IsBallIn
        IsBallIn = False
        looser = sgn(self.posX)
        return 0


def play_a_game(players: tuple, seed: int = -1, doDisplay = False):
    
    global looser
    global IsBallIn
    global bounceCount
    global p1Bouncer, p2Bouncer

    p1 : Player
    p2 : Player
    p1,p2 = players
    IsBallIn  = True
    bounceCount = 0
    if seed == -1:
        seed = random.randrange(1016)


    p1Bouncer = Bouncer(0)
    p2Bouncer = Bouncer(255)
    ball = Ball(seed%254+1,(seed%2)*2-1, (((seed%4)//2))*2-1)
    timer = 0


    while IsBallIn:
        
        if doDisplay:
            draw_game(ball, p1Bouncer, p2Bouncer)

     
        timer += 1
        ball.timeModifier = round(bounceCount*bounceCount*0.01 + 1)
        ball.move()
        p1Action = p1.decide(p2Bouncer.middle, p1Bouncer.middle, ball.y, ball.x, bounceCount)
        p2Action = p2.decide(p1Bouncer.middle, p2Bouncer.middle, ball.y, 256 - ball.x, bounceCount)
        
        if p1Action == 0:
            p1Bouncer.up()
        elif p1Action == 2:
            p1Bouncer.down()

        if p2Action == 0:
            p2Bouncer.up()
        elif p2Action == 2:
            p2Bouncer.down()
    #returns data needed to save, cannot save here because does not know gen and gameId
    #log[0] is idex of winner in players; bounceCount increments on goal, -1 adresses this
    winner = int(not looser)
    log = (winner, bounceCount-1, seed)
    return log
    
def save_game(players, log: tuple, gen, gameId, attemptNo):

    file = f"\\data\\attempt{attemptNo}\\gen{fill0(gen)}\\games\\game{fill0(gameId)}gen{fill0(gen)}.txt"
    filepath = os.getcwd() + file
    toWrite = f"{players[0].name} vs {players[1].name}\n"
    toWrite +=f"{log[2]}\n"
    toWrite +=f"{log[0]}\n"
    toWrite +=f"{log[1]}\n"


    if not os.path.exists(filepath.strip(f"\\game{fill0(gameId)}gen{fill0(gen)}.txt")):
        os.makedirs(filepath.strip(f"\\game{fill0(gameId)}gen{fill0(gen)}.txt"))
    with open(filepath, 'w') as wfile:
        wfile.write(toWrite)

def replay_game(gen, gameId, attemptNo):
    initialize_drawing()
    file = f"\\data\\attempt{attemptNo}\\gen{fill0(gen)}\\games\\game{fill0(gameId)}gen{fill0(gen)}.txt"
    filepath = os.getcwd() + file
    with open(filepath, 'r') as rfile:
        toRead = rfile.read()
    data = toRead.split('\n')
    playersNames = data[0].split(" vs ")
    players = (get_player(playersNames[0], attemptNo), get_player(playersNames[1], attemptNo))
    play_a_game(players, seed = int(data[1]), doDisplay = True)

def initialize_drawing():
    pygame.init()
    global win 
    global bounceCount
    win = pygame.display.set_mode((255,255))
    pygame.display.set_caption("Pong")

def draw_game(ball, p1Bouncer: Bouncer, p2Bouncer:Bouncer):

    global bouncer1Img
    global bouncer2Img
    time.sleep(0.01)
    
    pygame.draw.rect(win, (0,0,0), pygame.Rect(bouncer1Img))
    pygame.draw.rect(win, (0,0,0), pygame.Rect(bouncer2Img))

    pygame.draw.rect(win, (255,0,0), pygame.Rect(ball.x, ball.y, 1, 1))
    pygame.draw.rect(win, (0,0,255), pygame.Rect(p1Bouncer.posX, p1Bouncer.highEnd, 1, p1Bouncer.lowEnd - p1Bouncer.highEnd))
    pygame.draw.rect(win, (0,255,0), pygame.Rect(p2Bouncer.posX-1, p2Bouncer.highEnd, 1, p2Bouncer.lowEnd - p2Bouncer.highEnd))

    bouncer1Img = pygame.Rect(p1Bouncer.posX, p1Bouncer.highEnd, 1, p1Bouncer.lowEnd - p1Bouncer.highEnd)
    bouncer2Img = pygame.Rect(p2Bouncer.posX-1, p2Bouncer.highEnd, 1, p2Bouncer.lowEnd - p2Bouncer.highEnd)

    pygame.display.update()

