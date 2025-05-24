def explain_diagnosis(symptom_data, diagnosis):
    explanation = "O diagnóstico foi influenciado pelos seguintes sintomas:"
    for k in symptom_data:
        explanation += f"\n- {k}"
    return explanation
