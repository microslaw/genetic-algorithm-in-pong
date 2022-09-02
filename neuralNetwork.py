import random
import os

def fill0(num, lenght = 4):
    num = str(num)
    return ("0"*(lenght-len(num))) + num

def convert_to_fraction(string):
    return int(string)*0.0002 - 1

# 3 is used instead of e to reduce inference time
def tahn3(x):
    return  (3**x-3**(-x))/(3**x+3**(-x))

def mutate_brain(oryginalBrain):

    r = random.random()
    
    if r < 0.25:
        return swap(oryginalBrain)
    elif r < 0.5:
        return delete(oryginalBrain)
    elif r < 0.75:
        return delete(oryginalBrain)
    else:
        return change(oryginalBrain)


def swap(oryginalBrain):
    r1 = random.randrange(len(oryginalBrain))
    r2 = random.randrange(len(oryginalBrain))
    return oryginalBrain[:min(r1,r2)] + oryginalBrain[max(r1,r2)] + oryginalBrain[min(r1,r2) + 1:max(r1,r2)] + oryginalBrain[min(r1,r2)] + oryginalBrain[max(r1,r2) + 1:] 

def delete(oryginalBrain, brainSize = 16):
    if len(oryginalBrain) <= 6*brainSize:
        return add(oryginalBrain, brainSize)
    r = random.randrange(len(oryginalBrain))
    return oryginalBrain[:r] + oryginalBrain[r+1:]

def add(oryginalBrain, brainSize = 16):
    if len(oryginalBrain) > 50 + (6 * brainSize):
        return delete(oryginalBrain, brainSize)
    r1 = random.randrange(len(oryginalBrain))
    r2 = random.randrange(10)
    return oryginalBrain[:r1] + str(r2) + oryginalBrain[r1:]

def change(oryginalBrain):
    r1 = random.randrange(len(oryginalBrain))
    r2 = random.randrange(10)
    return oryginalBrain[:r1] + str(r2) + oryginalBrain[r1+1:]



class Player:
    def __init__(self, gen, playerId, brainSize, brain: str = None, parent: str = "None") -> None:
        self.name = f"player{fill0(playerId)}gen{fill0(gen)}"
        self.brainSize = brainSize
        self.gen = gen
        self.parent = parent
        self.playerId = playerId
        
# brain construction:
# (154312 x brain size) + (1523 x 5) 
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
                brain += fill0(random.randrange(1000000), lenght = 6)
            for j in range(5):
                brain += fill0(random.randrange(10000))
        self.brain = brain 
        self.load_brain()

    def load_brain(self):
        weights  = self.brain[:self.brainSize*6]
        splitWeights = [weights[(i*6)+2:(i+1)*6] for i in range(self.brainSize)]
        self.connectionIndexes = [(int(weights[(i*6)]),int(weights[(i*6)+1])) for i in range(self.brainSize)]
        self.weightsValues = [convert_to_fraction(w) for w in splitWeights]
        biases = self.brain[-40:]
        self.biasesValues = [convert_to_fraction(biases[i*4:(i+1)*4]) for i in range(5)]

# letters stand for:
# e - enemy height
# s - self height
# b - ball height
# d - ball distance
# c - bounce count

    def decide(self, enemyHeight, selfHeight, ballHeigt, ballDistance, bounceCount):
        neuronValues = [0 for i in range(10)]
        neuronValues[0] = enemyHeight/256
        neuronValues[1] = selfHeight/256
        neuronValues[2] = ballHeigt/256
        neuronValues[3] = ballDistance/256
        neuronValues[4] = bounceCount/10

        for i in range(len(self.biasesValues)):
            neuronValues[i+5] += self.biasesValues[i]

        for i in range(self.brainSize):
            neuronValues[self.connectionIndexes[i][1]] += tahn3(self.weightsValues[i] * neuronValues[self.connectionIndexes[i][0]])
        decisions = neuronValues[7:]
        return decisions.index(max(decisions))

    def save_network(self, attemptNo):
        
        file = f"\\data\\attempt{attemptNo}\\gen{fill0(self.gen)}\\players\\{self.name}.txt"
        filepath = os.getcwd() + file
        toWrite = f"{self.brain}\n"
        toWrite +=f"{self.parent}\n"
        toWrite += f"{self.brainSize}\n"

        if not os.path.exists(filepath.strip(f"\\{self.name}.txt")):
            os.makedirs(filepath.strip(f"\\{self.name}.txt"))

        with open(filepath, "w") as wfile:
            wfile.write(toWrite)

def get_player(name, attemptNo):

    gen = name.split("gen")[-1]
    playerId = str(name.split("player")[1]).split("gen")[0]
    file = f"\\data\\attempt{attemptNo}\\gen{fill0(gen)}\\players\\{name}.txt"
    filepath = os.getcwd() + file
    
    with open(filepath, 'r') as rfile:
        toRead = rfile.read()
    data = toRead.split('\n')
    return Player(gen, playerId, 16, brain = data[0])
