# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.types import DomainDict

import webbrowser   # inbuilt in python to open in webbrowser


#to reset slots, used before action_name_form
class ResetAllSlots(Action):

    def name(self) -> Text:
        return "action_reset_slots"  # this has to correspond to the action_name_form in domain

    async def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()] # reset all slots value

class validate_name_form(FormValidationAction):
    '''
    validation for form will be applied after every form slot is filled.
    '''

    def name(self) -> Text:
        return "validate_name_form"

    # @staticmethod
    # def check_reset_form_action_on_intent(tracker = Tracker, dispatcher=CollectingDispatcher):
    #     last_intent = tracker.latest_message['intent'].get('name')
    #     if last_intent == 'stop_registration':
    #         dispatcher.utter_message('Stop intent detected')
    #         return True
    #     else:
    #         return False

    # function to validate name
    # def validate_name(self,
    #     slot_value: float,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,) -> Dict[Text, Any]:
    #     reset = self.check_reset_form_action_on_intent(tracker= Tracker, dispatcher=CollectingDispatcher)
    #     if reset: # detect stop intent highest priority
    #         return (ActiveLoop(None))
    #     else:
    #         return {"name": slot_value}


    def validate_contact_no(self,
        slot_value: float,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:
        #extracted_slots: Dict[Text,Any]= tracker.slots_to_validate()
        # reset = self.check_reset_form_action_on_intent(tracker= Tracker, dispatcher=CollectingDispatcher)
        # if reset:# detect stop intent highest priority
        #     return (ActiveLoop(None))
        if self.check_int(slot_value) and len(slot_value) > 2: #if true
            return {"contact_no":slot_value}
        else:
            dispatcher.utter_message("Erm input is invalid, try again.")
            return {"contact_no": None}

    # def validate_organisation(self,
    #     slot_value: float,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,) -> Dict[Text, Any]:
    #     reset = self.check_reset_form_action_on_intent(tracker= Tracker, dispatcher=CollectingDispatcher)
    #     if reset: # detect stop intent highest priority
    #         return (ActiveLoop(None))
    #     else:
    #         return {"organisation": slot_value}

    @staticmethod
    def check_int(string: Text) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False




class ActionRequestConsulation(Action):


    def name(self) -> Text:
        return "action_name_form"  # this has to correspond to the action_name_form in domain

    # boiler plate code, but what do they each mean?
    async def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],) -> List[Dict[Text, Any]]:

        for slot_name in required_slots:
            if self.check_reset_form_action_on_intent(tracker= Tracker, dispatcher=CollectingDispatcher): # detect stop intent highest priority
                return [ActiveLoop(None)]
            elif tracker.get_slot(slot_name) is None:
                return (SlotSet("required_slots",slot_name))
        # all slots are filled
        return [SlotSet("required_slots",None)]


    @staticmethod
    def check_reset_form_action_on_intent(tracker= Tracker, dispatcher=CollectingDispatcher):
        last_intent = tracker.latest_message['intent'].get('name')
        if last_intent == 'stop_registration':
            dispatcher.utter_message('Stop intent detected')
            return True
        else:
            return False
#class to submit details
class ActionSubmit(Action):

    def name(self) -> Text:
        return "action_submit" # this will correspond to the action_submit under domain

    async def run(
        self, dispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template= "utter_register_verification",
                                 Name = tracker.get_slot("name"),   # the Name, Contact_Number, Organisation variables will be displayed in a verification message
                                 Contact_Number = tracker.get_slot("contact_no"),
                                 Organisation= tracker.get_slot("organisation"))




# to play a video defined earlier --> how do you modify to search online on google?
class ActionVideo(Action):

    def name(self) -> Text:
        return "action_video"  # this will be your name for custom action in domain.yml

    async def run(
        self, dispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        video_url = "https://www.youtube.com/watch?v=iEUuwhHgbbg"

        dispatcher.utter_message(text="wait... loading your video...")  # this is the display message user sees before video will display
        webbrowser.open(video_url)  # get the video_url variable defined previously

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
