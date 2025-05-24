import re

class DialogueManager:
    def __init__(self):
        self.collected_symptoms = {}
        self.required_symptoms = ['Febre', 'Tosse', 'DorCorpo', 'Fadiga']

    def process_message(self, message):
        lowered = message.lower()
        updated = False

        def symptom_present(symptom_keywords):
            return any(re.search(rf"\b{kw}\b", lowered) for kw in symptom_keywords)

        def symptom_negative(symptom_keywords):
            return any(re.search(rf"(não|nao).*\b{kw}\b", lowered) or re.search(rf"\b{kw}\b.*(não|nao)", lowered) for kw in symptom_keywords)

        symptoms_map = {
            "Febre": ["febre"],
            "Tosse": ["tosse"],
            "DorCorpo": ["dor no corpo", "dores no corpo"],
            "Fadiga": ["fadiga", "cansaço"]
        }

        for symptom, keywords in symptoms_map.items():
            if symptom in self.collected_symptoms:
                continue
            if symptom_negative(keywords):
                self.collected_symptoms[symptom] = 0
                updated = True
            elif symptom_present(keywords):
                self.collected_symptoms[symptom] = 1
                updated = True

        missing = [s for s in self.required_symptoms if s not in self.collected_symptoms]

        if not missing:
            return ("Obrigado, já coletei todas as informações necessárias.", self.collected_symptoms, True)
        elif updated:
            return (f"Entendi. Você poderia me informar se sente: {', '.join(missing)}?", self.collected_symptoms, False)
        else:
            return ("Poderia me dizer se você tem febre, tosse, dores no corpo ou fadiga?", self.collected_symptoms, False)