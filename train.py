from environment import Environment
from brain import Brain
from dqn import Dqn
from double_dqn import Double_Dqn
from per_dqn import Prioritized_Dqn
from per_double_dqn import Prioritized_Double_Dqn
import numpy as np
import csv
from keras.models import clone_model
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--exp", type=str, default="baseline", help="Experiment name")
parser.add_argument("--map", type=int, default=1, help="Map id")
parser.add_argument("--curriculum", action="store_true", help="Enable curriculum learning")
args = parser.parse_args()

experiment_name = args.exp
map_id = args.map 
use_curriculum = args.curriculum

#Defining the arameters
learningRate = 0.001
maxMemory = 60000
gamma = 0.9
batchSize = 32

updateTargetEvery = 1000
stepCounter = 0

epsilon = 1.0
epsilonDecayRate = 0.002
minEpsilon = 0.05

curriculumWindow = 50
recentScores = []

if use_curriculum:
    filepathToSave = f"models/{experiment_name}_curriculum.keras"
    csv_file = f"logs/{experiment_name}_curriculum.csv"
else:
    filepathToSave = f"models/{experiment_name}_map{map_id}.keras"
    csv_file = f"assets/logs/{experiment_name}_map{map_id}.csv"

env = Environment(0, map_id)

def update_curriculum_level(level, avg_score):
    if level == 1 and avg_score >= 2.0:
        return 2
    elif level == 2 and avg_score >= 4.0:
        return 3
    elif level == 3 and avg_score >= 5.0:
        return 4
    return level

current_level = 1 if use_curriculum else map_id
env.set_map(current_level)

state_size = env.reset().shape[0]
brain = Brain(state_size, learningRate)
model = brain.model

if experiment_name == "baseline":
    DQN = Dqn(maxMemory, gamma)
elif experiment_name == "double_dqn":
    DQN = Double_Dqn(maxMemory, gamma)
    print("Double")
elif experiment_name == "per_baseline":
    DQN = Prioritized_Dqn(maxMemory, gamma)
elif experiment_name == "per_double_dqn":
    DQN = Prioritized_Double_Dqn(maxMemory, gamma)
else:
    print("experiment necunoscut")
    exit()

target_model = clone_model(model)
target_model.set_weights(model.get_weights())


with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["epochs", "collected", "steps", "reward_total", "best_score", "snake_length", "epsilon", "level"])

def log_epochs(epochs, collected, steps, reward_total, best_score, snake_length, epsilon, level):
    with open(csv_file,"a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([epochs, collected, steps, reward_total, best_score, snake_length, epsilon, level])


epoch = 0
nCollected = 0
maxNCollected = 0
totNCollected = 0

while True:
    epoch += 1 
    
    if use_curriculum:
        env.set_map(current_level)
    
    currentState = env.reset().reshape(1, -1)
    gameOver = False
    steps = 0
    reward_total = 0
    nCollected = 0
    while not gameOver:

        stepCounter += 1
        
        if np.random.rand() <= epsilon:
            action = np.random.randint(0, 4)
        else:
            qvalues = model.predict(currentState, verbose=0)[0]
            action = np.argmax(qvalues)
        
        nextState, reward, gameOver = env.step(action)
        nextState = nextState.reshape(1, -1)
        steps += 1
        reward_total += reward
        
        
        DQN.remember((currentState, action, reward, nextState), gameOver)

        if experiment_name in ["per_baseline", "per_double_dqn"]:
            inputs, targets, weights = DQN.getBatch(model, target_model, batchSize)
            model.train_on_batch(inputs, targets, sample_weight=weights)
        else:
            inputs, targets = DQN.getBatch(model, target_model, batchSize)
            model.train_on_batch(inputs, targets)

        if stepCounter % updateTargetEvery == 0:
            target_model.set_weights(model.get_weights())
            print("Target network updated")
        
        if env.collected:
            nCollected += 1
        
        currentState = nextState
        
    epsilon -= epsilonDecayRate
    epsilon = max(epsilon, minEpsilon)
    
    if nCollected > maxNCollected:
        model.save(filepathToSave)
        maxNCollected = nCollected
    
    snake_length = len(env.SnakePos)
    log_epochs(epoch, nCollected, steps, reward_total, maxNCollected, snake_length, epsilon, current_level)
    totNCollected += nCollected

    if use_curriculum:
        recentScores.append(nCollected)

        if len(recentScores) > curriculumWindow:
            recentScores.pop(0)
        
        avg_score = sum(recentScores) / len(recentScores)
        new_level = update_curriculum_level(current_level, avg_score)
        if new_level != current_level:
            old_level = current_level
            current_level = new_level

            epsilon = max(epsilon, 0.30)

            print(f"[CURRICULUM] Epoch {epoch} | Level {old_level} -> {current_level} | AvgScore: {avg_score:.2f}")
    
    nCollected = 0
    
    print("Epoch: " + str(epoch) + " Level: " + str(current_level) + " Current Best: " + str(maxNCollected) + " Epsilon: {:.5}".format(epsilon))