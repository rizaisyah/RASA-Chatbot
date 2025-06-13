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
    
class ActionIdentifyDevice(Action):
    def name(self) -> str:
        return "action_identify_device"

    def run(self, dispatcher, tracker, domain):
        os_type = tracker.get_slot("os_type")

        if os_type == "Windows":
            dispatcher.utter_message(text="Ikuti panduan ini untuk Windows:\n" \
            "1. Koneksikan wifi ke UGM-Secure.\n" \
            "2. Muncul halaman login yang berisikan username dan password. Isikan dengan username tanpa @mail.ugm.ac.id dan password yang sama dengan SSO UGM.\n" \
            "3. Jika sudah, klik OK, kemudian jika muncul Verify Certificate pilih Connect untuk memverifikasi.")
        elif os_type == "MacOS":
            dispatcher.utter_message(text="Ikuti panduan ini untuk MacOS:\n" \
            "1. Koneksikan wifi ke UGM-Secure.\n" \
            "2. Muncul halaman login yang berisikan username dan password. Isikan dengan username tanpa @mail.ugm.ac.id dan password yang sama dengan SSO UGM.\n" \
            "3. Jika muncul pop up Verify Certificate pilih Continue untuk memverifikasi.")
        elif os_type == "Android":
            dispatcher.utter_message(text="Ikuti panduan ini untuk Android:\n" \
            "1. Koneksikan wifi ke UGM-Secure.\n" \
            "2. Isi form sebagai berikut:\n" \
            "EAP METHOD: TTLS\n" \
            "HASE 2 AUTHENTICATION : PAP\n" \
            "CA CERTIFICATE: (unspecified)\n" \
            "Identity: email ugm @mail.ugm.ac.id\n" \
            "Anonymous identity: email ugm\n" \
            "Password: password email ugm\n" \
            "3. Kemudian klik connect.")
        elif os_type == "iPhone":
            dispatcher.utter_message(text="Ikuti panduan ini untuk iPhone:\n" \
            "1. Klik setting WLAN pada iPhone.\n" \
            "2. Muncul halaman login yang berisikan username dan password. Isikan dengan username tanpa '@mail.ugm.ac.id' dan password yang sama dengan SSO UGM.\n" \
            "3. Pilih Trust untuk memverifikasi Certificate.")
        else:
            dispatcher.utter_message(text="OS tidak dikenali. Silakan pilih antara Windows, MacOS, Android, atau iPhone.")

        dispatcher.utter_message(text="Untuk login ke UGM Secure, pastikan Anda memasukkan username dan password yang benar.")
        
        return []

