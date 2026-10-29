import keras
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Input
from keras.optimizers import Adam

class Brain():
    def __init__(self, inputSize, lr = 0.005):
        self.inputSize = inputSize
        self.learningRate = lr
        self.numOutputs = 4
        
        self.model = Sequential()

        self.model.add(Input(shape=(self.inputSize,)))
        self.model.add(Dense(128, activation="relu"))
        self.model.add(Dense(128, activation="relu"))
        self.model.add(Dense(self.numOutputs, activation="linear"))

        self.model.compile(optimizer = Adam(learning_rate = self.learningRate), loss = "mean_squared_error")
    
    def loadModel(self, filepath):
        self.model = load_model(filepath)
        return self.model
