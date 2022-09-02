import random
import pygame
from game import * 
from neuralNetwork import *


#paramaters:
attemptNo = 5
#attemptNo refers to different versions with changed global parameters and bugfixes 
brainSize = 16
populationSize = 5000
maxGenerations = 5000

#Generate first players
players: list[Player] = []
generation = 0
for i in range(populationSize):
    players.append(Player(generation, i, brainSize))
    players[i].save_network(attemptNo)

training_results = ""
while generation <= maxGenerations:
    maxBounceCount = 0
    averageBounceCount = 0
    generation+=1
    for i in range(0, len(players), 2):
        log = play_a_game((players[i],players[i+1]))
        save_game((players[i],players[i+1]), log, generation, i, attemptNo )
        winner = log[0]
        looser = 0 if log[0] == 1 else 1
        players[i+looser] = Player(generation, players[i+looser].playerId, brainSize, mutate_brain(players[i+winner].brain), players[i+winner].name)
        players[i+looser].save_network(attemptNo)
        averageBounceCount += log[1]
        if maxBounceCount< log[1]:
            maxBounceCount =  log[1]
            maxBounceCountId = i
    averageBounceCount /= len(players)/2
    training_result = f"Generation: {fill0(generation)}; Highest bounces: {fill0(maxBounceCount, 2)} in game {fill0(maxBounceCountId)}; Average bounces per game: {averageBounceCount};"
    training_results += training_result + "\n"
    print(training_result)
    random.shuffle(players)


    with open(os.getcwd() + f"\\data\\attempt{attemptNo}\\training_log.txt", "w") as wfile:
        wfile.write(training_results)




