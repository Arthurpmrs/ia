def classificar_candidato(candidato: dict, vaga: dict):
    justificativas = []
    pontos = 0
    total = 0

    # 1. Formação
    total += 1
    if vaga["formacao"] == "superior":
        if candidato["formacao"] == "superior":
            pontos += 1
        else:
            justificativas.append("Formação inferior ao exigido.")
    else:
        pontos += 0
       
    # 2. Experiência
    total += 1
    if candidato["experiencia"] >= vaga["experiencia"]:
        pontos += 1
    else:
        justificativas.append(f"Experiência insuficiente: {candidato['experiencia']} ano(s), necessário pelo menos {vaga['experiencia']}.")

    # 3. Tecnologias
    total += 1
    tecnologias_requeridas = set(vaga["tecnologias"])
    tecnologias_candidato = set(candidato["tecnologias"])
    faltando = tecnologias_requeridas - tecnologias_candidato
    if not faltando:
        pontos += 1
    else:
        justificativas.append(f"Faltam tecnologias requeridas: {', '.join(faltando)}.")

    # 4. Idiomas
    total += 1
    idiomas_requeridos = set(vaga["idiomas"])
    idiomas_candidato = set(candidato["idiomas"])
    faltando_idiomas = idiomas_requeridos - idiomas_candidato

    if not faltando_idiomas:
        pontos += 1
    else:
        justificativas.append(f"Idiomas desejados não atendidos: {', '.join(faltando_idiomas)}.")

    # 5. Entrevista
    total += 1
    if candidato["entrevista"] >= vaga["entrevista"]:
        pontos += 1
    else:
        justificativas.append(f"Nota da entrevista abaixo do esperado: {candidato['entrevista']} (mínimo: {vaga['entrevista']}).")

    # Classificação com base em pontuação
    if pontos == total:
        categoria = "Aprovado"
    elif pontos >= total / 2:
        categoria = "Aprovado parcialmente"
    else:
        categoria = "Reprovado"

    if not justificativas:
        justificativas = ["Todos os critérios foram atendidos."]

    return categoria, justificativas
