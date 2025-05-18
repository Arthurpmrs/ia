import math


def get_attribute(data: list[dict], attr: str) -> list[str]:
    return [d[attr] for d in data if attr in d]


def get_subsets(attr_col: list[str], target_col: list[str]):
    target_subset = {}
    for target_class in set(target_col):
        target_subset.update({target_class: 0})

    subsets = {}
    for attr, target in zip(attr_col, target_col):
        if attr not in subsets:
            subsets[attr] = {**target_subset}

        subsets[attr][target] += 1
    return subsets


def get_class_entropy(subset: dict) -> float:
    n = sum([ni for ni in subset.values()])

    entropy = 0
    for ni in subset.values():
        p = ni / n
        if p > 0:
            entropy += p * math.log(p, 2)

    return -entropy


def get_class_entropy_equation(subset: dict) -> str:
    n = sum([ni for ni in subset.values()])
    s = "-("
    for i, ni in enumerate(subset.values()):
        s += f"{ni}/{n} * log_2({ni}/{n})"
        if i < len(subset) - 1:
            s += " + "
    s += ")"
    return s


def get_attr_entropy(class_subsets: dict[dict]) -> dict:
    entropy = {}
    for attr_class, subset in class_subsets.items():
        entropy.update(
            {
                attr_class: {
                    "entropy": get_class_entropy(subset),
                    "count": sum([ni for ni in subset.values()]),
                    "equation": get_class_entropy_equation(subset),
                }
            }
        )
    return entropy


def get_knowledge_gain(
    set_size: int, set_entropy: float, attr_entropy: dict[str, dict]
) -> float:
    sum = 0
    for info in attr_entropy.values():
        entropy, count, _ = info.values()
        sum += count / set_size * entropy
    return set_entropy - sum


def get_knowledge_gain_equation(
    set_size: int, set_entropy: float, attr_entropy: dict[str, dict]
) -> str:
    s = f"{set_entropy:.3f} - ("
    for i, info in enumerate(attr_entropy.values()):
        entropy, count, _ = info.values()
        s += f"{count} / {set_size} * {entropy:.3f}"
        if i < len(attr_entropy) - 1:
            s += " + "
    s += ")"
    return s


def get_attr_class_count(attr: list) -> dict:
    result = {}
    for i in attr:
        result[i] = result.get(i, 0) + 1
    return result


def calculate_entropy_of_attr(data: list[dict], attr: str, target: str):
    print("-----------------------------------------")
    n = len(data)
    Hs = get_class_entropy(get_attr_class_count(get_attribute(data, target)))
    print(f"{n=}, H(S)={Hs:.3f}")
    print(attr)
    attr_col = get_attribute(data, attr)
    target_col = get_attribute(data, target)

    subsets = get_subsets(attr_col, target_col)
    entropy = get_attr_entropy(subsets)

    # Print classes
    for (attr_class, subset), info in zip(subsets.items(), entropy.values()):
        print(f"    {attr_class} = {subset}")
        print(f"        s = {info['equation']} = {info['entropy']:.3f}")

    A = get_knowledge_gain(n, Hs, entropy)
    print(f"    G = {get_knowledge_gain_equation(n, Hs, entropy)} = {A:.3f}")


def calculate_level_1(data: list):
    calculate_entropy_of_attr(data, "Historia de Crédito", "Risco")
    calculate_entropy_of_attr(data, "Dívida", "Risco")
    calculate_entropy_of_attr(data, "Garantia", "Risco")
    calculate_entropy_of_attr(data, "Renda", "Risco")


def calculate_0a15(data: list):
    data = [d for d in data if d["Renda"] == "$0 a $15k"]
    for d in data:
        print(d)

    calculate_entropy_of_attr(data, "Historia de Crédito", "Risco")
    calculate_entropy_of_attr(data, "Dívida", "Risco")
    calculate_entropy_of_attr(data, "Garantia", "Risco")


def calculate_15a35(data: list):
    data = [d for d in data if d["Renda"] == "$15 a $35k"]
    for d in data:
        print(d)

    calculate_entropy_of_attr(data, "Historia de Crédito", "Risco")
    calculate_entropy_of_attr(data, "Dívida", "Risco")
    calculate_entropy_of_attr(data, "Garantia", "Risco")


def calculate_15a35_nenhuma(data: list):
    data = [
        d for d in data if d["Renda"] == "$15 a $35k" and d["Garantia"] == "Nenhuma"
    ]
    for d in data:
        print(d)

    calculate_entropy_of_attr(data, "Historia de Crédito", "Risco")
    calculate_entropy_of_attr(data, "Dívida", "Risco")


def calculate_15a35_nenhuma_descon(data: list):
    data = [
        d
        for d in data
        if d["Renda"] == "$15 a $35k"
        and d["Garantia"] == "Nenhuma"
        and d["Historia de Crédito"] == "Desconhecida"
    ]
    for d in data:
        print(d)

    calculate_entropy_of_attr(data, "Dívida", "Risco")


def calculate_15a35_adequada(data: list):
    data = [
        d for d in data if d["Renda"] == "$15 a $35k" and d["Garantia"] == "Adequada"
    ]
    for d in data:
        print(d)
    calculate_entropy_of_attr(data, "Historia de Crédito", "Risco")
    calculate_entropy_of_attr(data, "Dívida", "Risco")


def calculate_0a35(data: list):
    data = [d for d in data if d["Renda"] == "Acima de $35k"]
    for d in data:
        print(d)
    calculate_entropy_of_attr(data, "Historia de Crédito", "Risco")
    calculate_entropy_of_attr(data, "Dívida", "Risco")
    calculate_entropy_of_attr(data, "Garantia", "Risco")


if __name__ == "__main__":
    data = [
        {
            "ID": "E1",
            "Historia de Crédito": "Ruim",
            "Dívida": "Alta",
            "Garantia": "Nenhuma",
            "Renda": "$0 a $15k",
            "Risco": "Alto",
        },
        {
            "ID": "E2",
            "Historia de Crédito": "Desconhecida",
            "Dívida": "Alta",
            "Garantia": "Nenhuma",
            "Renda": "$15 a $35k",
            "Risco": "Alto",
        },
        {
            "ID": "E3",
            "Historia de Crédito": "Desconhecida",
            "Dívida": "Baixa",
            "Garantia": "Nenhuma",
            "Renda": "$15 a $35k",
            "Risco": "Moderado",
        },
        {
            "ID": "E4",
            "Historia de Crédito": "Desconhecida",
            "Dívida": "Baixa",
            "Garantia": "Nenhuma",
            "Renda": "$0 a $15k",
            "Risco": "Alto",
        },
        {
            "ID": "E5",
            "Historia de Crédito": "Desconhecida",
            "Dívida": "Baixa",
            "Garantia": "Nenhuma",
            "Renda": "Acima de $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E6",
            "Historia de Crédito": "Desconhecida",
            "Dívida": "Baixa",
            "Garantia": "Adequada",
            "Renda": "Acima de $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E7",
            "Historia de Crédito": "Ruim",
            "Dívida": "Baixa",
            "Garantia": "Nenhuma",
            "Renda": "$0 a $15k",
            "Risco": "Alto",
        },
        {
            "ID": "E8",
            "Historia de Crédito": "Ruim",
            "Dívida": "Baixa",
            "Garantia": "Adequada",
            "Renda": "Acima de $35k",
            "Risco": "Moderado",
        },
        {
            "ID": "E9",
            "Historia de Crédito": "Boa",
            "Dívida": "Baixa",
            "Garantia": "Nenhuma",
            "Renda": "Acima de $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E10",
            "Historia de Crédito": "Boa",
            "Dívida": "Alta",
            "Garantia": "Adequada",
            "Renda": "Acima de $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E11",
            "Historia de Crédito": "Boa",
            "Dívida": "Alta",
            "Garantia": "Nenhuma",
            "Renda": "$0 a $15k",
            "Risco": "Alto",
        },
        {
            "ID": "E12",
            "Historia de Crédito": "Boa",
            "Dívida": "Alta",
            "Garantia": "Nenhuma",
            "Renda": "$15 a $35k",
            "Risco": "Moderado",
        },
        {
            "ID": "E13",
            "Historia de Crédito": "Boa",
            "Dívida": "Alta",
            "Garantia": "Nenhuma",
            "Renda": "Acima de $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E14",
            "Historia de Crédito": "Ruim",
            "Dívida": "Alta",
            "Garantia": "Nenhuma",
            "Renda": "$15 a $35k",
            "Risco": "Alto",
        },
        {
            "ID": "E15",
            "Historia de Crédito": "Boa",
            "Dívida": "Baixa",
            "Garantia": "Adequada",
            "Renda": "Acima de $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E16",
            "Historia de Crédito": "Desconhecida",
            "Dívida": "Baixa",
            "Garantia": "Adequada",
            "Renda": "$15 a $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E17",
            "Historia de Crédito": "Boa",
            "Dívida": "Alta",
            "Garantia": "Adequada",
            "Renda": "$15 a $35k",
            "Risco": "Baixo",
        },
        {
            "ID": "E18",
            "Historia de Crédito": "Ruim",
            "Dívida": "Baixa",
            "Garantia": "Adequada",
            "Renda": "$15 a $35k",
            "Risco": "Moderado",
        },
        {
            "ID": "E19",
            "Historia de Crédito": "Boa",
            "Dívida": "Alta",
            "Garantia": "Adequada",
            "Renda": "$0 a $15k",
            "Risco": "Moderado",
        },
        {
            "ID": "E20",
            "Historia de Crédito": "Ruim",
            "Dívida": "Alta",
            "Garantia": "Adequada",
            "Renda": "$15 a $35k",
            "Risco": "Moderado",
        },
    ]
    calculate_0a35(data)
