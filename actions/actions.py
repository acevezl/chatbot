# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import random
import string

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted

class ActionSessionStart(Action):
	def name(self):
		return "action_session_start"

	def run(self, dispatcher, tracker, domain):
		# Forzar utter greeet para que nos diga hola al principio
		dispatcher.utter_message(response="utter_greet")

		return [SessionStarted(), ActionExecuted("action_listen")]


class ActionConfirmPizzaOrder(Action):
	def name(self):
		return "action_confirm_pizza_type_order"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
		pizza_size = tracker.get_slot("pizza_size")
		pizza_type = tracker.get_slot("pizza_type")

		base_prices = {
			"small": 12,
			"medium": 14,
			"large": 18,
		}

		price = base_prices.get(pizza_size, 0)

		if pizza_type and pizza_type.lower() == "margherita":
			price -= 2

		pickup_id = self.generate_code(4)

		dispatcher.utter_message(
			text=(
				f"Your {pizza_size} {pizza_type} pizza is confirmed. "
				f"The total is {price} euro. "
				f"Your pickup identifier is {pickup_id}."
			)
		)

		return []

	def generate_code(self, k=4):
		return f"PIZZA-{random.choices(string.ascii_uppercase + string.digits, k)}"
    
class ActionConfirmDrinksOrder(Action):

    def name(self) -> Text:
        return "action_confirm_drinks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []