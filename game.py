import random
import this
import pygame

bouncerHeight = 32
bouncerSpeed = 0
bounceCount = 0
IsBallIn = True
p1Bouncer = None
p2Bouncer = None
winner = None

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
        self.modifier

    def move(self):
        dx = self.xSpeed * self.modifier
        dy = self.ySpeed * self.modifier
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
            modifier = p1Bouncer.get_bounce_modifier(p1Bouncer, self.y)
            bounceCount += 1
                
        if self.x == 254:
            modifier = p1Bouncer.get_bounce_modifier(p1Bouncer, self.y)
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

# bounce modifier changes the speed of ball, if bouncer misses the ball returns 0 
    def get_bounce_modifier(self, y):
        if self.lowEnd>=y and self.highEnd<= y:
            distanceToY = abs(y-self.highEnd - bouncerHeight//2)
            if distanceToY<bouncerHeight//8:
                return 2
            if distanceToY<bouncerHeight//4:
                return 1.5
            return 1
        IsBallIn = False


def play_a_game(players, seed = random.randrange(1016)):
    p1,p2 = players
    isBallIn = True
    bounceCount = 0

    p1Bouncer = Bouncer(1)
    p2Bouncer = Bouncer(254)
    ball = Ball()

    while isBallIn:

        ball.move()
        
        p1Action = p1.decide()
        p2Action = p2.decide()

        
        if p1Action == "up":
            p1Bouncer.up()
        elif p1Action == "down":
            p1Bouncer.down()

        if p2Action == "up":
            p2Bouncer.up()
        elif p2Action == "down":
            p2Bouncer.down()

    if ball.x == 0:
        return 0
    else:
        return 1



def read_game(filename):
    with open(filename, 'r') as rfile:
        return rfile.read()

def save_game(filename):
    with open(filename, 'w') as wfile:
        return wfile.write()

def draw_game(ball, p1,p2):
    pass

