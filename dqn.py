import numpy as np

class Dqn():
    def __init__(self, maxMemory, discount):
        self.maxMemory = maxMemory
        self.discount = discount
        self.memory = list()
    
    def remember(self, transition, gameOver):
        self.memory.append([transition, gameOver])
        if len(self.memory) > self.maxMemory:
            del self.memory[0]
    
    def getBatch(self, model, target_model, batchSize):
        lenMemory = len(self.memory)
        numOutputs = model.output_shape[-1]
        
        inputs = np.zeros((min(batchSize, lenMemory), self.memory[0][0][0].shape[1]), dtype=np.float32)
        targets = np.zeros((min(batchSize, lenMemory), numOutputs), dtype=np.float32)
        
        for i, inx in enumerate(np.random.randint(0, lenMemory, size = min(batchSize, lenMemory))):
            currentState, action, reward, nextState = self.memory[inx][0]
            gameOver = self.memory[inx][1]
            
            inputs[i] = currentState[0]
            targets[i] = model.predict(currentState, verbose=0)[0]

            if gameOver:
                targets[i][action] = reward
            else:
                next_q_values = target_model.predict(nextState, verbose=0)[0]
                targets[i][action] = reward + self.discount * np.max(next_q_values)
        
        return inputs, targets