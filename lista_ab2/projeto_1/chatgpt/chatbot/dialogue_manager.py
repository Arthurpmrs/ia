class DialogueManager:
    def __init__(self):
        self.collected_symptoms = {}
        self.required_symptoms = ["Febre", "Tosse", "DorCorpo", "Fadiga"]

    def process_message(self, message):
        lowered = message.lower()
        updated = False

        if "febre" in lowered:
            self.collected_symptoms["Febre"] = 1
            updated = True
        if "tosse" in lowered:
            self.collected_symptoms["Tosse"] = 1
            updated = True
        if "dores no corpo" in lowered or "dor no corpo" in lowered:
            self.collected_symptoms["DorCorpo"] = 1
            updated = True
        if "fadiga" in lowered or "cansaço" in lowered:
            self.collected_symptoms["Fadiga"] = 1
            updated = True

        missing = [
            s for s in self.required_symptoms if s not in self.collected_symptoms
        ]

        if not missing:
            return (
                "Obrigado, já coletei todas as informações necessárias.",
                self.collected_symptoms,
                True,
            )
        elif updated:
            return (
                f"Entendi. Você poderia me informar se sente: {', '.join(missing)}?",
                self.collected_symptoms,
                False,
            )
        else:
            return (
                "Poderia me dizer se você tem febre, tosse, dores no corpo ou fadiga?",
                self.collected_symptoms,
                False,
            )
