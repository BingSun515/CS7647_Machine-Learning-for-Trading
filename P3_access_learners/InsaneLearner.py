import numpy as np
from LinRegLearner import LinRegLearner
from BagLearner import BagLearner
class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.learners = [BagLearner(learner=LinRegLearner, kwargs={}, bags=20, boost = False, verbose=verbose) for _ in range(20)]
    def add_evidence(self, dataX, dataY):
        for learner in self.learners:
            learner.add_evidence(dataX, dataY)
    def query(self, points):
        predictions = np.array([learner.query(points) for learner in self.learners])
        return predictions.mean(axis=0)
    def author(self):
        return "bsun302"