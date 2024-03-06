import numpy as np


class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return "bsun302"

    def add_evidence(self, dataX, dataY):
        self.tree = self.build_tree(dataX, dataY)
        if self.verbose:
            print("RT tree size:", self.tree.shape)

    def query(self, points):
        return np.array([self.predict(point) for point in points])

    def build_tree(self, dataX, dataY):
        if dataX.shape[0] <= self.leaf_size or len(np.unique(dataY)) == 1:
            return np.array([[np.nan, np.mean(dataY), np.nan, np.nan]])

        random_feature_index = self.random_feature(dataX)
        split_val = np.median(dataX[:, random_feature_index])

        left_mask = dataX[:, random_feature_index] <= split_val
        if np.all(left_mask) or np.all(~left_mask):
            return np.array([[np.nan, np.mean(dataY), np.nan, np.nan]])

        left_tree = self.build_tree(dataX[left_mask], dataY[left_mask])
        right_tree = self.build_tree(dataX[~left_mask], dataY[~left_mask])

        root = np.array([random_feature_index, split_val, 1, left_tree.shape[0] + 1 if left_tree.ndim > 1 else 2])
        return np.vstack((root, left_tree, right_tree))

    def predict(self, point):
        node = 0
        while not np.isnan(self.tree[node, 0]):
            split_feature = int(self.tree[node, 0])
            split_val = self.tree[node, 1]
            node += int(self.tree[node, 2] if point[split_feature] <= split_val else self.tree[node, 3])
        return self.tree[node, 1]

    def random_feature(self, dataX):
        np.random.seed(42)
        return np.random.randint(dataX.shape[1])
