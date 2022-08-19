from itertools import count
import random
from turtle import distance
import numpy

def fill0(num, lenght = 4):
    num = str(num)
    return ("0"*(lenght-len(num))) + num

def decode_string(string):
    return int(string)*0.0002 - 1

class Player:
    def __init__(self, gen, playerId, brainSize, brain: str = None) -> None:
        self.name = f"game{fill0(playerId)}gen{fill0(gen)}"
        self.brainSize = brainSize
        
# brain construction:
# (154312 x brain size) + (1523 x 10) 
# first two digits are indexes of neurons they are connecting, with the latter being altered. Identical digits result in neuron changing its own value
# This allows for connection of neurons in the same layer as well as RNN
# four latter digits represent weight of a connection
# number of connections is described by brain size. It is followed by five biases of five different non-input neurons.
# ten neurons consist of 5 inputs, 3 outputs and 2 hidded. Note that such network is sparse
# if lenght of the brain is too small encoded weights and biases will overlap, however there is upper limit of lenght in order to force the most important connections
# weights and biases are later processed with f(x) = 2 * x * 0,0001 -1 to allow for negative values at the cost of precision
        
        if brain == None:
            brain = ""
            for i in range(brainSize):
                brain += fill0(random.randrange(1000000), lenght = 6*brainSize)
            for j in range(5):
                brain += fill0(random.randrange(10000))
        self.brain = brain 


    def load_brain(self):
        weights  = self.brain[:self.brainSize*6]
        splitWeights = (weights[(i*6)+2:(i+1)*6] for i in range(self.brainSize))
        connectionIndexes = ((weights[(i*6)],weights[(i*6)+1]) for i in range(self.brainSize))
        self.weightsValues = (decode_string(w) for w in splitWeights)
        biases = self.brain[-40:]
        self.biasesValues = (decode_string(biases[i*4:(i+1)*4]) for i in range(5))

        

# letters stand for:
# e - enemy height
# s - self height
# b - ball height
# d - ball distance
# c - bounce count

    def decide(self, enemyHeight, selfHeight, ballHeigt, ballDistance, bounceCount):
        neuronValues = [b for b in self.biasesValues]

player = Player(0,0,16,fill0(random.randint(10**136))).decide()

