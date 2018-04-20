import numpy as np

from .utils.data_manipulations import divide_on_feature, train_test_split, standardize
from .utils.functions import calculate_entropy, accuracy_score, calculate_variance, mean_squared_error

class Node():

    def __init__(self, feature_index=None, threshold=None, value=None, true_branch=None, false_branch=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.value = value
        self.true_branch = true_branch
        self.false_branch = false_branch

class DecisionTree(object):
    
    def __init__(self, min_samples_split=2, min_impurity=1e-5, max_depth=3, loss=None):
        self.root = None
        self.min_samples_split = min_samples_split
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        self._impurity_calculation = None
        self._leaf_value_calculation = None
        self.one_dim = None
        self.loss = loss
    
    def fit(self, X, y, loss=None):
        self.one_dim = len(np.shape(y)) == 1
        self.root = self._build_tree(X, y)
        self.loss = None
    
    def _build_tree(self, X, y, current_depth=0):
        largest_impurity = 0
        best_criteria = None
        best_sets = None

        if len(np.shape(y)) == 1:
            y = np.expand_dims(y, axis=1)
        
        Xy = np.concatenate((X, y), axis=1)

        n_samples, n_features = np.shape(X)

        if n_samples >= self.min_samples_split and current_depth <= self.max_depth:
            
            for feature_index in range(n_features):
                feature_values = np.expand_dims(X[:, feature_index], axis=1)
                unique_value = np.unique(feature_values)

                for threshold in unique_value:
                    Xy1, Xy2 = divide_on_feature(Xy, feature_index, threshold)

                    if len(Xy1) > 0 and len(Xy2) > 0:
                        y1 = Xy1[:, n_features:]
                        y2 = Xy2[:, n_features:]

                        impurity = self._impurity_calculation(y, y1, y2)

                        if impurity > largest_impurity:
                            largest_impurity = impurity
                            best_criteria = {"feature_index": feature_index, "threshold": threshold}
                            best_sets = {
                                "leftX": Xy1[:, :n_features],
                                "lefty": Xy1[:, n_features:],
                                "rightX": Xy2[:, :n_features],
                                "righty": Xy2[:, n_features:]
                            }
        
        if largest_impurity > self.min_impurity:
            true_branch = self._build_tree(best_sets["leftX"], best_sets["lefty"], current_depth + 1)
            false_branch = self._build_tree(best_sets["rightX"], best_sets["righty"], current_depth + 1)
            return Node(feature_index=best_criteria["feature_index"], threshold=best_criteria[
                "threshold"], true_branch=true_branch, false_branch=false_branch)
        
        leaf_value = self._leaf_value_calculation(y)

        return Node(value=leaf_value)

    def predict_value(self, x, tree=None):
        
        if tree is None:
            tree = self.root
        
        if tree.value is not None:
            return tree.value
        
        feature_value = x[tree.feature_index]

        branch = tree.false_branch
        if isinstance(feature_value, int) or isinstance(feature_value, float):
            if feature_value >= tree.threshold:
                branch = tree.true_branch
        elif feature_value == tree.threshold:
            branch = tree.true_branch
        
        return self.predict_value(x, branch)
    
    def predict(self, X):
        y_pred = []
        for x in X:
            y_pred.append(self.predict_value(x))
        return y_pred
    
    def print_tree(self, tree=None, indent=" "):
        """ Recursively print the decision tree """
        if not tree:
            tree = self.root

        # If we're at leaf => print the label
        if tree.value is not None:
            print (tree.value)
        # Go deeper down the tree
        else:
            # Print test
            print ("%s:%s? " % (tree.feature_index, tree.threshold))
            # Print the true scenario
            print ("%sT->" % (indent))
            self.print_tree(tree.true_branch, indent + indent)
            # Print the false scenario
            print ("%sF->" % (indent))
            self.print_tree(tree.false_branch, indent + indent)

class RegressionTree(DecisionTree):
    def _calculate_variance_reduction(self, y, y1, y2):
        var_total = calculate_variance(y)
        var_1 = calculate_variance(y1)
        var_2 = calculate_variance(y2)
        frac_1 = len(y1) / len(y)
        frac_2 = len(y1) / len(y)

        variance_reduction = var_total - (frac_1 * var_1 + frac_2 * var_2)

        return sum(variance_reduction)
    
    def _mean_of_y(self, y):
        value = np.mean(y, axis=0)
        return value if len(value) > 1 else value[0]
    
    def fit(self, X, y):
        self._impurity_calculation = self._calculate_variance_reduction
        self._leaf_value_calculation = self._mean_of_y
        super(RegressionTree, self).fit(X, y)

class ClassificationTree(DecisionTree):
    def _calculate_information_gain(self, y, y1, y2):
        p = len(y1) / len(y)
        entropy = calculate_entropy(y)
        info_gain = entropy - p * \
            calculate_entropy(y1) - (1 - p) * \
            calculate_entropy(y2)

        return info_gain
    
    def _majority_vote(self, y):
        most_common = None
        max_count = 0
        for label in np.unique(y):
            # Count number of occurences of samples with label
            count = len(y[y == label])
            if count > max_count:
                most_common = label
                max_count = count
        return most_common

    def fit(self, X, y):
        self._impurity_calculation = self._calculate_information_gain
        self._leaf_value_calculation = self._majority_vote
        super(ClassificationTree, self).fit(X, y)