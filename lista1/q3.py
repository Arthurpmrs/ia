from collections import deque


def check_condition_true(condition, facts):
    # Vamos considerar que condições podem ser apenas do tipo
    # A1 ^ A2 ^ ... ^ An -> X
    # A1 v A2 v ... v An -> X
    if len(condition) == 1:
        return True
    if " ^ " in condition:
        literals = condition.split(" ^ ")
        return all(fact in facts for fact in literals)
    if " v " in condition:
        literals = condition.split(" v ")
        return any(fact in facts for fact in literals)


def modus_ponens(rule, facts):
    if "→" not in rule:
        return None

    condition, result = rule.split(" → ")
    if check_condition_true(condition, facts):
        return result
    return None


def search(base):
    facts = {fact for fact in knowledge_base if len(fact) == 1}
    queue = deque(facts)
    inferred_facts = set(facts)

    while queue:
        _ = queue.popleft()

        for rule in base:
            result = modus_ponens(rule, inferred_facts)
            if result and result not in inferred_facts:
                inferred_facts.add(result)
                queue.append(result)
                continue
    return inferred_facts


def controller(base, goal):
    if goal in search(base):
        print(f"Provamos {goal}!")
    else:
        print(f"Não pudemos provar {goal}.")


if __name__ == "__main__":
    knowledge_base = [
        "A",
        "B",
        "F",
        "A ^ B → C",
        "A → D",
        "C ^ D → E",
        "B ^ E ^ F → G",
        "A ^ E → H",
        "D ^ E ^ H → I",
    ]

    controller(knowledge_base, "H")
