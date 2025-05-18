import matplotlib.pyplot as plt
import pandas as pd
from data import assignment_data
from id3 import id3
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree


def transform_data(data):
    result = {}
    for col in data[0]:
        result.update({col: []})

    for row in data:
        for col, value in row.items():
            result[col].append(value)
    del result["ID"]
    return result


def generate_trees(data):
    df = pd.DataFrame(data)

    mappings = {}
    for col in df.columns[:-1]:
        df[col], mappings[col] = df[col].astype("category").factorize(sort=True)

    df["Risco"], class_mapping = df["Risco"].astype("category").factorize(sort=True)

    X = df.drop("Risco", axis=1)
    Y = df["Risco"]

    id3 = DecisionTreeClassifier(criterion="entropy")
    id3.fit(X, Y)

    c45 = DecisionTreeClassifier(criterion="entropy")
    c45.fit(X, Y)

    cart = DecisionTreeClassifier(criterion="gini")
    cart.fit(X, Y)

    # Função para converter os números de volta para as categorias originais
    def convert_tree_to_text(tree, feature_names):
        tree_rules = export_text(
            tree, feature_names=feature_names, class_names=class_mapping.tolist()
        )
        for feature, mapping in mappings.items():
            for i, category in enumerate(mapping):
                tree_rules = tree_rules.replace(f"[X{i}]", category)
        return tree_rules

    print("\nÁrvore de Decisão ID3:")
    print(convert_tree_to_text(id3, list(X.columns)))

    print("\nÁrvore de Decisão C4.5 (Simulado):")
    print(convert_tree_to_text(c45, list(X.columns)))

    print("\nÁrvore de Decisão CART:")
    print(convert_tree_to_text(cart, list(X.columns)))

    plt.figure(figsize=(12, 6))
    plot_tree(
        id3, feature_names=X.columns, class_names=class_mapping.tolist(), filled=True
    )
    plt.title("Árvore de Decisão id3")
    plt.savefig("id3.jpg")

    plt.figure(figsize=(12, 6))
    plot_tree(
        c45, feature_names=X.columns, class_names=class_mapping.tolist(), filled=True
    )
    plt.title("Árvore de Decisão c45")
    plt.savefig("c45.jpg")

    plt.figure(figsize=(12, 6))
    plot_tree(
        cart, feature_names=X.columns, class_names=class_mapping.tolist(), filled=True
    )
    plt.title("Árvore de Decisão CART")
    plt.savefig("cart.jpg")


def generate_id3(data):
    df = pd.DataFrame(data)

    X = df.drop("Risco", axis=1)
    Y = df["Risco"]
    tree = id3(X, Y)
    print(tree)


if __name__ == "__main__":
    data = transform_data(assignment_data)
    generate_id3(data)
