import argparse
import numpy as np
from keras.models import load_model
from environment import Environment

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True, help="Path to .keras model")
parser.add_argument("--map", type=int, default=1, help="Map id")
args = parser.parse_args()


env = Environment(120, args.map)
env.set_map(args.map)

model = load_model(args.model)


while True:
    currentState = env.reset().reshape(1, -1)
    gameOver = False

    while not gameOver:
        qvalues = model.predict(currentState, verbose=0)[0]
        action = np.argmax(qvalues)

        nextState, reward, gameOver = env.step(action)
        currentState = nextState.reshape(1, -1)