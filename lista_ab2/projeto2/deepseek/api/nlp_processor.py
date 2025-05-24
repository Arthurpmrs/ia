from typing import Dict, List

import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token

# Carrega o modelo de linguagem em português
nlp = spacy.load("pt_core_news_lg")

# Listas de termos relevantes
TECHNOLOGIES = [
    "python",
    "java",
    "javascript",
    "c#",
    "sql",
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "machine learning",
    "ml",
    "ai",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "git",
]

EDUCATION_LEVELS = [
    "phd",
    "doutorado",
    "mestrado",
    "graduação",
    "bacharelado",
    "tecnólogo",
    "técnico",
    "especialização",
    "mba",
]

LANGUAGES = [
    "inglês",
    "english",
    "espanhol",
    "spanish",
    "francês",
    "french",
    "alemão",
    "german",
    "italiano",
    "italian",
    "chinês",
    "chinese",
    "japonês",
    "japanese",
    "russo",
    "russian",
    "árabe",
    "arabic",
]


class CandidateInfoExtractor:
    def __init__(self):
        self.tech_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        self.edu_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        self.lang_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

        # Adiciona padrões aos matchers
        self.tech_matcher.add("TECH", list(nlp.pipe(TECHNOLOGIES)))
        self.edu_matcher.add("EDU", list(nlp.pipe(EDUCATION_LEVELS)))
        self.lang_matcher.add("LANG", list(nlp.pipe(LANGUAGES)))

    def extract_info(self, text: str) -> Dict:
        doc = nlp(text.lower())

        result = {
            "education": "Não informado",
            "experience_years": 0.0,
            "technologies": [],
            "languages": [],
            "behavioral_interview_score": 5.0,
        }

        self._extract_education(doc, result)
        self._extract_experience(doc, result)
        self._extract_technologies(doc, result)
        self._extract_languages(doc, result)
        self._extract_interview_score(doc, result)

        return result

    def _extract_education(self, doc, result):
        matches = self.edu_matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            if "phd" in span.text or "doutorado" in span.text:
                result["education"] = "PhD"
            elif "mestrado" in span.text and result["education"] not in ["PhD"]:
                result["education"] = "Mestrado"
            elif ("graduação" in span.text or "bacharelado" in span.text) and result[
                "education"
            ] not in ["PhD", "Mestrado"]:
                result["education"] = "Bacharelado"

    def _extract_experience(self, doc, result):
        for i, token in enumerate(doc):
            if token.like_num:
                if i < len(doc) - 1 and any(
                    word in doc[i + 1].text for word in ["ano", "anos", "years"]
                ):
                    try:
                        result["experience_years"] = float(token.text)
                    except Exception:
                        pass

        if result["experience_years"] == 0:
            for token in doc:
                if "experiência" in token.text or "experiente" in token.text:
                    result["experience_years"] = 1.0

    def _extract_technologies(self, doc, result):
        matches = self.tech_matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            tech_token = span[-1]
            if not self._is_negated(doc, tech_token):
                tech = tech_token.text.lower()
                if tech not in result["technologies"]:
                    result["technologies"].append(tech)

    def _extract_languages(self, doc, result):
        matches = self.lang_matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            lang_token = span[-1]
            if not self._is_negated(doc, lang_token):
                lang = lang_token.text.lower()
                if lang not in result["languages"]:
                    result["languages"].append(lang)

        # Padroniza os idiomas
        result["languages"] = self._standardize_languages(result["languages"])

    def _extract_interview_score(self, doc, result):
        for i, token in enumerate(doc):
            if token.like_num and i < len(doc) - 1:
                next_token = doc[i + 1]
                if (
                    "/10" in next_token.text
                    or "nota" in token.nbor(-1).text
                    or "score" in token.nbor(-1).text
                ):
                    try:
                        score = float(token.text)
                        result["behavioral_interview_score"] = max(0, min(10, score))
                    except Exception:
                        pass

    def _is_negated(self, doc, token: Token) -> bool:
        """Versão simplificada e mais confiável para detectar negações"""
        negations = {"não", "nao", "nunca", "jamais", "nem"}

        # Verifica os 2 tokens anteriores
        start_idx = max(0, token.i - 3)
        for prev_token in doc[start_idx : token.i]:
            if prev_token.lower_ in negations:
                return True

        # Verifica dependentes diretos de negação
        for child in token.children:
            if child.dep_ == "neg" or child.lower_ in negations:
                return True

        return False

    def _standardize_languages(self, languages: List[str]) -> List[str]:
        """Padroniza os idiomas para formas consistentes"""
        lang_map = {
            "english": "inglês",
            "spanish": "espanhol",
            "french": "francês",
            "german": "alemão",
            "italian": "italiano",
            "chinese": "chinês",
            "japanese": "japonês",
            "russian": "russo",
            "arabic": "árabe",
        }

        standardized = []
        for lang in languages:
            standardized.append(lang_map.get(lang, lang))

        # Remove duplicatas mantendo a ordem
        seen = set()
        return [x for x in standardized if not (x in seen or seen.add(x))]
