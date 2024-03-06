import numpy as np


class BagLearner(object):
    def __init__(self, learner, bags=20, kwargs={}, boost=False, verbose=False):
        self.learners = [learner(**kwargs) for _ in range(bags)]
        self.boost = boost
        self.verbose = verbose

    def author(self):
        return "bsun302"

    def add_evidence(self, dataX, dataY):
        n_data = dataX.shape[0]
        for learner in self.learners:
            # Create a bootstrap sample for training
            indices = np.random.choice(n_data, n_data, replace=True)
            learner.add_evidence(dataX[indices], dataY[indices])

    def query(self, points):
        # Get predictions from all learners and average them
        predictions = np.array([learner.query(points) for learner in self.learners])
        return predictions.mean(axis=0)