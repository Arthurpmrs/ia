def explain_diagnosis(symptom_data, diagnosis):
    prob_gripe = diagnosis['Gripe'][1]
    explicacao = ["O sistema analisou os seguintes sintomas:"]

    for sintoma, presente in symptom_data.items():
        if presente:
            explicacao.append(f"✔ {sintoma}: presente (contribui positivamente para a hipótese de Gripe)")
        else:
            explicacao.append(f"✘ {sintoma}: ausente (reduz a probabilidade de Gripe)")

    explicacao.append(f"\nProbabilidade final estimada de Gripe: {prob_gripe:.2f}")

    if prob_gripe > 0.7:
        explicacao.append("Conclusão: Alta probabilidade de Gripe com base na combinação dos sintomas presentes.")
    elif prob_gripe > 0.4:
        explicacao.append("Conclusão: Possível Gripe, recomenda-se monitorar os sintomas.")
    else:
        explicacao.append("Conclusão: Baixa probabilidade de Gripe, os sintomas observados não são fortemente indicativos.")

    return "\n".join(explicacao)