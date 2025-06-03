from typing import Any, List, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, EventType, SlotSet, FollowupAction

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
    

class ActionFilterByDevice(Action):
    def name(self):
        return "action_filter_by_device"

    def run(self, dispatcher, tracker, domain):
        device = tracker.get_slot("device_type")
        intent = tracker.latest_message.get("intent", {}).get("name")

        ap_intents = ["ap_connection_problem", "ap_login_secure", "ap_login_hotspot"]
        lan_intents = ["lan_connection_problem"]
        tv_intents = ["tv_connect_device", "tv_bluetooth", "tv_soundbar", "tv_remot", "tv_layar_hdmi", "tv_network", "tv_mati"]

        if device == "AP" and intent in ap_intents:
            return []
        elif device == "LAN" and intent in lan_intents:
            return []
        elif device == "Smart TV" and intent in tv_intents:
            return []
        else:
            dispatcher.utter_message(
                text=f"Permasalahan '{intent}' tidak sesuai dengan perangkat yang Anda pilih ({device}). Silakan pilih ulang dari menu."
            )
            # Kosongkan slot supaya tidak digunakan lagi
            return [SlotSet("device_type", None), FollowupAction(name="action_listen")]



class ActionShowSlots(Action):
    def name(self):
        return "action_show_slots"

    def run(self, dispatcher, tracker, domain):
        device = tracker.get_slot("device_type")
        dispatcher.utter_message(f"[DEBUG] Slot device_type berisi: {device}")
        return []
