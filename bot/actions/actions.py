# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from nsetools import Nse
import requests

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

class ActionStockInfo(Action):

    def name(self) -> Text:
        return "action_stock_info"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message["entities"]
        nse = Nse()
        name = ""
        msg = ""
        for e in entities:
            if e["entity"] == "st_list":
                name = e["value"]

        q = nse.get_quote(name)
        msg = name.upper() +" Day High: " + str(q["dayHigh"]) +" Day Low: " + str(q["dayLow"])+" Average Price: " + str(q["averagePrice"])+" Change: " + str(q["change"])+" Delivery Quantity " + str(q["deliveryQuantity"])+" pChange " + str(q["pChange"])

        dispatcher.utter_message(msg)

        return []
     
class ActionNewsInfo(Action):

    def name(self) -> Text:
        return "action_news_info"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = ""
        msg = ""
        url = ('http://newsapi.org/v2/top-headlines?'
        'country=in&'
        'apiKey=13ea6a7e0a9d4361999cad03e219bb69')
        response = requests.get(url)
        data = response.json()
        for article in data["articles"]:
            dispatcher.utter_message(text=article["description"])
            dispatcher.utter_message(image=article['urlToImage'])

        return []
