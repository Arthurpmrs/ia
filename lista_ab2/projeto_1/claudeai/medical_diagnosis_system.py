import json
import re
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import numpy as np


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
        P(doença|sintomas) ∝ P(sintomas|doença) * P(doença)
        """
        posteriors = {}

        for disease in self.diseases:
            # Probabilidade a priori
            prior = self.disease_priors[disease]

            # Likelihood: P(sintomas|doença)
            likelihood = 1.0
            for symptom in self.symptoms:
                if symptom in observed_symptoms:
                    # Sintoma presente
                    likelihood *= self.conditional_probs[disease][symptom]
                else:
                    # Sintoma ausente
                    likelihood *= 1 - self.conditional_probs[disease][symptom]

            posteriors[disease] = prior * likelihood

        # Normalização
        total = sum(posteriors.values())
        if total > 0:
            posteriors = {k: v / total for k, v in posteriors.items()}

        return posteriors


class MedicalChatbot:
    """
    Chatbot para interação com o usuário e coleta de sintomas
    """

    def __init__(self):
        self.bayesian_net = BayesianNetwork()
        self.user_symptoms = []
        self.conversation_state = "greeting"

        # Mapeamento de sintomas em linguagem natural
        self.symptom_mapping = {
            # Febre
            "febre": ["febre", "temperatura alta", "calor", "quentura"],
            # Tosse
            "tosse": ["tosse", "tossir", "pigarro"],
            # Dor de cabeça
            "dor_cabeca": ["dor de cabeça", "cefaleia", "enxaqueca", "dor na cabeça"],
            # Cansaço
            "cansaco": ["cansaço", "fadiga", "fraqueza", "indisposição", "sonolência"],
            # Dor de garganta
            "dor_garganta": [
                "dor de garganta",
                "garganta inflamada",
                "garganta dolorida",
            ],
            # Falta de ar
            "falta_ar": ["falta de ar", "dispneia", "dificuldade respirar", "sem ar"],
            # Dor no peito
            "dor_peito": ["dor no peito", "dor torácica", "aperto no peito"],
            # Náusea
            "nausea": ["náusea", "enjoo", "mal estar"],
            # Vômito
            "vomito": ["vômito", "vomitar", "regurgitar"],
            # Dor de estômago
            "dor_estomago": ["dor de estômago", "dor abdominal", "dor na barriga"],
            # Tontura
            "tontura": ["tontura", "vertigem", "desequilíbrio"],
            # Palpitação
            "palpitacao": ["palpitação", "coração acelerado", "taquicardia"],
            # Irritabilidade
            "irritabilidade": ["irritabilidade", "irritação", "nervosismo", "ansioso"],
            # Coriza
            "coriza": ["coriza", "nariz escorrendo", "secreção nasal"],
            # Espirros
            "espirros": ["espirros", "espirrar"],
        }

    def extract_symptoms(self, user_input: str) -> List[str]:
        """
        Extrai sintomas do texto do usuário usando processamento de linguagem natural básico
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

    def generate_response(self, user_input: str) -> str:
        """
        Gera resposta baseada no estado da conversa e entrada do usuário
        """
        if self.conversation_state == "greeting":
            self.conversation_state = "collecting_symptoms"
            return """Olá! Sou um assistente de diagnóstico médico. 

⚠️  IMPORTANTE: Este sistema é apenas uma ferramenta de apoio e NÃO substitui a consulta médica profissional.

Para começar, me conte quais sintomas você está sentindo. Pode descrever livremente, por exemplo:
- "Estou com febre e dor de cabeça"
- "Sinto cansaço e falta de ar"
- "Tenho dor de estômago e náusea"

Quais são seus sintomas?"""

        elif self.conversation_state == "collecting_symptoms":
            # Extrair novos sintomas
            new_symptoms = self.extract_symptoms(user_input)

            if new_symptoms:
                for symptom in new_symptoms:
                    if symptom not in self.user_symptoms:
                        self.user_symptoms.append(symptom)

                response = f"Entendi. Identifiquei os seguintes sintomas: {', '.join([self.translate_symptom(s) for s in new_symptoms])}\n\n"
                response += f"Sintomas registrados até agora: {', '.join([self.translate_symptom(s) for s in self.user_symptoms])}\n\n"
                response += "Há mais algum sintoma que você gostaria de relatar? Ou podemos prosseguir com o diagnóstico? (digite 'diagnóstico' para continuar)"

                return response
            else:
                if (
                    "diagnóstico" in user_input.lower()
                    or "diagnostico" in user_input.lower()
                ):
                    return self.generate_diagnosis()
                else:
                    return "Não consegui identificar sintomas específicos no que você disse. Pode tentar descrever de outra forma? Ou digite 'diagnóstico' se quiser prosseguir com os sintomas já informados."

        elif self.conversation_state == "diagnosis_complete":
            if "novo" in user_input.lower() or "reiniciar" in user_input.lower():
                self.reset_conversation()
                return "Vamos começar uma nova consulta. Quais sintomas você está sentindo?"
            else:
                return "Consulta finalizada. Digite 'novo diagnóstico' se quiser fazer uma nova avaliação."

        return "Desculpe, não entendi. Pode reformular sua pergunta?"

    def translate_symptom(self, symptom_key: str) -> str:
        """
        Traduz chave do sintoma para descrição legível
        """
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

    def generate_diagnosis(self) -> str:
        """
        Gera diagnóstico baseado nos sintomas coletados
        """
        if not self.user_symptoms:
            return "Não foram identificados sintomas suficientes para realizar um diagnóstico. Por favor, descreva seus sintomas."

        # Calcular probabilidades
        posteriors = self.bayesian_net.calculate_posterior(self.user_symptoms)

        # Ordenar por probabilidade
        sorted_diseases = sorted(posteriors.items(), key=lambda x: x[1], reverse=True)

        # Gerar resposta
        response = "📊 DIAGNÓSTICO PROBABILÍSTICO\n"
        response += "=" * 50 + "\n\n"

        response += f"Sintomas analisados: {', '.join([self.translate_symptom(s) for s in self.user_symptoms])}\n\n"

        response += "🎯 PROBABILIDADES DE DIAGNÓSTICO:\n\n"

        for i, (disease, prob) in enumerate(sorted_diseases[:5]):
            percentage = prob * 100
            disease_name = self.translate_disease(disease)

            if i == 0:
                response += f"1º. {disease_name}: {percentage:.1f}% ⭐\n"
            else:
                response += f"{i + 1}º. {disease_name}: {percentage:.1f}%\n"

        # Explicação da decisão
        response += "\n" + "=" * 50 + "\n"
        response += "💡 EXPLICAÇÃO DO DIAGNÓSTICO:\n\n"
        response += self.generate_explanation(sorted_diseases[0][0])

        # Recomendações
        response += "\n" + "=" * 50 + "\n"
        response += "🏥 RECOMENDAÇÕES:\n\n"
        response += self.generate_recommendations(sorted_diseases[0][0])

        response += "\n⚠️  IMPORTANTE: Este diagnóstico é probabilístico e serve apenas como orientação. Sempre consulte um médico para avaliação profissional adequada."

        self.conversation_state = "diagnosis_complete"
        return response

    def translate_disease(self, disease_key: str) -> str:
        """
        Traduz chave da doença para nome legível
        """
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

    def generate_explanation(self, most_likely_disease: str) -> str:
        """
        Gera explicação detalhada da decisão diagnóstica
        """
        disease_name = self.translate_disease(most_likely_disease)

        explanation = f"O diagnóstico mais provável é {disease_name} baseado na análise Bayesiana dos sintomas reportados.\n\n"

        explanation += "🔍 ANÁLISE DOS SINTOMAS:\n"

        relevant_symptoms = []
        for symptom in self.user_symptoms:
            prob = self.bayesian_net.conditional_probs[most_likely_disease][symptom]
            if prob > 0.5:
                relevant_symptoms.append((symptom, prob))

        relevant_symptoms.sort(key=lambda x: x[1], reverse=True)

        for symptom, prob in relevant_symptoms:
            symptom_name = self.translate_symptom(symptom)
            explanation += f"• {symptom_name}: {prob * 100:.0f}% de probabilidade em casos de {disease_name}\n"

        return explanation

    def generate_recommendations(self, disease: str) -> str:
        """
        Gera recomendações baseadas no diagnóstico mais provável
        """
        recommendations = {
            "gripe": """• Repouso e hidratação adequada
• Medicamentos sintomáticos (analgésicos, antitérmicos)
• Consulte médico se sintomas persistirem por mais de 7 dias
• Isolamento para evitar contágio""",
            "covid19": """• Isolamento imediato por pelo menos 7 dias
• Monitoramento da saturação de oxigênio
• Procure atendimento médico urgente se houver dificuldade respiratória
• Hidratação e repouso
• Notifique contatos próximos""",
            "pneumonia": """• ⚠️ PROCURE ATENDIMENTO MÉDICO IMEDIATAMENTE
• Pneumonia requer tratamento profissional urgente
• Possível necessidade de antibióticos ou hospitalização
• Não tente auto-medicação""",
            "alergia": """• Identifique e evite possíveis alérgenos
• Anti-histamínicos podem ajudar com sintomas
• Mantenha ambientes limpos e arejados
• Consulte alergista para testes específicos""",
            "enxaqueca": """• Repouso em ambiente escuro e silencioso
• Compressas frias na testa
• Evite gatilhos conhecidos (stress, alguns alimentos)
• Consulte neurologista para tratamento preventivo""",
            "gastrite": """• Dieta leve e fraccionada
• Evite alimentos irritantes (picantes, ácidos, café)
• Consulte gastroenterologista
• Possível necessidade de medicamentos para reduzir acidez""",
            "ansiedade": """• Técnicas de respiração e relaxamento
• Atividade física regular
• Consulte psicólogo ou psiquiatra
• Evite cafeína e álcool
• Procure ajuda profissional especializada""",
            "hipertensao": """• ⚠️ Monitore regularmente a pressão arterial
• Consulte cardiologista urgentemente
• Dieta com baixo teor de sódio
• Atividade física moderada (com acompanhamento médico)
• Possível necessidade de medicação anti-hipertensiva""",
        }

        return recommendations.get(
            disease, "Consulte um médico para orientações específicas sobre tratamento."
        )

    def reset_conversation(self):
        """
        Reinicia a conversa para novo diagnóstico
        """
        self.user_symptoms = []
        self.conversation_state = "collecting_symptoms"


class MedicalDiagnosisSystem:
    """
    Sistema principal que integra todos os componentes
    """

    def __init__(self):
        self.chatbot = MedicalChatbot()
        print("Sistema de Diagnóstico Médico Inteligente")
        print("=" * 50)
        print("⚠️  AVISO: Este sistema é apenas educacional/demonstrativo")
        print("   Sempre procure um médico para diagnóstico real!")
        print("=" * 50)

    def run(self):
        """
        Loop principal do sistema
        """
        print(self.chatbot.generate_response(""))  # Mensagem de boas-vindas

        while True:
            try:
                user_input = input("\n👤 Você: ").strip()

                if user_input.lower() in ["sair", "quit", "exit"]:
                    print("\n🏥 Obrigado por usar o sistema. Cuide-se bem!")
                    break

                if not user_input:
                    continue

                response = self.chatbot.generate_response(user_input)
                print(f"\n🤖 Assistente: {response}")

            except KeyboardInterrupt:
                print("\n\n🏥 Sistema encerrado. Cuide-se bem!")
                break
            except Exception as e:
                print(f"\n❌ Erro no sistema: {e}")
                print("Tente novamente ou digite 'sair' para encerrar.")


# Demonstração de uso do sistema
def demonstrate_system():
    """
    Função para demonstrar o funcionamento do sistema
    """
    print("=" * 60)
    print("DEMONSTRAÇÃO DO SISTEMA DE DIAGNÓSTICO MÉDICO")
    print("=" * 60)

    # Criar instância do sistema
    chatbot = MedicalChatbot()

    # Simular conversa
    test_cases = [
        "Estou com febre alta e muita tosse",
        "Também sinto falta de ar e cansaço extremo",
        "diagnóstico",
    ]

    print(chatbot.generate_response(""))  # Boas-vindas

    for user_input in test_cases:
        print(f"\n👤 Usuário: {user_input}")
        response = chatbot.generate_response(user_input)
        print(f"\n🤖 Sistema: {response}")
        print("\n" + "-" * 60)


if __name__ == "__main__":
    # Demonstração
    demonstrate_system()

    print("\n" + "=" * 60)
    print("INICIANDO SISTEMA INTERATIVO")
    print("=" * 60)

    # Sistema interativo
    system = MedicalDiagnosisSystem()
    system.run()
