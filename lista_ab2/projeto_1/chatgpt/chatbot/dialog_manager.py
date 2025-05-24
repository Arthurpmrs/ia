def get_response(user_message):
    # Simples processamento de linguagem natural (mock)
    structured_data = {}
    if "febre" in user_message.lower():
        structured_data["febre"] = True
    if "tosse" in user_message.lower():
        structured_data["tosse"] = True
    return "Entendi, obrigado pelas informações.", structured_data
