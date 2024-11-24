from collections import defaultdict
import numpy as np

class MarkovModel:
    def __init__(self):
        self.transition_matrix = defaultdict(lambda: defaultdict(float))
    
    def train(self, data):
        for i in range(len(data) - 1):
            state = data [i]
            next_state = data[i + 1]
            self.transition_matrix[state][next_state] += 1

        # Normalize transitions
        for state, transitions in self.transition_matrix.items():
            total = sum(transitions.values())
            for next_state in transitions:
                transitions[next_state] /= total

    def predict_next_state(self, state):
        if state not in self.transition_matrix:
            return None
        next_states = list(self.transition_matrix[state].keys())
        probabilities = list(self.transition_matrix[state].values())
        return np.random.choice(next_states, p=probabilities)
    
model = MarkovModel()
model.train(historical_data)