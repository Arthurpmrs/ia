# backend.py - FastAPI Backend
import json
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


# Importar as classes do sistema original
class BayesianNetwork:
    """
    Implementação de uma Rede Bayesiana para diagnóstico médico
    """

    def __init__(self):
        # Estrutura da rede: doenças -> sintomas
        self.diseases = [
            "gripe",
            "covid19",
            "pneumonia",
            "alergia",
            "enxaqueca",
            "gastrite",
            "ansiedade",
            "hipertensao",
        ]

        self.symptoms = [
            "febre",
            "tosse",
            "dor_cabeca",
            "cansaco",
            "dor_garganta",
            "falta_ar",
            "dor_peito",
            "nausea",
            "vomito",
            "dor_estomago",
            "tontura",
            "palpitacao",
            "irritabilidade",
            "coriza",
            "espirros",
        ]

        # Probabilidades a priori das doenças (prevalência)
        self.disease_priors = {
            "gripe": 0.15,
            "covid19": 0.08,
            "pneumonia": 0.03,
            "alergia": 0.20,
            "enxaqueca": 0.12,
            "gastrite": 0.10,
            "ansiedade": 0.18,
            "hipertensao": 0.14,
        }

        # Probabilidades condicionais P(sintoma|doença)
        self.conditional_probs = {
            "gripe": {
                "febre": 0.85,
                "tosse": 0.70,
                "dor_cabeca": 0.65,
                "cansaco": 0.80,
                "dor_garganta": 0.75,
                "falta_ar": 0.20,
                "dor_peito": 0.15,
                "nausea": 0.25,
                "vomito": 0.15,
                "dor_estomago": 0.10,
                "tontura": 0.30,
                "palpitacao": 0.10,
                "irritabilidade": 0.25,
                "coriza": 0.60,
                "espirros": 0.55,
            },
            "covid19": {
                "febre": 0.80,
                "tosse": 0.75,
                "dor_cabeca": 0.60,
                "cansaco": 0.85,
                "dor_garganta": 0.40,
                "falta_ar": 0.65,
                "dor_peito": 0.35,
                "nausea": 0.30,
                "vomito": 0.20,
                "dor_estomago": 0.25,
                "tontura": 0.35,
                "palpitacao": 0.25,
                "irritabilidade": 0.40,
                "coriza": 0.30,
                "espirros": 0.25,
            },
            "pneumonia": {
                "febre": 0.90,
                "tosse": 0.85,
                "dor_cabeca": 0.45,
                "cansaco": 0.80,
                "dor_garganta": 0.25,
                "falta_ar": 0.80,
                "dor_peito": 0.70,
                "nausea": 0.35,
                "vomito": 0.25,
                "dor_estomago": 0.20,
                "tontura": 0.40,
                "palpitacao": 0.30,
                "irritabilidade": 0.30,
                "coriza": 0.15,
                "espirros": 0.10,
            },
            "alergia": {
                "febre": 0.10,
                "tosse": 0.45,
                "dor_cabeca": 0.30,
                "cansaco": 0.40,
                "dor_garganta": 0.35,
                "falta_ar": 0.40,
                "dor_peito": 0.20,
                "nausea": 0.15,
                "vomito": 0.10,
                "dor_estomago": 0.15,
                "tontura": 0.20,
                "palpitacao": 0.15,
                "irritabilidade": 0.35,
                "coriza": 0.85,
                "espirros": 0.90,
            },
            "enxaqueca": {
                "febre": 0.15,
                "tosse": 0.10,
                "dor_cabeca": 0.95,
                "cansaco": 0.70,
                "dor_garganta": 0.10,
                "falta_ar": 0.20,
                "dor_peito": 0.15,
                "nausea": 0.75,
                "vomito": 0.50,
                "dor_estomago": 0.30,
                "tontura": 0.60,
                "palpitacao": 0.25,
                "irritabilidade": 0.65,
                "coriza": 0.10,
                "espirros": 0.05,
            },
            "gastrite": {
                "febre": 0.20,
                "tosse": 0.10,
                "dor_cabeca": 0.35,
                "cansaco": 0.50,
                "dor_garganta": 0.15,
                "falta_ar": 0.15,
                "dor_peito": 0.25,
                "nausea": 0.80,
                "vomito": 0.60,
                "dor_estomago": 0.90,
                "tontura": 0.30,
                "palpitacao": 0.20,
                "irritabilidade": 0.55,
                "coriza": 0.05,
                "espirros": 0.05,
            },
            "ansiedade": {
                "febre": 0.10,
                "tosse": 0.15,
                "dor_cabeca": 0.55,
                "cansaco": 0.70,
                "dor_garganta": 0.20,
                "falta_ar": 0.60,
                "dor_peito": 0.45,
                "nausea": 0.50,
                "vomito": 0.25,
                "dor_estomago": 0.45,
                "tontura": 0.55,
                "palpitacao": 0.75,
                "irritabilidade": 0.85,
                "coriza": 0.10,
                "espirros": 0.10,
            },
            "hipertensao": {
                "febre": 0.15,
                "tosse": 0.20,
                "dor_cabeca": 0.70,
                "cansaco": 0.60,
                "dor_garganta": 0.15,
                "falta_ar": 0.45,
                "dor_peito": 0.40,
                "nausea": 0.35,
                "vomito": 0.20,
                "dor_estomago": 0.25,
                "tontura": 0.65,
                "palpitacao": 0.60,
                "irritabilidade": 0.55,
                "coriza": 0.10,
                "espirros": 0.10,
            },
        }

    def calculate_posterior(self, observed_symptoms: List[str]) -> Dict[str, float]:
        """
        Calcula probabilidades posteriores usando Teorema de Bayes
        """
        posteriors = {}

        for disease in self.diseases:
            prior = self.disease_priors[disease]
            likelihood = 1.0

            for symptom in self.symptoms:
                if symptom in observed_symptoms:
                    likelihood *= self.conditional_probs[disease][symptom]
                else:
                    likelihood *= 1 - self.conditional_probs[disease][symptom]

            posteriors[disease] = prior * likelihood

        # Normalização
        total = sum(posteriors.values())
        if total > 0:
            posteriors = {k: v / total for k, v in posteriors.items()}

        return posteriors


class MedicalChatbot:
    """
    Chatbot adaptado para interface web
    """

    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.bayesian_net = BayesianNetwork()
        self.user_symptoms = []
        self.conversation_state = "greeting"

        # Mapeamento de sintomas em linguagem natural
        self.symptom_mapping = {
            "febre": ["febre", "temperatura alta", "calor", "quentura"],
            "tosse": ["tosse", "tossir", "pigarro"],
            "dor_cabeca": ["dor de cabeça", "cefaleia", "enxaqueca", "dor na cabeça"],
            "cansaco": ["cansaço", "fadiga", "fraqueza", "indisposição", "sonolência"],
            "dor_garganta": [
                "dor de garganta",
                "garganta inflamada",
                "garganta dolorida",
            ],
            "falta_ar": ["falta de ar", "dispneia", "dificuldade respirar", "sem ar"],
            "dor_peito": ["dor no peito", "dor torácica", "aperto no peito"],
            "nausea": ["náusea", "enjoo", "mal estar"],
            "vomito": ["vômito", "vomitar", "regurgitar"],
            "dor_estomago": ["dor de estômago", "dor abdominal", "dor na barriga"],
            "tontura": ["tontura", "vertigem", "desequilíbrio"],
            "palpitacao": ["palpitação", "coração acelerado", "taquicardia"],
            "irritabilidade": ["irritabilidade", "irritação", "nervosismo", "ansioso"],
            "coriza": ["coriza", "nariz escorrendo", "secreção nasal"],
            "espirros": ["espirros", "espirrar"],
        }

    def extract_symptoms(self, user_input: str) -> List[str]:
        """
        Extrai sintomas do texto do usuário
        """
        user_input = user_input.lower()
        found_symptoms = []

        for symptom_key, variations in self.symptom_mapping.items():
            for variation in variations:
                if variation in user_input:
                    if symptom_key not in found_symptoms:
                        found_symptoms.append(symptom_key)
                    break

        return found_symptoms

    def generate_response(self, user_input: str) -> dict:
        """
        Gera resposta estruturada para a interface web
        """
        if self.conversation_state == "greeting":
            self.conversation_state = "collecting_symptoms"
            return {
                "message": """Olá! Sou um assistente de diagnóstico médico. 

⚠️  IMPORTANTE: Este sistema é apenas uma ferramenta de apoio e NÃO substitui a consulta médica profissional.

Para começar, me conte quais sintomas você está sentindo. Pode descrever livremente, por exemplo:
- "Estou com febre e dor de cabeça"
- "Sinto cansaço e falta de ar"
- "Tenho dor de estômago e náusea"

Quais são seus sintomas?""",
                "state": "collecting_symptoms",
                "symptoms": [],
                "show_diagnosis_button": False,
            }

        elif self.conversation_state == "collecting_symptoms":
            new_symptoms = self.extract_symptoms(user_input)

            if new_symptoms:
                for symptom in new_symptoms:
                    if symptom not in self.user_symptoms:
                        self.user_symptoms.append(symptom)

                message = f"Entendi. Identifiquei os seguintes sintomas: {', '.join([self.translate_symptom(s) for s in new_symptoms])}\n\n"
                message += f"Sintomas registrados até agora: {', '.join([self.translate_symptom(s) for s in self.user_symptoms])}\n\n"
                message += "Há mais algum sintoma que você gostaria de relatar? Ou podemos prosseguir com o diagnóstico?"

                return {
                    "message": message,
                    "state": "collecting_symptoms",
                    "symptoms": [self.translate_symptom(s) for s in self.user_symptoms],
                    "show_diagnosis_button": True,
                }
            else:
                if (
                    "diagnóstico" in user_input.lower()
                    or "diagnostico" in user_input.lower()
                ):
                    return self.generate_diagnosis()
                else:
                    return {
                        "message": "Não consegui identificar sintomas específicos no que você disse. Pode tentar descrever de outra forma?",
                        "state": "collecting_symptoms",
                        "symptoms": [
                            self.translate_symptom(s) for s in self.user_symptoms
                        ],
                        "show_diagnosis_button": len(self.user_symptoms) > 0,
                    }

        elif self.conversation_state == "diagnosis_complete":
            if "novo" in user_input.lower() or "reiniciar" in user_input.lower():
                self.reset_conversation()
                return {
                    "message": "Vamos começar uma nova consulta. Quais sintomas você está sentindo?",
                    "state": "collecting_symptoms",
                    "symptoms": [],
                    "show_diagnosis_button": False,
                }
            else:
                return {
                    "message": "Consulta finalizada. Clique em 'Nova Consulta' se quiser fazer uma nova avaliação.",
                    "state": "diagnosis_complete",
                    "symptoms": [self.translate_symptom(s) for s in self.user_symptoms],
                    "show_diagnosis_button": False,
                }

        return {
            "message": "Desculpe, não entendi. Pode reformular sua pergunta?",
            "state": self.conversation_state,
            "symptoms": [self.translate_symptom(s) for s in self.user_symptoms],
            "show_diagnosis_button": False,
        }

    def translate_symptom(self, symptom_key: str) -> str:
        """Traduz chave do sintoma para descrição legível"""
        translations = {
            "febre": "febre",
            "tosse": "tosse",
            "dor_cabeca": "dor de cabeça",
            "cansaco": "cansaço",
            "dor_garganta": "dor de garganta",
            "falta_ar": "falta de ar",
            "dor_peito": "dor no peito",
            "nausea": "náusea",
            "vomito": "vômito",
            "dor_estomago": "dor de estômago",
            "tontura": "tontura",
            "palpitacao": "palpitação",
            "irritabilidade": "irritabilidade",
            "coriza": "coriza",
            "espirros": "espirros",
        }
        return translations.get(symptom_key, symptom_key)

    def translate_disease(self, disease_key: str) -> str:
        """Traduz chave da doença para nome legível"""
        translations = {
            "gripe": "Gripe",
            "covid19": "COVID-19",
            "pneumonia": "Pneumonia",
            "alergia": "Alergia Respiratória",
            "enxaqueca": "Enxaqueca",
            "gastrite": "Gastrite",
            "ansiedade": "Transtorno de Ansiedade",
            "hipertensao": "Hipertensão",
        }
        return translations.get(disease_key, disease_key)

    def generate_diagnosis(self) -> dict:
        """Gera diagnóstico estruturado para a interface web"""
        if not self.user_symptoms:
            return {
                "message": "Não foram identificados sintomas suficientes para realizar um diagnóstico.",
                "state": "collecting_symptoms",
                "symptoms": [],
                "show_diagnosis_button": False,
            }

        posteriors = self.bayesian_net.calculate_posterior(self.user_symptoms)
        sorted_diseases = sorted(posteriors.items(), key=lambda x: x[1], reverse=True)

        # Preparar dados estruturados para o frontend
        diagnosis_data = {
            "symptoms_analyzed": [
                self.translate_symptom(s) for s in self.user_symptoms
            ],
            "probabilities": [
                {
                    "disease": self.translate_disease(disease),
                    "probability": prob * 100,
                    "rank": i + 1,
                }
                for i, (disease, prob) in enumerate(sorted_diseases[:5])
            ],
            "most_likely": {
                "disease": self.translate_disease(sorted_diseases[0][0]),
                "probability": sorted_diseases[0][1] * 100,
                "explanation": self.generate_explanation(sorted_diseases[0][0]),
                "recommendations": self.generate_recommendations(sorted_diseases[0][0]),
            },
        }

        self.conversation_state = "diagnosis_complete"

        return {
            "message": "Diagnóstico concluído com sucesso!",
            "state": "diagnosis_complete",
            "symptoms": [self.translate_symptom(s) for s in self.user_symptoms],
            "show_diagnosis_button": False,
            "diagnosis": diagnosis_data,
        }

    def generate_explanation(self, most_likely_disease: str) -> dict:
        """Gera explicação estruturada da decisão diagnóstica"""
        disease_name = self.translate_disease(most_likely_disease)

        relevant_symptoms = []
        for symptom in self.user_symptoms:
            prob = self.bayesian_net.conditional_probs[most_likely_disease][symptom]
            if prob > 0.5:
                relevant_symptoms.append(
                    {
                        "symptom": self.translate_symptom(symptom),
                        "probability": prob * 100,
                    }
                )

        relevant_symptoms.sort(key=lambda x: x["probability"], reverse=True)

        return {
            "text": f"O diagnóstico mais provável é {disease_name} baseado na análise Bayesiana dos sintomas reportados.",
            "relevant_symptoms": relevant_symptoms,
        }

    def generate_recommendations(self, disease: str) -> List[str]:
        """Gera recomendações estruturadas baseadas no diagnóstico"""
        recommendations_map = {
            "gripe": [
                "Repouso e hidratação adequada",
                "Medicamentos sintomáticos (analgésicos, antitérmicos)",
                "Consulte médico se sintomas persistirem por mais de 7 dias",
                "Isolamento para evitar contágio",
            ],
            "covid19": [
                "Isolamento imediato por pelo menos 7 dias",
                "Monitoramento da saturação de oxigênio",
                "Procure atendimento médico urgente se houver dificuldade respiratória",
                "Hidratação e repouso",
                "Notifique contatos próximos",
            ],
            "pneumonia": [
                "⚠️ PROCURE ATENDIMENTO MÉDICO IMEDIATAMENTE",
                "Pneumonia requer tratamento profissional urgente",
                "Possível necessidade de antibióticos ou hospitalização",
                "Não tente auto-medicação",
            ],
            "alergia": [
                "Identifique e evite possíveis alérgenos",
                "Anti-histamínicos podem ajudar com sintomas",
                "Mantenha ambientes limpos e arejados",
                "Consulte alergista para testes específicos",
            ],
            "enxaqueca": [
                "Repouso em ambiente escuro e silencioso",
                "Compressas frias na testa",
                "Evite gatilhos conhecidos (stress, alguns alimentos)",
                "Consulte neurologista para tratamento preventivo",
            ],
            "gastrite": [
                "Dieta leve e fraccionada",
                "Evite alimentos irritantes (picantes, ácidos, café)",
                "Consulte gastroenterologista",
                "Possível necessidade de medicamentos para reduzir acidez",
            ],
            "ansiedade": [
                "Técnicas de respiração e relaxamento",
                "Atividade física regular",
                "Consulte psicólogo ou psiquiatra",
                "Evite cafeína e álcool",
                "Procure ajuda profissional especializada",
            ],
            "hipertensao": [
                "⚠️ Monitore regularmente a pressão arterial",
                "Consulte cardiologista urgentemente",
                "Dieta com baixo teor de sódio",
                "Atividade física moderada (com acompanhamento médico)",
                "Possível necessidade de medicação anti-hipertensiva",
            ],
        }

        return recommendations_map.get(
            disease,
            ["Consulte um médico para orientações específicas sobre tratamento."],
        )

    def reset_conversation(self):
        """Reinicia a conversa para novo diagnóstico"""
        self.user_symptoms = []
        self.conversation_state = "collecting_symptoms"


# Modelos Pydantic para API
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: dict
    session_id: str


class DiagnosisRequest(BaseModel):
    session_id: str


# FastAPI App
app = FastAPI(title="Sistema de Diagnóstico Médico", version="1.0.0")

# Armazenamento de sessões em memória
sessions: Dict[str, MedicalChatbot] = {}


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve a página principal"""
    return FileResponse("static/index.html")


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Endpoint principal para conversa com o chatbot"""
    try:
        session_id = chat_message.session_id

        # Criar nova sessão se não existir
        if not session_id or session_id not in sessions:
            session_id = str(uuid.uuid4())
            sessions[session_id] = MedicalChatbot(session_id)

        chatbot = sessions[session_id]
        response = chatbot.generate_response(chat_message.message)

        return ChatResponse(response=response, session_id=session_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.post("/api/diagnosis")
async def get_diagnosis(request: DiagnosisRequest):
    """Endpoint para gerar diagnóstico"""
    try:
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")

        chatbot = sessions[request.session_id]
        diagnosis = chatbot.generate_diagnosis()

        return {"diagnosis": diagnosis}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.post("/api/reset")
async def reset_session(request: DiagnosisRequest):
    """Endpoint para reiniciar sessão"""
    try:
        if request.session_id in sessions:
            sessions[request.session_id].reset_conversation()
            return {"message": "Sessão reiniciada com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {"status": "ok", "sessions_active": len(sessions)}


# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    print("🏥 Iniciando Sistema de Diagnóstico Médico Web")
    print("📱 Acesse: http://localhost:8000")
    print("🔗 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
