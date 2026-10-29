import numpy as np

class Prioritized_Double_Dqn():
    def __init__(self, maxMemory, discount, alpha=0.6, beta=0.4, betaIncrement=0.001, epsilon=1e-5):
        self.maxMemory = maxMemory
        self.discount = discount

        self.alpha = alpha
        self.beta = beta
        self.betaIncrement = betaIncrement
        self.epsilon = epsilon

        self.memory = list()
        self.priorities = list()
    
    def remember(self, transition, gameOver):
        self.memory.append([transition, gameOver])

        if len(self.priorities) == 0:
            maxPriority = 1.0
        else:
            maxPriority = max(self.priorities)

        self.priorities.append(maxPriority)

        if len(self.memory) > self.maxMemory:
            del self.memory[0]
            del self.priorities[0]
    
    def getBatch(self, model, target_model, batchSize):
        lenMemory = len(self.memory)
        numOutputs = model.output_shape[-1]

        actualBatchSize = min(batchSize, lenMemory)

        inputs = np.zeros((actualBatchSize, self.memory[0][0][0].shape[1]), dtype=np.float32)
        targets = np.zeros((actualBatchSize, numOutputs), dtype=np.float32)

        priorities = np.array(self.priorities, dtype=np.float32)
        probabilities = priorities ** self.alpha
        probabilities /= np.sum(probabilities)

        indexes = np.random.choice(lenMemory, size=actualBatchSize, replace=False, p=probabilities)

        weights = (lenMemory * probabilities[indexes]) ** (-self.beta)
        weights /= np.max(weights)
        weights = weights.astype(np.float32)

        tdErrors = np.zeros(actualBatchSize, dtype=np.float32)

        for i, inx in enumerate(indexes):
            currentState, action, reward, nextState = self.memory[inx][0]
            gameOver = self.memory[inx][1]

            inputs[i] = currentState[0]
            targets[i] = model.predict(currentState, verbose=0)[0]

            oldValue = targets[i][action]

            if gameOver:
                newValue = reward
            else:
                next_q_main = model.predict(nextState, verbose=0)[0]
                best_next_action = np.argmax(next_q_main)

                next_q_target = target_model.predict(nextState, verbose=0)[0]
                newValue = reward + self.discount * next_q_target[best_next_action]

            targets[i][action] = newValue
            tdErrors[i] = abs(newValue - oldValue)

        for i, inx in enumerate(indexes):
            self.priorities[inx] = tdErrors[i] + self.epsilon

        self.beta = min(1.0, self.beta + self.betaIncrement)

        return inputs, targets, weights