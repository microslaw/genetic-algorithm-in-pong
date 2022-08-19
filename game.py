import random
import pygame
import os

bouncerHeight = 32
bouncerSpeed = 0
bounceCount = 0
IsBallIn = True
p1Bouncer = None
p2Bouncer = None
winner = None
attemptNo = 1

def sgn(x):
    if x>0:return 1
    if x == 0: return 0
    return -1

class Ball:
    def __init__(self, y, xSpeed, ySpeed) -> None:
        self.x = 128
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        #timeModifier speeds up the ball over time (time is measured in bounces)
        self.timeModifier = 1
        #bounceModifier speeds up the ball based on where it hits bouncer
        self.bounceModifier = 1

    def move(self):
        dx = self.xSpeed * self.bounceModifier * self.timeModifier
        dy = self.ySpeed * self.bounceModifier * self.timeModifier
        self.x -= dx
        self.y -= dy

        if self.x>255 or self.x<0 or self.y >255 or self.y<0:
            self.x += dx
            self.y += dy

            #breaking velocity vector into smaller to implement collision
            while (abs(dx) + abs(dy)>0):
                if abs(dx)>abs(dy):
                    v = (round(dx/abs(dy)),sgn(dy))
                elif abs(dx)<abs(dy):
                    v = (round(dy/abs(dx)),sgn(dx))
                else:
                    v = (1,1)
                
                dx -= v[0]
                dy -= v[1]
                
                if abs(dx) > abs(dy):
                    for i in range(v[0]+1):
                        if i == v[0]//2:
                            self.y +=1
                        else:
                            self.x +=1
                        self.try_bouncing()
                else:
                    for i in range(v[1]+1):
                        if i == v[1]//2:
                            self.x +=1
                            continue
                        self.y +=1

    def try_bouncing(self):

        if self.y == 0:
            tmp = self.ySpeed
            self.ySpeed = abs(self.xSpeed)
            self.xSpeed = abs(tmp) * sgn(self.xSpeed)
            bounceCount+=1
            return 0
        if self.y == 255:
            tmp = self.ySpeed
            self.ySpeed = abs(self.xSpeed) * -1
            self.xSpeed = abs(tmp) * sgn(self.xSpeed)
            bounceCount+=1
            return 0

        if self.x == 1:
            bounceModifier = p1Bouncer.get_bounce_modifier(p1Bouncer, self.y)
            bounceCount += 1
                
        if self.x == 254:
            bounceModifier = p1Bouncer.get_bounce_modifier(p1Bouncer, self.y)
            bounceCount += 1

class Bouncer:
    def __init__(self, posX) -> None:
        self.posX = posX
        self.lowEnd = 128+bouncerHeight//2
        self.highEnd = 128-bouncerHeight//2

    def up(self):
        self.lowEnd -= bouncerSpeed
        self.highEnd -= bouncerSpeed    

    def down(self):
        self.lowEnd -= bouncerSpeed
        self.highEnd -= bouncerSpeed    

# bounce bounceModifier changes the speed of ball, if bouncer misses the ball returns 0 
    def get_bounce_modifier(self, y):
        if self.lowEnd>=y and self.highEnd<= y:
            distanceToY = abs(y-self.highEnd - bouncerHeight//2)
            if distanceToY<bouncerHeight//8:
                return 2
            if distanceToY<bouncerHeight//4:
                return 1.5
            return 1
        IsBallIn = False


def play_a_game(players: tuple, seed = random.randrange(1016)):
    p1,p2 = players
    isBallIn = True
    bounceCount = 0

    p1Bouncer = Bouncer(1)
    p2Bouncer = Bouncer(254)
    ball = Ball(seed%254+1,(seed%2)*2-1, ((seed%2)%2)*2-1)

    while isBallIn:
        ball.timeModifier = round(bounceCount*bounceCount*0.01 + 1)
        ball.move()
        
        p1Action = p1.decide()
        p2Action = p2.decide()

        if p1Action == -1:
            p1Bouncer.up()
        elif p1Action == 1:
            p1Bouncer.down()

        if p2Action == -1:
            p2Bouncer.up()
        elif p2Action == 1:
            p2Bouncer.down()

    #returns data needed to save, cannot save here because does not know gen and gameId
    #log[0] is idex of winner in players
    if ball.x == 0:
        return (0, bounceCount, seed)
    else:
        return (1, bounceCount, seed)

def fill0(num, lenght = 4):
    num = str(num)
    return ("0"*(lenght-len(num))) + num

def save_game(players, log, gen, gameId):
    file = f"\\genetic-algorithm-in-pong\\data\\attempt{attemptNo}\\gen{fill0(gen)}\\games\\game{fill0(gameId)}gen{fill0(gen)}.txt"
    filepath = os.getcwd() + file
    toWrite = f"{players[0].name} vs {players[1].name}/n"
    towrite +=f"{log[2]}/n"
    towrite +=f"{log[0]}/n"
    towrite +=f"{log[1]}/n"

    with open(filepath, 'w') as wfile:
        wfile.write(towrite)

def read_game(gen, gameId):
    file = f"\\genetic-algorithm-in-pong\\data\\attempt{attemptNo}\\gen{fill0(gen)}\\games\\game{fill0(gameId)}gen{fill0(gen)}.txt"
    filepath = os.getcwd() + file
    with open(filepath, 'r') as rfile:
        toRead = rfile.read()

def draw_game(ball, p1,p2):
    pass

print(os.path.realpath(__file__))

# with open(os.getcwd() + filepath, 'w') as wfile:
#     wfile.write("you found me")