from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
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

        dispatcher.utter_message(
            template="utter_confirm_order", clothes_details=clothes_details
        )

        return [AllSlotsReset()]
