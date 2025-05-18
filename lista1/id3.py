import numpy as np


class Node:
    def __init__(self, attribute=None, value=None, children=None, label=None):
        self.attribute = attribute
        self.value = value
        self.children = children if children is not None else {}
        self.label = label

    def is_leaf(self):
        return self.label is not None

    def __repr__(self, level=0):
        indent = "    " * level
        if self.is_leaf():
            return f"{self.label}\n"
        result = f"[{self.attribute}]\n"
        for value, child in self.children.items():
            result += f"{indent}--({value})--> {child.__repr__(level + 1)}"
        return result


def entropy(y):
    values, counts = np.unique(y, return_counts=True)
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs))


def information_gain(X, y, attribute):
    total_entropy = entropy(y)
    values, counts = np.unique(X[attribute], return_counts=True)

    weighted_entropy = sum(
        (counts[i] / len(y)) * entropy(y[X[attribute] == values[i]])
        for i in range(len(values))
    )
    return total_entropy - weighted_entropy


def best_attribute(X, y):
    return max(X.columns, key=lambda attr: information_gain(X, y, attr))


def id3(X, y):
    if len(np.unique(y)) == 1:
        return Node(label=y.iloc[0])

    if X.empty:
        return Node(label=y.mode()[0])

    best_attr = best_attribute(X, y)
    root = Node(attribute=best_attr)

    for value in X[best_attr].unique():
        subset_X = X[X[best_attr] == value].drop(columns=[best_attr])
        subset_y = y[X[best_attr] == value]

        root.children[value] = id3(subset_X, subset_y)

    return root
