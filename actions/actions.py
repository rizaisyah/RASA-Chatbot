from typing import Any, List, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, EventType

class ActionContactITSupport(Action):
    def name(self) -> str:
        return "action_contact_it_support"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(
            text="Sepertinya saya masih belum bisa mengenali pertanyaan Anda. Silakan menghubungi tim IT untuk layanan lebih lanjut di email: tik.sv@ugm.ac.id."
        )
        return []

class CustomSessionStart(Action):
    def name(self) -> str:
        return "action_session_start"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[EventType]:
        return [SessionStarted()]
