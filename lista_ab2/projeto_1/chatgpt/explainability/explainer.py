def explain_diagnosis(symptom_data, diagnosis):
    explanation = "O diagnóstico foi influenciado pelos seguintes sintomas:"
    for k, v in symptom_data.items():
        estado = "Presente" if v == 1 else "Ausente"
        explanation += f"\n- {k}: {estado}"
    explanation += f"\nProbabilidade de Gripe: {diagnosis['Gripe'][1]:.2f}"
    return explanation