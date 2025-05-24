def get_response(user_message):
    # Simples processamento de linguagem natural (mock)
    structured_data = {}
    if "febre" in user_message.lower():
        structured_data["Febre"] = 1
    if "tosse" in user_message.lower():
        structured_data["Tosse"] = 1
    if "dores no corpo" in user_message.lower():
        structured_data["DorCorpo"] = 1
    if "fadiga" in user_message.lower():
        structured_data["Fadiga"] = 1
    return "Entendi, obrigado pelas informações.", structured_data
