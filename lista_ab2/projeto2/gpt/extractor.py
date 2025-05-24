import re


def extrair_dados(texto):
    texto = texto.lower()
    dados = {
        "formacao": "",
        "experiencia": 0,
        "tecnologias": [],
        "idiomas": [],
        "entrevista": 0,
    }

    # Formação
    if "superior" in texto or "graduação" in texto:
        dados["formacao"] = "superior"

    # Experiência em anos - busca por números próximos da palavra 'ano(s)'
    match = re.search(r"(\d+)\s*ano", texto)
    if match:
        dados["experiencia"] = int(match.group(1))

    # Tecnologias
    tecnologias_possiveis = {
        "python",
        "fastapi",
        "html",
        "css",
        "javascript",
        "react",
        "java",
        "sql",
    }
    for tech in tecnologias_possiveis:
        padrao_negacao = rf"(não|n[ãa]o)\s(conhece|sabe|domina|tem experiência com|tem experiência em)\s{tech}"
        if re.search(padrao_negacao, texto):
            continue
        if tech in texto:
            dados["tecnologias"].append(tech)

    # Idiomas
    idiomas_conhecidos = ["inglês", "espanhol", "francês"]
    for idioma in idiomas_conhecidos:
        padrao_negacao = rf"(não|n[ãa]o)\s(fala|domina|conhece|sabe)\s{idioma}"
        if re.search(padrao_negacao, texto):
            continue
        if idioma in texto:
            dados["idiomas"].append(idioma)

    # Nota da entrevista - busca números entre 0 e 10 próximos de 'nota' ou 'entrevista'
    match_nota = re.search(r"(nota|entrevista)\D*(\d{1,2})", texto)
    if match_nota:
        val = int(match_nota.group(2))
        if 0 <= val <= 10:
            dados["entrevista"] = val

    print(dados)

    return dados
