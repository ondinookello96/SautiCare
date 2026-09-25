"""
SautiCare Agent Engine
Provides culturally grounded reasoning in Swahili with elder-respectful honorifics (Heshima kwa Wazee),
intent recognition, and function/tool execution for emergencies, M-Pesa, and smartphone features.
"""

import re
from typing import Dict, Any

SWAHILI_SYSTEM_PROMPT = """
Wewe ni "SautiCare", msaidizi wa sauti mwenye heshima, subira, na upendo kwa wazee barani Afrika, hususan Afrika Mashariki (Kenya, Tanzania, Uganda n.k.).

MAADILI NA SAUTI YAKO (PERSONA):
1. Heshima kwa Wazee: Kila mara anza kwa heshima, ukitumia salamu za kiutamaduni kama "Shikamoo Mama" au "Shikamoo Mzee" au "Marahaba".
2. Lugha Rahisi: Usitumie maneno magumu ya kiteknolojia kama "interface", "cache", "operating system". Tumia maneno ya kawaida (mfano: "kitufe cha kijani", "kubonyeza", "ujumbe", "kupiga simu").
3. Subira na Ukarimu: Zungumza kwa utulivu na polepole. Mzee asihisi kuhimizwa au kuogopa kukosea.
4. Hali ya Dharura (Emergency): Ikiwa mzee anasema ameanguka, anaumwa, au anahitaji msaada wa haraka, zungumza kwa utulivu kumtuliza na mara moja piga kengele ya dharura.

MAENEO YA MSINGI (CORE AREAS):
1. Dharura (Emergency SOS): Mzee akianguka au akiwa mgonjwa peke yake nyumbani.
2. M-Pesa / Pesa kwa Simu: Kumsaidia kutuma pesa au kuangalia salio bila hofu ya kutuma kwa nambari isiyo sahihi. Kila mara muulize jina la mpokeaji ili athibitishe kabla ya kutuma.
3. Matumizi ya Simu: Kuwasha tochi gizani, kupiga simu kwa watoto/familia, kusoma ujumbe, au kurekebisha sauti ya simu.
"""

class AgentEngine:
    def __init__(self):
        self.emergency_contact = {
            "name": "Mwanangu Juma",
            "phone": "+254712345678",
            "relationship": "Mwanafamilia wa karibu"
        }

    def process_swahili_intent(self, text: str) -> Dict[str, Any]:
        """
        Analyze transcribed Swahili speech, classify intent, and execute the corresponding tool.
        Supports natural code-switching (Swahili + Sheng / English terms).
        """
        lower = text.lower().strip()

        # 1. Greetings (Shikamoo, Habari, Hujambo) - checked early unless emergency/action attached
        greeting_words = ["shikamoo", "habari", "hujambo", "jambo", "mambo", "hello", "asalaam"]
        is_greeting = any(re.search(rf"\b{gw}\b", lower) for gw in greeting_words)
        has_other_intent = any(w in lower for w in ["tochi", "pesa", "mpesa", "dharura", "anguka", "umwa", "betri"])

        if is_greeting and not has_other_intent:
            return {
                "action": "greeting",
                "swahili_response": "Marahaba Mzee wangu! Mimi ni SautiCare, msaidizi wako wa karibu. Niko hapa kukusaidia kutumia simu yako, kuangalia Em-pesa, au kupiga simu kwa dharura. Nikusaidie na nini leo?",
                "english_translation": "Greetings elder! I am SautiCare, your voice assistant. I am here to help you navigate your phone, check M-Pesa, or make emergency calls. How may I help you today?",
                "visual_card": {
                    "type": "welcome",
                    "title": "Karibu SautiCare",
                    "details": "Nisikilize nikikuelekeza kwa sauti yako ya Kiswahili."
                }
            }

        # 2. M-Pesa / Mobile Money Intent Detection
        mpesa_keywords = [
            "pesa", "mpesa", "m-pesa", "shilingi", "tuma", "salio", "kutoa pesa", 
            "lipa", "bando", "airtime", "send money", "balance"
        ]
        has_mpesa = any(kw in lower for kw in mpesa_keywords)

        # 3. Emergency Intent Detection
        pure_emergency_words = [
            "dharura", "nimeanguka", "anguka", "naumwa", "vibaya", "hospitali", 
            "kizunguzungu", "damu", "emergency", "kuanguka", "peke yangu", "sijisikii vizuri"
        ]
        has_pure_emergency = any(kw in lower for kw in pure_emergency_words)

        if has_pure_emergency or (("nisaidie" in lower or "help" in lower) and not has_mpesa and "tochi" not in lower):
            return self.tool_trigger_emergency_sos(
                distress_type="Matatizo ya Kiafya / Kuanguka",
                details=text
            )

        if has_mpesa:
            return self.tool_guide_mpesa_transfer(query=text)

        # 4. Device Controls Intent Detection
        # Flashlight / Torch
        if "tochi" in lower or "torch" in lower or "giza" in lower or "mwanga" in lower:
            state = "off" if ("zima" in lower or "off" in lower) else "on"
            return self.tool_control_phone_feature(action=f"torch_{state}", query=text)

        # Phone Call / WhatsApp to family
        if "piga simu" in lower or "call" in lower or "ongea" in lower or "whatsapp" in lower:
            return self.tool_control_phone_feature(action="call_family", query=text)

        # Battery / Charge status
        if "betri" in lower or "battery" in lower or "chaji" in lower:
            return self.tool_control_phone_feature(action="check_battery", query=text)

        # Volume / Sauti (use word boundaries to avoid matching SautiCare)
        if re.search(r"\b(sauti|volume)\b", lower) and ("ongeza" in lower or "punguza" in lower or "weka" in lower or "kubwa" in lower):
            return self.tool_control_phone_feature(action="adjust_volume", query=text)

        # Default fallback guidance
        return {
            "action": "guidance",
            "swahili_response": f"Nimekuelewa vizuri Mzee wangu. Unaweza kuniambia kwa urahisi: Washa tochi, Nisaidie na Em-pesa, au ukipata shida sema tu Nisaidie dharura.",
            "english_translation": f"I understood you well. You can simply tell me: Turn on torch, Help with M-Pesa, or in trouble say Emergency help.",
            "visual_card": {
                "type": "suggestion",
                "title": "Mifano ya Kusema",
                "items": [
                    "Washa tochi (gizani)",
                    "Nataka kutuma pesa kwa M-Pesa",
                    "Nisaidie nimeanguka (Dharura)",
                    "Piga simu kwa Juma"
                ]
            }
        }

    def tool_trigger_emergency_sos(self, distress_type: str, details: str) -> Dict[str, Any]:
        """
        Emergency SOS Tool: Dispatches simulated SMS with GPS and initiates emergency call.
        Works in both online and offline mode.
        """
        gps_coords = "1°17'31.2\"S 36°49'10.8\"E (Nairobi, Kenya)"
        return {
            "action": "emergency_sos",
            "is_emergency": True,
            "swahili_response": "Tulia Mzee wangu, usijali wala usiogope. Nimeshatuma ujumbe mfupi wa dharura pamoja na mahali ulipo kwa mwanao Juma, na sasa ninapiga simu ya msaada mara moja.",
            "english_translation": "Stay calm elder, do not be afraid. I have already dispatched an emergency SMS with your live location to your child Juma, and I am calling for help immediately.",
            "visual_card": {
                "type": "sos_card",
                "status": "DHARURA IMETUMWA (SOS SENT)",
                "recipient": self.emergency_contact["name"],
                "phone": self.emergency_contact["phone"],
                "location": gps_coords,
                "sms_preview": f"DHARURA: Mzazi wako anahitaji msaada wa haraka nyumbani! Mahali: {gps_coords}. Piga simu mara moja.",
                "gsm_dialer_intent": f"tel:{self.emergency_contact['phone']}"
            }
        }

    def tool_guide_mpesa_transfer(self, query: str) -> Dict[str, Any]:
        """
        M-Pesa Guidance Tool: Guides the elder through safe money transfers step-by-step
        to prevent sending to the wrong number.
        """
        return {
            "action": "mpesa_guide",
            "swahili_response": "Shikamoo Mama. Kwenye Em-pesa, usalama wako ni muhimu sana. Piga nyota tatu tatu nne reli kwenye simu yako, kisha uhakikishe jina la mpokeaji linaonekana wazi kwenye skrini kabla ya kuweka namba yako ya siri.",
            "english_translation": "Greetings Mama. On M-Pesa, your safety is very important. Dial star 3 3 4 hash on your phone, then verify the recipient's name is clearly shown on screen before entering your secret PIN.",
            "visual_card": {
                "type": "mpesa_safety",
                "title": "Hatua Salama za M-Pesa",
                "ussd_code": "*334# (Njia ya Nje ya Mtandao / Offline)",
                "steps": [
                    "1. Piga nambari *334# kwenye simu yako",
                    "2. Chagua '1: Tuma Pesa'",
                    "3. Weka nambari ya simu ya mpokeaji",
                    "4. ANGALIA JINA KWANZA kabla ya kuweka PIN!",
                    "5. Weka nambari yako ya siri kwa siri"
                ],
                "warning": "Usitoe nambari yako ya siri (PIN) kwa mtu yeyote, hata akisema anapiga simu kutoka kampuni ya simu."
            }
        }

    def tool_control_phone_feature(self, action: str, query: str) -> Dict[str, Any]:
        """
        Phone Feature Accessibility Tool: Controls flashlight, volume, battery, calls.
        """
        if action == "torch_on":
            return {
                "action": "torch_on",
                "swahili_response": "Tayari nimewasha tochi ya simu yako ili uweze kuona vizuri gizani.",
                "english_translation": "I have turned on your phone's flashlight so you can see clearly in the dark.",
                "visual_card": {
                    "type": "device_action",
                    "title": "Tochi Imewashwa 🔦",
                    "details": "Mwanga wa simu umewashwa kwa usalama wako."
                }
            }
        elif action == "torch_off":
            return {
                "action": "torch_off",
                "swahili_response": "Nimezima tochi ya simu yako.",
                "english_translation": "I have turned off your phone's flashlight.",
                "visual_card": {
                    "type": "device_action",
                    "title": "Tochi Imezimwa",
                    "details": "Mwanga umezimwa kuhifadhi chaji."
                }
            }
        elif action == "call_family":
            return {
                "action": "call_family",
                "swahili_response": f"Ninampigia simu mwanao {self.emergency_contact['name']} sasa hivi. Shikilia simu sikioni mwako.",
                "english_translation": f"I am calling your child {self.emergency_contact['name']} right now. Hold the phone to your ear.",
                "visual_card": {
                    "type": "call_dialer",
                    "title": f"Inapiga simu: {self.emergency_contact['name']}",
                    "phone": self.emergency_contact["phone"],
                    "dialer_intent": f"tel:{self.emergency_contact['phone']}"
                }
            }
        elif action == "check_battery":
            return {
                "action": "check_battery",
                "swahili_response": "Betri ya simu yako iko asilimia themanini na tano. Chaji inatosha kabisa kwa siku nzima ya leo.",
                "english_translation": "Your phone's battery is at 85%. You have plenty of charge for the rest of today.",
                "visual_card": {
                    "type": "battery_card",
                    "title": "Hali ya Betri: 85% 🔋",
                    "details": "Simu yako ina chaji ya kutosha. Hakuna haja ya kuchomeka kwa sasa."
                }
            }
        elif action == "adjust_volume":
            return {
                "action": "adjust_volume",
                "swahili_response": "Nimeongeza sauti ya simu hadi mwisho kabisa ili uweze kusikia vizuri kila neno linalosemwa.",
                "english_translation": "I have raised your phone's volume to maximum so you can hear every word clearly.",
                "visual_card": {
                    "type": "volume_card",
                    "title": "Sauti Imeongezwa 🔊",
                    "details": "Kiwango cha sauti: 100% kwa ajili ya kusikia vizuri."
                }
            }
        return {
            "action": "unknown",
            "swahili_response": "Nipo hapa kukusaidia Mzee wangu. Niambie chochote unachohitaji kwenye simu yako.",
            "english_translation": "I am here to help you elder. Tell me anything you need with your phone."
        }
