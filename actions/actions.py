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

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet

import random
import string

PIZZA_PRICES = {
	"small": 12,
	"medium": 14,
	"large": 18,
}

PIZZA_PROMOS = {
	"margherita": -2,
}

DRINK_PRICE = 3


# Function to get entity (pizza_size, pizza_drink, pizza_type, etc.)
def get_entity(tracker: Tracker, entity_name: Text):
	entities = tracker.latest_message.get("entities", [])

	for entity in entities:
		if entity.get("entity") == entity_name:
			return entity.get("value")

	return None

# Function to summarize order
def summarize_order(tracker: Tracker):
	items = tracker.get_slot("order_items") or []
	total = tracker.get_slot("order_total") or 0

	if not items:
		return None

	lines = []

	for item in items:
		if item["type"] == "pizza":
			lines.append(f"+ {item['size']} {item['name']} pizza: {item['price']} €")
			if item['promo'] != 0:
				lines.append(f"   - promo: {item['promo']} €")
		elif item["type"] == "drink":
			lines.append(f"+ {item['name']}: {item['price']} €")

	text=(
		"Here's your order:\n"
		+ "\n".join(lines)
		+ f"\n====================\nTotal: {total} €"
	)

	return text
	

class ActionStartRestartOrder(Action):

	def name(self) -> Text:
		return "action_start_restart_order"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		return [
			SlotSet("order_started", True),
			SlotSet("order_items", []),
			SlotSet("order_total", 0),
			SlotSet("pizza_type", None),
			SlotSet("pizza_size", None),
			SlotSet("drink", None),
			SlotSet("pickup_code", None),
		]
	
class ActionAddPizzaToOrder(Action):

	def name(self) -> Text:
		return "action_add_pizza_to_order"
	
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		
		pizza_type = get_entity(tracker, "pizza_type") or tracker.get_slot("pizza_type")
		pizza_size = get_entity(tracker, "pizza_size") or tracker.get_slot("pizza_size")
	
		print (f"DEBUG: pizza_type={pizza_type}, pizza_size={pizza_size}")
		if not pizza_type and not pizza_size:
			dispatcher.utter_message(response="utter_ask_pizza_type")
			return []
		elif not pizza_type:
			dispatcher.utter_message(response="utter_ask_pizza_type")
			return [SlotSet("pizza_size", pizza_size)]
		elif not pizza_size:
			dispatcher.utter_message(response="utter_ask_pizza_size")
			return [SlotSet("pizza_type", pizza_type)]

		order_items = tracker.get_slot("order_items") or []
		order_total = tracker.get_slot("order_total") or 0

		pizza_size = pizza_size.lower()

		if pizza_size in ["l","lg"]:
			pizza_size = "large"
		if pizza_size in ["m","md","med"]:
			pizza_size = "medium"
		if pizza_size in ["s","sm"]:
			pizza_size = "small"

		price = PIZZA_PRICES.get(pizza_size.lower(), 0)
		promo = PIZZA_PROMOS.get(pizza_type.lower(), 0)

		item = {
			"type": "pizza",
			"name": pizza_type,
			"size": pizza_size,
			"price": price,
			"promo": promo,
		}

		order_items.append(item)
		order_total += price + promo

		dispatcher.utter_message(
			text=f"I've added a {pizza_size} {pizza_type} pizza to your order"
		)

		dispatcher.utter_message(response="utter_ask_what_else")

		return [
			SlotSet("order_started", True),
			SlotSet("order_items", order_items),
			SlotSet("order_total", order_total),
			SlotSet("pizza_type", None),
			SlotSet("pizza_size", None),
		]
	
class ActionAddDrinkToOrder(Action):

	def name(self) -> Text:
		return "action_add_drink_to_order"
	
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
	
		drink = get_entity(tracker, "drink") or tracker.get_slot("drink")

		if not drink:
			dispatcher.utter_message(response="utter_ask_drink_type")
			return []

		order_items = tracker.get_slot("order_items") or []
		order_total = tracker.get_slot("order_total") or 0

		item = {
			"type": "drink",
			"name": drink,
			"price": DRINK_PRICE,
		}

		order_items.append(item)
		order_total += DRINK_PRICE

		dispatcher.utter_message(
			text=f"I've added a {drink} to your order."
		)

		dispatcher.utter_message(response="utter_ask_what_else")

		return [
			SlotSet("order_started", True),
			SlotSet("order_items", order_items),
			SlotSet("order_total", order_total),
			SlotSet("drink", None),
		]

class ActionConfirmOrder(Action):

	def name(self) -> Text:
		return "action_confirm_order"
	
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
	
		order_items = tracker.get_slot("order_items") or []

		if not order_items:
			dispatcher.utter_message(response="utter_empty_order")
			return []
		
		summary = summarize_order(tracker)

		dispatcher.utter_message(summary)
		dispatcher.utter_message(response="utter_confirm")

		return []

class ActionSubmitOrder(Action):

	def name(self) -> Text:
		return "action_submit_order"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		
		pickup_code = tracker.get_slot("pickup_code")

		if not pickup_code:
			pickup_code = "PIZZA-" + "".join(
				random.choices(string.ascii_uppercase + string.digits, k=4)
			)

		dispatcher.utter_message(
			text=(
				f"Here's your pickup code: {pickup_code}\n"
			)
		)

		return [SlotSet("pickup_code", pickup_code)]