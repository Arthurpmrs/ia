def explain_diagnosis(symptom_data, diagnosis):
    explanation = "O diagnóstico foi influenciado pelos seguintes sintomas:"
    for k in symptom_data:
        explanation += f"\n- {k}"
    explanation += f"\nProbabilidade de Gripe: {diagnosis['Gripe'][1]:.2f}"
    return explanation
