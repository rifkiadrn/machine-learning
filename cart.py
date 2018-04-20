import numpy as np


class Node:
    index = None
    value = None
    groups = None
    left = None
    right = None

    def __init__(self, index, value, groups):
        self.index = index
        self.value = value
        self.groups = groups


class DecisionTreeCART():

    def __init__(self, *args, **kwargs):
        self.tree = None

    def __gini_index(self, groups, classes):

        instances = 0
        for group in groups:
            instances += float(len(group))

        gini = 0.0
        for group in groups:
            size = float(len(group))

            if size == 0:
                continue

            score = 0.0
            for val in classes:

                p = 0
                for row in group:
                    if row[-1] == val:
                        p += 1

                p = p / size
                score += p * p

            gini += (1.0 - score) * (size / instances)

        return gini

    def __make_split_group(self, index, value, dataset):
        less_than = list()
        greater_than = list()
        for row in dataset:
            if row[index] < value:
                less_than.append(row)
            else:
                greater_than.append(row)
        return less_than, greater_than

    def __get_node(dataset):

        b_index = 999
        b_value = 999
        b_score = 999
        b_groups = None

        class_values = list(set(row[-1] for row in dataset))
        feature_cols = len(dataset[0]) - 1

        for index in range(feature_cols):
            for row in dataset:
                groups = make_split_group(index, row[index], dataset)
                gini = gini_index(groups, class_values)

                if gini < b_score:
                    b_index = index
                    b_value = row[index]
                    b_score = gini
                    b_groups = groups

        return Node(b_index, b_value, b_groups)

    def __to_terminal(self, group):
        outcomes = [row[-1] for row in group]
        return max(set(outcomes), key=outcomes.count)

    def __split(node, max_depth, min_size, depth):
        left, right = node.groups
        del(node.groups)
        # check for a no split
        if not left or not right:
            node.left = node.right = self.__to_terminal(left + right)
            return
        # check for max depth
        if depth >= max_depth:
            node.left, node.right = self.__to_terminal(left),
            self.__to_terminal(right)
            return
        # process left child
        if len(left) <= min_size:
            node.left = self.__to_terminal(left)
        else:
            node.left = self.__get_node(left)
            self.__split(node.left, max_depth, min_size, depth+1)
        # process right child
        if len(right) <= min_size:
            node.right = self.__to_terminal(right)
        else:
            node.right = self.__get_node(right)
            self.__split(node.right, max_depth, min_size, depth+1)

    def __build_tree(self, train, max_depth, min_size):
        root = self.__get_split(train)
        self.__split(root, max_depth, min_size, 1)
        return root

    def print_tree(self, node, depth=0):
        if not isinstance(node, int):
            print('%s[X%d < %.3f]' %
                  ((depth*' ', (node.index+1), node.index)))
            self.print_tree(node.left, depth+1)
            self.print_tree(node.right, depth+1)
        else:
            print('%s[%s]' % ((depth*' ', node)))

    def fit(self, X, y, max_depth=10, min_size=1):
        a = np.array(X)
        b = np.array(y).reshape(len(y), 1)
        dataset = np.concatenate((a, b), axis=1)

        self.tree = self.__build_tree(dataset, max_depth, min_size)

    def __predict_row(self, node, row):
        if row[node.index] < node.value:
            if not isinstance(node.left, int):
                return self.__predict_row(node.left, row)
            else:
                return node.left
        else:
            if not isinstance(node.right, int):
                return self.__predict_row(node.right, row)
            else:
                return node.right

    def predict(self, X):
        pred = list()
        for row in X:
            prediction = self.__predict_row(self.tree, row)
            pred.append(prediction)

        return pred
