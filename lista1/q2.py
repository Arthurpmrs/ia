import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from data import assignment_data
from sklearn.model_selection import train_test_split
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


def main(data):
    df = pd.DataFrame(data)

    # Convertendo atributos categóricos para numéricos
    for col in df.columns[:-1]:
        df[col] = df[col].astype("category").cat.codes

    X = df.drop("Risco", axis=1)
    Y = df["Risco"].astype("category").cat.codes
    print(set(zip(Y, df["Risco"])))

    # --- ID3 ---
    id3 = DecisionTreeClassifier(criterion="entropy")  # ID3 usa entropia
    id3.fit(X, Y)

    # --- C4.5 (Simulado, pois sklearn não implementa poda automaticamente) ---
    c45 = DecisionTreeClassifier(criterion="entropy")  # C4.5 também usa entropia
    c45.fit(X, Y)

    # --- CART ---
    cart = DecisionTreeClassifier(criterion="gini")  # CART usa índice de Gini
    cart.fit(X, Y)

    print(X.columns)
    # Exibir regras das árvores
    print("\nÁrvore de Decisão ID3:")
    print(export_text(id3, feature_names=list(X.columns)))

    print("\nÁrvore de Decisão C4.5 (Simulado):")
    print(export_text(c45, feature_names=list(X.columns)))

    print("\nÁrvore de Decisão CART:")
    print(export_text(cart, feature_names=list(X.columns)))

    # # Visualização gráfica da árvore CART
    # plt.figure(figsize=(12, 6))
    # plot_tree(
    #     cart,
    #     feature_names=X.columns,
    #     class_names=["Baixo", "Moderado", "Alto"],
    #     filled=True,
    # )
    # plt.title("Árvore de Decisão CART")
    # plt.savefig("tree.png")


if __name__ == "__main__":
    data = transform_data(assignment_data)
    main(data)
