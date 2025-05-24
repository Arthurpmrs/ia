import os
from typing import Dict

import joblib
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "candidate_model.pkl"


def train_sample_model():
    # Conjunto de dados ampliado e mais realista
    samples = [
        # Candidatos aprovados (0)
        {
            "education": "PhD",
            "experience_years": 5,
            "technologies": ["Python", "ML", "TensorFlow"],
            "languages": ["English"],
            "behavioral_interview_score": 9,
        },
        {
            "education": "Mestrado",
            "experience_years": 3,
            "technologies": ["Java", "Spring", "SQL"],
            "languages": ["English", "Spanish"],
            "behavioral_interview_score": 8,
        },
        {
            "education": "Bacharelado",
            "experience_years": 4,
            "technologies": ["JavaScript", "React", "Node.js"],
            "languages": ["English"],
            "behavioral_interview_score": 7,
        },
        {
            "education": "PhD",
            "experience_years": 7,
            "technologies": ["Python", "Data Science", "PyTorch"],
            "languages": ["English", "German"],
            "behavioral_interview_score": 9.5,
        },
        # Candidatos aprovados parcialmente (1)
        {
            "education": "Bacharelado",
            "experience_years": 2,
            "technologies": ["Java", "SQL"],
            "languages": [],
            "behavioral_interview_score": 6,
        },
        {
            "education": "Tecnólogo",
            "experience_years": 1.5,
            "technologies": ["HTML", "CSS", "JavaScript"],
            "languages": ["English"],
            "behavioral_interview_score": 5.5,
        },
        {
            "education": "Mestrado",
            "experience_years": 0.5,
            "technologies": ["Python"],
            "languages": ["French"],
            "behavioral_interview_score": 6.5,
        },
        # Candidatos reprovados (2)
        {
            "education": "Bacharelado",
            "experience_years": 0,
            "technologies": [],
            "languages": [],
            "behavioral_interview_score": 4,
        },
        {
            "education": "Técnico",
            "experience_years": 1,
            "technologies": ["Word", "Excel"],
            "languages": [],
            "behavioral_interview_score": 3,
        },
        {
            "education": "Bacharelado",
            "experience_years": 2,
            "technologies": ["Photoshop"],
            "languages": [],
            "behavioral_interview_score": 5,
        },
    ]

    labels = np.array(
        [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
    )  # 0=Aprovado, 1=Parcialmente, 2=Reprovado

    # Pipeline mais sofisticada
    numeric_features = ["experience_years", "behavioral_interview_score"]
    numeric_transformer = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )

    categorical_features = ["education"]
    categorical_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", DictVectorizer(sparse=False)),
        ]
    )

    list_features = ["technologies", "languages"]
    list_transformer = Pipeline([("vectorizer", DictVectorizer(sparse=False))])

    preprocessor = ColumnTransformer(
        [
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
            ("list", list_transformer, list_features),
        ]
    )

    model = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=5,
                    min_samples_split=5,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    # Pré-processamento manual dos dados para o DictVectorizer
    processed_samples = []
    for sample in samples:
        processed = {
            "education": sample["education"],
            "experience_years": sample["experience_years"],
            "behavioral_interview_score": sample["behavioral_interview_score"],
            **{f"tech_{tech}": 1 for tech in sample["technologies"]},
            **{f"lang_{lang}": 1 for lang in sample["languages"]},
        }
        processed_samples.append(processed)

    model.fit(processed_samples, labels)
    joblib.dump(model, MODEL_PATH)

    # Retorna métricas básicas
    train_accuracy = model.score(processed_samples, labels)
    print(f"Model trained with accuracy: {train_accuracy:.2f}")
    return model


if not os.path.exists(MODEL_PATH):
    model = train_sample_model()
else:
    model = joblib.load(MODEL_PATH)


def evaluate_candidate(candidate_data: Dict) -> Dict:
    # Preparar dados para o modelo
    input_data = {
        "education": candidate_data["education"],
        "experience_years": candidate_data["experience_years"],
        "technologies": candidate_data["technologies"],
        "languages": candidate_data["languages"],
        "behavioral_interview_score": candidate_data["behavioral_interview_score"],
    }

    # Fazer previsão
    probas = model.predict_proba([input_data])[0]
    decision = model.predict([input_data])[0]
    confidence = np.max(probas)

    # Mapear decisão numérica para texto
    decisions = {0: "Aprovado", 1: "Aprovado parcialmente", 2: "Reprovado"}

    # Gerar justificativa baseada nos critérios
    justification = generate_justification(decision, candidate_data)

    return {
        "decision": decisions[decision],
        "justification": justification,
        "confidence": float(confidence),
    }


def generate_justification(decision: int, candidate_data: Dict) -> str:
    education = candidate_data["education"]
    exp = candidate_data["experience_years"]
    tech = candidate_data["technologies"]
    langs = candidate_data["languages"]
    score = candidate_data["behavioral_interview_score"]

    if decision == 0:  # Aprovado
        return (
            f"Candidato altamente qualificado com {exp} anos de experiência em {', '.join(tech)}. "
            f"Formação em {education} e domínio de {len(langs)} idiomas. "
            f"Excelente desempenho na entrevista comportamental (nota {score}/10)."
        )

    elif decision == 1:  # Aprovado parcialmente
        return (
            f"Candidato com qualificações medianas. {exp} anos de experiência em {', '.join(tech)}. "
            f"Formação em {education} mas poderia melhorar em idiomas ({len(langs)} conhecidos). "
            f"Desempenho razoável na entrevista (nota {score}/10). Recomendável para posições júnior."
        )

    else:  # Reprovado
        return (
            f"Candidato não atende aos requisitos mínimos. Experiência insuficiente ({exp} anos). "
            f"Tecnologias conhecidas: {', '.join(tech) if tech else 'nenhuma'}. "
            f"Desempenho abaixo do esperado na entrevista (nota {score}/10)."
        )
