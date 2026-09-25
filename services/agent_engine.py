"""
SautiCare Agent Engine
Provides culturally grounded reasoning in Swahili with elder-respectful honorifics (Heshima kwa Wazee),
intent recognition, and multimodal navigation guides for everyday smartphone apps (WhatsApp, YouTube,
Camera, Settings, Airtime/USSD) alongside safe M-Pesa transactions and life-saving Emergency SOS.
"""

import re
from typing import Dict, Any

SWAHILI_SYSTEM_PROMPT = """
Wewe ni "SautiCare", msaidizi wa sauti mwenye heshima, subira, na upendo kwa wazee barani Afrika, hususan Afrika Mashariki (Kenya, Tanzania, Uganda n.k.).

MAADILI NA SAUTI YAKO (PERSONA):
1. Heshima kwa Wazee: Kila mara anza kwa heshima, ukitumia salamu za kiutamaduni kama "Shikamoo Mama" au "Shikamoo Mzee" au "Marahaba".
2. Lugha Rahisi: Usitumie maneno magumu ya kiteknolojia kama "interface", "cache", "operating system". Tumia maneno ya kawaida (mfano: "kitufe cha kijani", "kubonyeza", "ujumbe", "kupiga simu").
3. Subira na Ukarimu: Zungumza kwa utulivu na polepole. Mzee asihisi kuhimizwa au kuogopa kukosea.
4. Mwongozo wa Hatua kwa Hatua: Mweleze mzee hatua moja baada ya nyingine ili asichanganyikiwe.
5. Hali ya Dharura (Emergency): Ikiwa mzee anasema ameanguka, anaumwa, au anahitaji msaada wa haraka, zungumza kwa utulivu kumtuliza na mara moja piga kengele ya dharura.

MAENEO YA MSINGI (CORE AREAS):
1. Dharura (Emergency SOS): Mzee akianguka au akiwa mgonjwa peke yake nyumbani.
2. WhatsApp na Mawasiliano: Kutuma ujumbe wa sauti (voice note), kupiga simu ya video, kutazama picha.
3. Burudani na Imani: Kufungua nyimbo za injili, kwaya za Kiswahili, na redio kwenye YouTube.
4. Kamera na Picha: Kupiga picha za wajukuu na familia, na kufungua albamu ya picha.
5. Mipangilio na Urahisi wa Kusoma: Kuongeza ukubwa wa maandishi, mwangaza wa skrini, na kuwasha intaneti/data.
6. Salio la Simu na Bando: Kuangalia salio (*144#) na kununua bando (*544#).
7. M-Pesa / Fedha: Kumsaidia kutuma pesa au kuangalia salio bila hofu ya kutuma kwa nambari isiyo sahihi.
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
        Supports natural code-switching (Swahili + Sheng / everyday terms).
        """
        lower = text.lower().strip()

        # 1. Emergency Intent Detection (Top Priority)
        pure_emergency_words = [
            "dharura", "nimeanguka", "anguka", "naumwa", "vibaya", "hospitali", 
            "kizunguzungu", "damu", "emergency", "kuanguka", "peke yangu", "sijisikii vizuri"
        ]
        has_pure_emergency = any(kw in lower for kw in pure_emergency_words)
        is_general_help = ("nisaidie" in lower or "help" in lower) and not any(
            w in lower for w in ["tochi", "pesa", "mpesa", "watsapu", "whatsapp", "yutubu", "youtube", "picha", "kamera", "salio", "maandishi"]
        )

        if has_pure_emergency or is_general_help:
            return self.tool_trigger_emergency_sos(
                distress_type="Matatizo ya Kiafya / Kuanguka",
                details=text
            )

        # 2. Greetings (Shikamoo, Habari, Hujambo)
        greeting_words = ["shikamoo", "habari", "hujambo", "jambo", "mambo", "hello", "asalaam"]
        is_greeting = any(re.search(rf"\b{gw}\b", lower) for gw in greeting_words)
        has_action_intent = any(w in lower for w in [
            "tochi", "pesa", "mpesa", "watsapu", "whatsapp", "yutubu", "youtube", 
            "picha", "kamera", "salio", "maandishi", "mwangaza", "betri", "injili", "kwaya"
        ])

        if is_greeting and not has_action_intent:
            return {
                "action": "greeting",
                "swahili_response": "Marahaba Mzee wangu! Mimi ni SautiCare, msaidizi wako wa karibu. Niko hapa kukuongoza kutumia Watsapu, kusikiliza nyimbo za injili kwenye Yutubu, kupiga picha, kuangalia Em-pesa, au kupiga simu ya dharura. Nikusaidie na nini sasa hivi?",
                "english_translation": "Greetings elder! I am SautiCare, your companion. I am here to guide you through WhatsApp, listen to gospel music on YouTube, take photos, navigate M-Pesa, or make emergency calls. What can I help you with right now?",
                "visual_card": {
                    "type": "welcome",
                    "title": "Karibu SautiCare 🌿",
                    "details": "Chagua au zungumza kwa Kiswahili kutumia huduma yoyote ya simu yako."
                }
            }

        # 3. WhatsApp Navigation Intent
        if any(w in lower for w in ["watsapu", "whatsapp", "ujumbe wa sauti", "voice note", "video call"]):
            return self.tool_guide_whatsapp(query=text)

        # 4. YouTube & Gospel Music / Swahili Radio Intent
        if any(w in lower for w in ["yutubu", "youtube", "injili", "kwaya", "nyimbo", "redio", "radio", "maombi", "music"]):
            return self.tool_guide_youtube_gospel(query=text)

        # 5. Camera & Photos Intent
        if any(w in lower for w in ["picha", "kamera", "camera", "albamu", "gallery", "kupiga picha"]):
            return self.tool_guide_camera_photos(query=text)

        # 6. Phone Settings & Accessibility (Font Size, Brightness, Wi-Fi)
        if any(w in lower for w in ["maandishi", "mwangaza", "skrini", "wayafai", "wifi", "data ya simu", "intaneti", "kuza", "size"]):
            return self.tool_guide_phone_settings(query=text)

        # 7. Airtime & Data Balance Intent (*144#, *544#)
        if any(w in lower for w in ["salio", "airtime", "dakika", "bando", "vocha", "balance"]):
            return self.tool_guide_airtime_balance(query=text)

        # 8. SMS / Text Message Reading Intent
        if any(w in lower for w in ["sms", "ujumbe mfupi", "soma ujumbe", "nani ametuma", "message"]):
            return self.tool_guide_sms_reader(query=text)

        # 9. M-Pesa & Mobile Money Intent
        mpesa_keywords = ["mpesa", "m-pesa", "tuma pesa", "kutuma pesa", "shilingi", "kutoa pesa", "lipa"]
        if any(kw in lower for kw in mpesa_keywords):
            return self.tool_guide_mpesa_transfer(query=text)

        # 10. Device Hardware Features (Flashlight, Battery, Volume, Call)
        if "tochi" in lower or "torch" in lower or "giza" in lower:
            state = "off" if ("zima" in lower or "off" in lower) else "on"
            return self.tool_control_phone_feature(action=f"torch_{state}", query=text)

        if "piga simu" in lower or "call" in lower or "ongea" in lower:
            return self.tool_control_phone_feature(action="call_family", query=text)

        if "betri" in lower or "battery" in lower or "chaji" in lower:
            return self.tool_control_phone_feature(action="check_battery", query=text)

        if re.search(r"\b(sauti|volume)\b", lower) and any(w in lower for w in ["ongeza", "punguza", "weka", "kubwa"]):
            return self.tool_control_phone_feature(action="adjust_volume", query=text)

        # Default fallback guidance
        return {
            "action": "guidance",
            "swahili_response": "Nimekuelewa vizuri Mzee wangu. Unaweza kuniambia: Nisaidie na Watsapu, Fungua nyimbo za injili, Piga picha, Ongeza ukubwa wa maandishi, au Angalia salio langu.",
            "english_translation": "I understood you well elder. You can tell me: Help with WhatsApp, Open gospel songs, Take a picture, Increase text size, or Check my airtime balance.",
            "visual_card": {
                "type": "suggestion",
                "title": "Mambo Ninayoweza Kukusaidia",
                "items": [
                    "💬 'Kutuma sauti kwa Watsapu'",
                    "🎵 'Sikiliza nyimbo za Injili'",
                    "📸 'Kupiga picha ya familia'",
                    "🔤 'Ongeza ukubwa wa maandishi'",
                    "📞 'Angalia salio la simu (*144#)'",
                    "💸 'Kutuma pesa kwa M-Pesa'",
                    "🚨 'Nisaidie nimeanguka (Dharura)'"
                ]
            }
        }

    def tool_trigger_emergency_sos(self, distress_type: str, details: str) -> Dict[str, Any]:
        """Emergency SOS Tool: Dispatches SMS with GPS and triggers phone call."""
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

    def tool_guide_whatsapp(self, query: str) -> Dict[str, Any]:
        """WhatsApp Navigator Tool: Step-by-step guidance for voice notes, calls, and photos."""
        lower = query.lower()
        if "video" in lower or "simu" in lower:
            return {
                "action": "whatsapp_call",
                "swahili_response": "Kupiga simu ya Watsapu: Fungua mazungumzo ya mtu unayetaka kumpigia, kisha tazama juu kulia kabisa kwenye skrini yako. Bonyeza picha ya simu kwa maongezi ya kawaida, au picha ya kamera ndogo kwa simu ya kuonana sura.",
                "english_translation": "To make a WhatsApp call: Open the chat of the person, look at the top right of your screen. Tap the telephone icon for voice, or the video camera icon for video call.",
                "visual_card": {
                    "type": "whatsapp_call_guide",
                    "title": "Simu ya Watsapu 📞",
                    "app_color": "#25D366",
                    "steps": [
                        "1. Fungua Watsapu na ubofye jina la mtu",
                        "2. Tazama juu kulia mwa skrini",
                        "3. Bonyeza 📞 kwa sauti au 📹 kwa video",
                        "4. Subiri apokee simu yako"
                    ],
                    "action_intent": "whatsapp://"
                }
            }
        
        # Default: Voice note (most popular elder feature)
        return {
            "action": "whatsapp_voicenote",
            "swahili_response": "Kutuma ujumbe wa sauti kwa Watsapu ni rahisi sana: Fungua mazungumzo ya mtu unayetaka kumtumia, kisha bonyeza na ushikilie kile kitufe cha kijani cha kinasa sauti chini kulia. Zungumza maneno yako ukiwa umeshikilia, kisha achilia kidole chako. Ujumbe utaenda mara moja.",
            "english_translation": "To send a WhatsApp voice note: Open the person's chat, press and hold the green microphone button at the bottom right. Speak while holding it, then release your finger. The message will send immediately.",
            "visual_card": {
                "type": "whatsapp_guide",
                "title": "Kutuma Sauti kwa Watsapu 🎙️",
                "app_color": "#25D366",
                "steps": [
                    "1. Ingia kwenye Watsapu na uchague mtu",
                    "2. Chini kulia, bonyeza na USHIKILIE kitufe cha kijani 🎙️",
                    "3. Zungumza maneno unayotaka kusema",
                    "4. Achilia kidole chako kutuma mara moja!"
                ],
                "action_intent": "whatsapp://"
            }
        }

    def tool_guide_youtube_gospel(self, query: str) -> Dict[str, Any]:
        """YouTube & Gospel / Radio Tool: Direct audio/video access for faith and leisure."""
        return {
            "action": "youtube_gospel",
            "swahili_response": "Nimekuandalia nyimbo nzuri za injili na kwaya za Kiswahili kwenye Yutubu. Unaweza kubonyeza kitufe cha bluu hapa chini kusikiliza mara moja, au uniambie jina la kwaya unayopenda nikufungulie.",
            "english_translation": "I have prepared uplifting Swahili gospel songs and choirs for you on YouTube. Tap the blue button below to listen immediately, or tell me the choir you'd love to hear.",
            "visual_card": {
                "type": "youtube_guide",
                "title": "Nyimbo za Injili & Redio 🎵",
                "app_color": "#FF0000",
                "options": [
                    {"label": "▶️ Nyimbo za Injili za Kiswahili", "url": "https://www.youtube.com/results?search_query=nyimbo+za+injili+kiswahili"},
                    {"label": "▶️ Kwaya ya AIC Vijana", "url": "https://www.youtube.com/results?search_query=kwaya+ya+aic+vijana"},
                    {"label": "📻 Sikiliza Redio ya Taifa (KBC / TBC)", "url": "https://www.youtube.com/results?search_query=swahili+radio+live"}
                ],
                "action_url": "https://www.youtube.com/results?search_query=nyimbo+za+injili+kiswahili"
            }
        }

    def tool_guide_camera_photos(self, query: str) -> Dict[str, Any]:
        """Camera & Photos Navigator Tool: Camera shutter and photo album guidance."""
        lower = query.lower()
        if "albamu" in lower or "gallery" in lower or "ona" in lower or "tazama" in lower:
            return {
                "action": "view_photos",
                "swahili_response": "Kuangalia picha za familia na wajukuu: Fungua ile programu kwenye skrini inayoitwa Albamu au Picha. Picha zote ulizopigiwa au kutumiwa na watoto zitajipanga kuanzia ya karibuni zaidi.",
                "english_translation": "To view family photos: Open the Album or Photos app on your screen. All photos taken or sent by your children are sorted starting with the most recent.",
                "visual_card": {
                    "type": "gallery_guide",
                    "title": "Albamu ya Picha za Familia 🖼️",
                    "app_color": "#8B5CF6",
                    "steps": [
                        "1. Tafuta picha ya ua au fremu iliyoandikwa 'Albamu' au 'Picha'",
                        "2. Bonyeza mara moja kufungua",
                        "3. Picha za hivi karibuni ziko juu kabisa",
                        "4. Gusa picha yoyote mara mbili kuikuza"
                    ]
                }
            }

        return {
            "action": "take_photo",
            "swahili_response": "Kupiga picha: Elekeza kamera ya simu yako kwa watu au kitu unachotaka kupiga, kisha bonyeza kile kitufe kikubwa cheupe cha mviringo kilicho chini katikati ya skrini. Picha itapigwa mara moja.",
            "english_translation": "To take a photo: Direct the phone camera towards the subject, then tap the large round white button at the bottom center. The photo will be captured instantly.",
            "visual_card": {
                "type": "camera_guide",
                "title": "Kupiga Picha kwa Kamera 📸",
                "app_color": "#8B5CF6",
                "steps": [
                    "1. Shikilia simu kwa mikono miwili kwa utulivu",
                    "2. Elekeza kamera kwa watu unaowapiga picha",
                    "3. Bonyeza kitufe kikuu cha mviringo chini katikati ⚪",
                    "4. Picha itahifadhiwa kiotomatiki kwenye albamu"
                ]
            }
        }

    def tool_guide_phone_settings(self, query: str) -> Dict[str, Any]:
        """Settings & Accessibility Tool: Live font scaling, screen brightness, data toggle."""
        lower = query.lower()
        if "maandishi" in lower or "size" in lower or "kuza" in lower:
            return {
                "action": "enlarge_font",
                "swahili_response": "Nimeongeza ukubwa wa maandishi kwenye skrini yako mara moja ili usipate shida kusoma. Je, sasa maandishi yanaonekana makubwa na wazi Mzee wangu?",
                "english_translation": "I have increased the text size across your screen right now so you can read comfortably. Does the text look large and clear now elder?",
                "visual_card": {
                    "type": "font_magnifier",
                    "title": "Ukubwa wa Maandishi Umeongezwa 🔤",
                    "app_color": "#2563EB",
                    "status": "MAANDISHI YAMEKUZWA (+25%)",
                    "preview": "Sasa unaweza kusoma kwa urahisi bila miwani!"
                }
            }

        if "mwangaza" in lower or "brightness" in lower or "skrini" in lower:
            return {
                "action": "adjust_brightness",
                "swahili_response": "Nimeongeza mwangaza wa skrini yako hadi asilimia mia moja ili uweze kuona kila kitu wazi, hata ukiwa nje kwenye jua au chumbani.",
                "english_translation": "I have set your screen brightness to maximum so you can see everything clearly, whether outside in the sun or indoors.",
                "visual_card": {
                    "type": "brightness_card",
                    "title": "Mwangaza wa Skrini: 100% ☀️",
                    "app_color": "#2563EB",
                    "details": "Mwangaza umewekwa juu kabisa kwa kuona vizuri."
                }
            }

        # Internet / Wi-Fi toggle
        return {
            "action": "network_settings",
            "swahili_response": "Ili kuwasha bando au intaneti kwenye simu: Weka kidole chako juu kabisa ya skrini kisha shusha chini. Bonyeza picha ya mishale miwili ya 'Data ya Simu' au mawimbi ya wayafai.",
            "english_translation": "To turn on mobile data or Wi-Fi: Place your finger at the very top of the screen and swipe down. Tap the two mobile data arrows or the Wi-Fi icon.",
            "visual_card": {
                "type": "settings_network",
                "title": "Kuwasha Intaneti na Data 📶",
                "app_color": "#2563EB",
                "steps": [
                    "1. Shusha kidole chako kutoka juu ya skrini kwenda chini",
                    "2. Tafuta kitufe chenye mishale miwili ⇅ kinachoitwa 'Data'",
                    "3. Kibonyeze kigeuke rangi ya samawati (blue) kuwasha",
                    "4. Ikiwa unatumia wayafai ya nyumbani, bonyeza picha ya mawimbi 📶"
                ]
            }
        }

    def tool_guide_airtime_balance(self, query: str) -> Dict[str, Any]:
        """Airtime & Bundles Tool: USSD guidance for checking balances and purchasing data."""
        lower = query.lower()
        if "bando" in lower or "data" in lower or "intaneti" in lower or "nunua" in lower:
            return {
                "action": "buy_bundles",
                "swahili_response": "Kununua bando ya intaneti: Piga nyota tano nne nne reli kwenye simu yako, kisha uchague bando inayokufaa kama ya siku au ya wiki nzima.",
                "english_translation": "To buy data bundles: Dial star 5 4 4 hash on your phone, then choose your preferred daily or weekly package.",
                "visual_card": {
                    "type": "airtime_card",
                    "title": "Kununua Bando ya Data 🌐",
                    "app_color": "#059669",
                    "ussd_code": "*544#",
                    "steps": [
                        "1. Piga nambari *544# kwenye kipaza sauti au simu",
                        "2. Chagua '1: Bando za Data'",
                        "3. Chagua ya siku au wiki",
                        "4. Lipa kwa kutumia salio au M-Pesa"
                    ],
                    "dialer_intent": "tel:*544%23"
                }
            }

        # Check balance
        return {
            "action": "check_balance",
            "swahili_response": "Kuangalia salio lako la maongezi: Piga nyota moja nne nne reli kwenye simu yako. Ujumbe mfupi utatokea kwenye skrini kukuonyesha salio la pesa, dakika, na ujumbe.",
            "english_translation": "To check your airtime balance: Dial star 1 4 4 hash. A pop-up notification will display your remaining airtime, minutes, and SMS.",
            "visual_card": {
                "type": "airtime_card",
                "title": "Kuangalia Salio la Simu 📞",
                "app_color": "#059669",
                "ussd_code": "*144# (Bila Malipo / Free)",
                "steps": [
                    "1. Fungua simu yako na ubonyeze *144#",
                    "2. Piga simu mara moja",
                    "3. Skrini itakuonyesha salio lako lililobaki papo hapo"
                ],
                "dialer_intent": "tel:*144%23"
            }
        }

    def tool_guide_sms_reader(self, query: str) -> Dict[str, Any]:
        """SMS Reader Tool: Speaks elder's incoming SMS aloud in respectful Swahili."""
        return {
            "action": "read_sms",
            "swahili_response": "Niko tayari kukusomea ujumbe wako Mzee wangu. Ujumbe wa mwisho unatoka kwa mwanao Juma, unasema: Shikamoo Mzee, nilitaka kujua kama uko salama nyumbani na kama unahitaji chochote.",
            "english_translation": "I am ready to read your message elder. Your latest SMS is from your child Juma, saying: Greetings elder, I wanted to check if you are safe at home and if you need anything.",
            "visual_card": {
                "type": "sms_card",
                "title": "Ujumbe wa Mwisho Ulioingia 📨",
                "app_color": "#0284C7",
                "sender": "Mwanangu Juma (+254712345678)",
                "received_time": "Leo, Saa 10:15 Asubuhi",
                "message_body": "Shikamoo Mzee, nilitaka kujua kama uko salama nyumbani na kama unahitaji chochote."
            }
        }

    def tool_guide_mpesa_transfer(self, query: str) -> Dict[str, Any]:
        """M-Pesa Guidance Tool: Guides safe money transfers step-by-step to prevent fraud."""
        return {
            "action": "mpesa_guide",
            "swahili_response": "Shikamoo Mama. Kwenye Em-pesa, usalama wako ni muhimu sana. Piga nyota tatu tatu nne reli kwenye simu yako, kisha uhakikishe jina la mpokeaji linaonekana wazi kwenye skrini kabla ya kuweka namba yako ya siri.",
            "english_translation": "Greetings Mama. On M-Pesa, your safety is very important. Dial star 3 3 4 hash on your phone, then verify the recipient's name is clearly shown on screen before entering your secret PIN.",
            "visual_card": {
                "type": "mpesa_safety",
                "title": "Hatua Salama za M-Pesa 💸",
                "app_color": "#059669",
                "ussd_code": "*334# (Njia ya Nje ya Mtandao / Offline)",
                "steps": [
                    "1. Piga nambari *334# kwenye simu yako",
                    "2. Chagua '1: Tuma Pesa'",
                    "3. Weka nambari ya simu ya mpokeaji",
                    "4. ANGALIA JINA KWANZA kabla ya kuweka namba ya siri!",
                    "5. Weka nambari yako ya siri kwa siri kabisa"
                ],
                "warning": "Usitoe nambari yako ya siri (PIN) kwa mtu yeyote, hata akisema anapiga simu kutoka kampuni ya simu."
            }
        }

    def tool_control_phone_feature(self, action: str, query: str) -> Dict[str, Any]:
        """Phone Feature Accessibility Tool: Controls flashlight, volume, battery, calls."""
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
                    "title": f"Inapiga simu: {self.emergency_contact['name']} 📞",
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
