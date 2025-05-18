from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionProcessOrder(Action):
    def name(self) -> Text:
        return "action_process_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        clothes_type = tracker.get_slot("clothes_type")
        clothes_details = ""
        print("aaaaaaaaaaaaaaaaaaaaaa", clothes_type)

        if clothes_type == "calça":
            pants_size = tracker.get_slot("pants_size")
            pants_fit = tracker.get_slot("pants_fit")
            clothes_details = f"Calça tamanho {pants_size}, {pants_fit}"
        elif clothes_type == "camisa":
            shirt_size = tracker.get_slot("shirt_size")
            collar_type = tracker.get_slot("collar_type")
            clothes_details = f"Camisa tamanho {shirt_size}, {collar_type}"
        else:
            clothes_details = "item não especificado corretamente"

        # Envie a mensagem de confirmação com os detalhes
        dispatcher.utter_message(
            template="utter_confirm_order", clothes_details=clothes_details
        )

        # Reset all slots after processing the order
        return [AllSlotsReset()]


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Tell the user we didn't understand and ask for clarification
        dispatcher.utter_message(template="utter_fallback")

        clothes_type = tracker.get_slot("clothes_type")
        print("aaaaaaaaaaaaaaaaaaaaaa", clothes_type)
        if not clothes_type:
            dispatcher.utter_message(template="utter_ask_clothes_type")
        elif clothes_type == "calça":
            pants_size = tracker.get_slot("pants_size")
            if not pants_size:
                dispatcher.utter_message(template="utter_ask_pants_size")
            else:
                dispatcher.utter_message(template="utter_ask_pants_fit")
        elif clothes_type == "camisa":
            shirt_size = tracker.get_slot("shirt_size")
            if not shirt_size:
                dispatcher.utter_message(template="utter_ask_shirt_size")
            else:
                dispatcher.utter_message(template="utter_ask_collar_type")

        return []


print("INIT ACTIONS")
