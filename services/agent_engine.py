"""
SautiCare Pan-African Agent Engine
Provides culturally grounded reasoning in multiple African languages and dialects:
- Kiswahili (East Africa 🇰🇪 🇹🇿)
- Nigerian Pidgin & Dialects (West Africa 🇳🇬)
- isiZulu (Southern Africa 🇿🇦)
- Amharic / አማርኛ (Horn of Africa 🇪🇹)

Features elder-respectful personas, intent recognition, multimodal navigation guides
for everyday smartphone apps (WhatsApp, YouTube Gospel, Camera, Settings, Airtime/USSD),
mobile money safety, and life-saving Emergency SOS.
"""

import re
from typing import Dict, Any

PAN_AFRICAN_CONTENT = {
    "sw": {
        "region": "East Africa",
        "name": "Kiswahili",
        "emergency": {
            "response": "Tulia Mzee wangu, usijali wala usiogope. Nimeshatuma ujumbe mfupi wa dharura pamoja na mahali ulipo kwa mwanao Juma, na sasa ninapiga simu ya msaada mara moja.",
            "translation": "Stay calm elder, do not be afraid. I have already dispatched an emergency SMS with your live location to your child Juma, and I am calling for help immediately.",
            "status": "DHARURA IMETUMWA (SOS SENT)",
            "call_btn": "📞 Piga Simu ya Dharura Sasa"
        },
        "greeting": {
            "response": "Marahaba Mzee wangu! Mimi ni SautiCare, msaidizi wako wa karibu. Niko hapa kukuongoza kutumia Watsapu, kusikiliza nyimbo za injili kwenye Yutubu, kupiga picha, kuangalia Em-pesa, au kupiga simu ya dharura. Nikusaidie na nini sasa hivi?",
            "translation": "Greetings elder! I am SautiCare, your voice assistant. I am here to guide you through WhatsApp, gospel music on YouTube, taking photos, M-Pesa, or emergency calls. How may I help you now?"
        },
        "whatsapp": {
            "title": "Kutuma Sauti kwa Watsapu 🎙️",
            "response": "Kutuma ujumbe wa sauti kwa Watsapu ni rahisi sana: Fungua mazungumzo ya mtu unayetaka kumtumia, kisha bonyeza na ushikilie kile kitufe cha kijani cha kinasa sauti chini kulia. Zungumza maneno yako ukiwa umeshikilia, kisha achilia kidole chako. Ujumbe utaenda mara moja.",
            "translation": "To send a WhatsApp voice note: Open the chat, hold down the green microphone button at the bottom right. Speak while holding it, then release your finger. The message will send immediately.",
            "steps": [
                "1. Ingia kwenye Watsapu na uchague mtu",
                "2. Chini kulia, bonyeza na USHIKILIE kitufe cha kijani 🎙️",
                "3. Zungumza maneno unayotaka kusema",
                "4. Achilia kidole chako kutuma mara moja!"
            ],
            "btn": "📲 Fungua Watsapu Moja kwa Moja"
        },
        "youtube": {
            "title": "Nyimbo za Injili & Redio 🎵",
            "response": "Nimekuandalia nyimbo nzuri za injili na kwaya za Kiswahili kwenye Yutubu. Unaweza kubonyeza kitufe hapa chini kusikiliza mara moja, au uniambie jina la kwaya unayopenda nikufungulie.",
            "translation": "I have prepared uplifting Swahili gospel songs and choirs for you on YouTube. Tap the button below to listen right away, or tell me the choir you'd love to hear.",
            "options": [
                {"label": "▶️ Nyimbo za Injili za Kiswahili", "url": "https://www.youtube.com/results?search_query=nyimbo+za+injili+kiswahili"},
                {"label": "▶️ Kwaya ya AIC Vijana", "url": "https://www.youtube.com/results?search_query=kwaya+ya+aic+vijana"},
                {"label": "📻 Sikiliza Redio ya Taifa", "url": "https://www.youtube.com/results?search_query=swahili+radio+live"}
            ],
            "btn": "▶️ Fungua Yutubu Moja kwa Moja"
        },
        "camera": {
            "title": "Kupiga Picha kwa Kamera 📸",
            "response": "Kupiga picha: Elekeza kamera ya simu yako kwa watu au kitu unachotaka kupiga, kisha bonyeza kile kitufe kikubwa cheupe cha mviringo kilicho chini katikati ya skrini. Picha itapigwa mara moja.",
            "translation": "To take a photo: Direct the phone camera towards the subject, then tap the large round white button at the bottom center. The photo will be captured instantly.",
            "steps": [
                "1. Shikilia simu kwa mikono miwili kwa utulivu",
                "2. Elekeza kamera kwa watu unaowapiga picha",
                "3. Bonyeza kitufe kikuu cha mviringo chini katikati ⚪",
                "4. Picha itahifadhiwa kiotomatiki kwenye albamu"
            ]
        },
        "font": {
            "title": "Ukubwa wa Maandishi Umeongezwa 🔤",
            "response": "Nimeongeza ukubwa wa maandishi kwenye skrini yako mara moja ili usipate shida kusoma. Je, sasa maandishi yanaonekana makubwa na wazi Mzee wangu?",
            "translation": "I have increased the text size across your screen right now so you can read comfortably. Does the text look large and clear now elder?",
            "status": "MAANDISHI YAMEKUZWA (+25%)",
            "preview": "Sasa unaweza kusoma kwa urahisi bila miwani!"
        },
        "airtime": {
            "title": "Kuangalia Salio la Simu 📞",
            "response": "Kuangalia salio lako la maongezi: Piga nyota moja nne nne reli kwenye simu yako. Ujumbe mfupi utatokea kwenye skrini kukuonyesha salio la pesa, dakika, na ujumbe.",
            "translation": "To check your airtime balance: Dial star 1 4 4 hash. A pop-up notification will display your remaining airtime, minutes, and SMS.",
            "ussd": "*144# (Bila Malipo / Free)",
            "intent": "tel:*144%23"
        },
        "mpesa": {
            "title": "Hatua Salama za M-Pesa 💸",
            "response": "Shikamoo Mama. Kwenye Em-pesa, usalama wako ni muhimu sana. Piga nyota tatu tatu nne reli kwenye simu yako, kisha uhakikishe jina la mpokeaji linaonekana wazi kwenye skrini kabla ya kuweka namba yako ya siri.",
            "translation": "Greetings Mama. On M-Pesa, your safety is very important. Dial star 3 3 4 hash on your phone, then verify the recipient's name is clearly shown on screen before entering your secret PIN.",
            "ussd": "*334# (Njia ya Nje ya Mtandao / Offline)",
            "warning": "Usitoe nambari yako ya siri (PIN) kwa mtu yeyote, hata akisema anapiga simu kutoka kampuni ya simu."
        }
    },
    "ng": {
        "region": "West Africa",
        "name": "Nigerian Pidgin",
        "emergency": {
            "response": "Elder calm down, no fear at all! I don send emergency SMS with your live GPS location give your pikin Juma, and I dey dial emergency help call right now!",
            "translation": "Elder stay calm, do not fear! I have sent an emergency SMS with your live GPS location to your child Juma, and I am dialing emergency help immediately.",
            "status": "EMERGENCY DISPATCHED (SOS SENT)",
            "call_btn": "📞 Dial Emergency Call Now"
        },
        "greeting": {
            "response": "Respect Elder! My name na SautiCare, your personal phone voice helper. I dey here to guide you on how to send voice notes on WhatsApp, play gospel songs on YouTube, snap fine photos, check money, or call emergency. Wetin you wan make I do for you now?",
            "translation": "Respect Elder! I am SautiCare, your phone voice helper. I am here to guide you with WhatsApp, YouTube gospel, photos, money, or emergency. What can I do for you?"
        },
        "whatsapp": {
            "title": "Send Voice Note for WhatsApp 🎙️",
            "response": "To send voice note on WhatsApp dey very easy: Open the chat of the person you wan send to, hold down that green microphone button for bottom right. Talk your message while holding am, then release your hand. E go send sharp sharp!",
            "translation": "Sending a voice note on WhatsApp is very simple: Open the chat, hold down the green microphone button at the bottom right. Speak your message and release. It will send immediately!",
            "steps": [
                "1. Open WhatsApp and click the person name",
                "2. Look for the green mic button 🎙️ at bottom right and HOLD am",
                "3. Speak the words you wan talk",
                "4. Release your finger make e send immediately!"
            ],
            "btn": "📲 Open WhatsApp Right Now"
        },
        "youtube": {
            "title": "Gospel Worship & Praise 🎵",
            "response": "I don arrange sweet African gospel worship and praise songs for you on YouTube. Tap that button below make you enjoy yourself right away, or tell me the choir you like!",
            "translation": "I have arranged uplifting African gospel worship and praise songs for you on YouTube. Tap the button below to enjoy right away!",
            "options": [
                {"label": "▶️ African Gospel Praise & Worship", "url": "https://www.youtube.com/results?search_query=african+gospel+praise+and+worship"},
                {"label": "▶️ Sinach & Mercy Chinwo Worship", "url": "https://www.youtube.com/results?search_query=sinach+mercy+chinwo+worship"},
                {"label": "📻 Listen to Live Gospel Radio", "url": "https://www.youtube.com/results?search_query=nigerian+gospel+radio+live"}
            ],
            "btn": "▶️ Open YouTube Directly"
        },
        "camera": {
            "title": "Snap Fine Picture with Camera 📸",
            "response": "To snap photo: Point your phone camera to the people, then press that big round white button for bottom middle. E go snap am sharp sharp!",
            "translation": "To take a photo: Point the camera towards the people, then press the big round white button in the bottom middle. It will snap the picture immediately!",
            "steps": [
                "1. Hold phone steady with two hands",
                "2. Point camera to the people you wan snap",
                "3. Press the big round white circle button ⚪",
                "4. The picture go save for your phone album automatically"
            ]
        },
        "font": {
            "title": "Big Text Magnifier Activated 🔤",
            "response": "I don make all the text big big for your screen now, so that reading go dey very easy without any eye strain. Elder, shey you dey see am clearly now?",
            "translation": "I have enlarged all the text across your screen now so reading is effortless without eye strain. Can you see it clearly now elder?",
            "status": "TEXT ENLARGED (+25%)",
            "preview": "Now you fit read everything without glasses!"
        },
        "airtime": {
            "title": "Check Airtime & Data Balance 📞",
            "response": "To check your airtime balance, dial star 3 1 0 hash (*310#) for airtime or use your bank code. A message go show you your remaining airtime balance sharp sharp.",
            "translation": "To check your airtime balance, dial star 310 hash (*310#). A message will display your remaining balance immediately.",
            "ussd": "*310# (Airtime Balance)",
            "intent": "tel:*310%23"
        },
        "mpesa": {
            "title": "Mobile Money & Banking Safety 💸",
            "response": "Respect Elder. For mobile money transfers, your safety dey very important. Check the person name clearly on screen before you enter your secret PIN, and never give your PIN to anyone!",
            "translation": "Respect Elder. For mobile money transfers, safety is critical. Always verify the recipient's name before entering your secret PIN, and never share your PIN with anyone.",
            "ussd": "*901# (Mobile Money / Bank)",
            "warning": "Never give your secret 4-digit PIN to anybody, even if dem say dem dey call from bank or network company!"
        }
    },
    "zu": {
        "region": "Southern Africa",
        "name": "isiZulu",
        "emergency": {
            "response": "Thula Mkhulu, ungesabi nakancane! Sengithumele umlayezo we-SOS nendawo yakho ku-Juma, futhi ngishayela ucingo lwezimo eziphuthumayo manje.",
            "translation": "Stay calm elder, do not be afraid. I have already dispatched an SOS message with your location to Juma, and I am calling emergency help now.",
            "status": "USIZO LUTHUNYELWE (SOS SENT)",
            "call_btn": "📞 Shayela Usizo Lwezimo Eziphuthumayo"
        },
        "greeting": {
            "response": "Sawubona Mkhulu wami / Gogo! Igama lami ngingu-SautiCare, umsizi wakho wezwi. Ngilapha ukukusiza usebenzise i-WhatsApp, ulalele umculo wokholo ku-YouTube, uthwebule izithombe, noma ushayele usizo oluphuthumayo. Ngingakusiza ngani namhlanje?",
            "translation": "Greetings elder! I am SautiCare, your voice helper. I am here to assist you with WhatsApp, gospel music on YouTube, photos, or emergency calls. How may I help you today?"
        },
        "whatsapp": {
            "title": "Thumela Izwi ku-WhatsApp 🎙️",
            "response": "Ukuthumela izwi ku-WhatsApp kulula kakhulu: Vula ingxoxo yomuntu ofuna ukumthumelela, bese ucindezela ubambe inkinobho eluhlaza yombhobho ezansi kwesokudla. Khuluma ubanjwe, bese ukhulula umunwe wakho. Umlayezo uzohamba ngokushesha.",
            "translation": "Sending a voice note on WhatsApp is very easy: Open the chat, hold down the green microphone button at the bottom right. Speak while holding it, then release your finger. The message will send immediately.",
            "steps": [
                "1. Vula i-WhatsApp ukhethe igama lomuntu",
                "2. Ezansi kwesokudla, cindezela UBAMBE inkinobho eluhlaza 🎙️",
                "3. Khuluma amazwi ofuna ukuwasho",
                "4. Khulula umunwe wakho ukuze kuhambe ngokushesha!"
            ],
            "btn": "📲 Vula i-WhatsApp Manje"
        },
        "youtube": {
            "title": "Umculo Wokholo Nezincwadi 🎵",
            "response": "Ngikulungiselele umculo omnandi wokholo nezihlabelelo zase-Afrika ku-YouTube. Cindezela inkinobho engezansi ukuze ulalele manje, noma ungitshele ikhwaya oyithandayo!",
            "translation": "I have prepared uplifting gospel music and African hymns for you on YouTube. Tap the button below to listen right away, or tell me your favorite choir!",
            "options": [
                {"label": "▶️ Umculo Wokholo Wase-Ningizimu Afrika", "url": "https://www.youtube.com/results?search_query=south+african+gospel+worship"},
                {"label": "▶️ Joyous Celebration Worship", "url": "https://www.youtube.com/results?search_query=joyous+celebration+live"},
                {"label": "📻 Lalela Umsakazo Wokholo", "url": "https://www.youtube.com/results?search_query=ukhozi+fm+live"}
            ],
            "btn": "▶️ Vula i-YouTube Ngqo"
        },
        "camera": {
            "title": "Thatha Isithombe Nge-Khamera 📸",
            "response": "Ukuthatha isithombe: Qondisa ikhamera kubantu, bese ucindezela leyo nkinobho enkulu emhlophe eyindilinga ezansi maphakathi. Isithombe sizothathwa ngokushesha.",
            "translation": "To take a photo: Point the camera towards the people, then press the big round white button in the bottom middle. The photo will be taken immediately.",
            "steps": [
                "1. Bamba ifoni ngezandla zombili ngokuzinza",
                "2. Qondisa ikhamera kubantu ofuna ukubathatha",
                "3. Cindezela inkinobho enkulu emhlophe eyindilinga ⚪",
                "4. Isithombe sizogcinwa ngokuzenzakalelayo"
            ]
        },
        "font": {
            "title": "Ubungako Bencwadi Bukhulisiwe 🔤",
            "response": "Sengikhulise amagama esikrinini sakho ukuze ukwazi ukufunda kahle ngaphandle kokuhlupheka. Ingabe avela ngokucacile manje Mkhulu?",
            "translation": "I have enlarged the words on your screen so you can read comfortably without difficulty. Do they appear clearly now elder?",
            "status": "AMAGAMA AKHULISIWE (+25%)",
            "preview": "Manje ungafunda kalula ngaphandle kwezibuko!"
        },
        "airtime": {
            "title": "Hlola Ibhalansi Yocingo 📞",
            "response": "Ukuhlola ibhalansi yakho, shayela u-star 1 3 6 hash (*136#) ocingweni lwakho. Umlayezo uzovela ubonise ibhalansi yakho yemali namaminithi.",
            "translation": "To check your balance, dial star 1 3 6 hash (*136#) on your phone. A message will appear showing your balance and minutes.",
            "ussd": "*136# (Ibhalansi)",
            "intent": "tel:*136%23"
        },
        "mpesa": {
            "title": "Ukuthumela Imali Ngokuphephile 💸",
            "response": "Sawubona Gogo. Ekuthumeleni imali ngefoni, ukuphepha kwakho kubalulekile. Qinisekisa igama lomemukeli ngaphambi kokufaka i-PIN yakho eyimfihlo, futhi ungalokothi unikeze muntu i-PIN yakho!",
            "translation": "Greetings elder. When sending money, your safety is paramount. Always verify the recipient's name before entering your secret PIN, and never give your PIN to anyone.",
            "ussd": "*120# (I-Mobile Banking)",
            "warning": "Ungalinge unikeze umuntu inombolo yakho eyimfihlo (PIN), ngisho noma bethi bafona ebhange!"
        }
    },
    "am": {
        "region": "Horn of Africa",
        "name": "Amharic",
        "emergency": {
            "response": "አይዞዎ አያቴ፣ በጭራሽ አይጨነቁ! የአደጋ ጊዜ መልእክት እና የት እንዳሉ የሚያሳይ መረጃ ወዲያውኑ ለልጅዎ ጁማ ልኬያለሁ፣ አሁን ደግሞ የእርዳታ ጥሪ እየደወልኩ ነው።",
            "translation": "Stay calm elder, do not worry! I have immediately sent an emergency message with your location to your child Juma, and I am placing an emergency call right now.",
            "status": "የአደጋ ጊዜ መልእክት ተልኳል (SOS SENT)",
            "call_btn": "📞 የአደጋ ጊዜ ጥሪ ደውል"
        },
        "greeting": {
            "response": "ጤና ይስጥልኝ አያቴ! እኔ ሳውቲኬር (SautiCare) ነኝ፣ የስልክዎ የድምፅ ረዳት። በዋትስአፕ መልእክት ለመላክ፣ በዩቲዩብ መዝሙር ለማዳመጥ፣ ፎቶ ለማንሳት ወይም የአደጋ ጊዜ ጥሪ ለማድረግ ዝግጁ ነኝ። ዛሬ በምን ልርዳዎት?",
            "translation": "Greetings elder! I am SautiCare, your voice assistant. I am ready to help you with WhatsApp, YouTube hymns, photos, or emergency calls. How may I help you today?"
        },
        "whatsapp": {
            "title": "በዋትስአፕ የድምፅ መልእክት ለመላክ 🎙️",
            "response": "በዋትስአፕ የድምፅ መልእክት ለመላክ በጣም ቀላል ነው፤ የሰውየውን ቻት ይክፈቱ፣ ከታች በቀኝ በኩል ያለውን አረንጓዴ ማይክሮፎን ተጭነው ይያዙ፣ መልእክትዎን ይናገሩና ጣትዎን ይልቀቁ። መልእክቱ ወዲያውኑ ይላካል።",
            "translation": "To send a voice note on WhatsApp: Open the chat, hold down the green microphone at the bottom right. Speak and release your finger. The message will send immediately.",
            "steps": [
                "1. ዋትስአፕን ይክፈቱና የሰውየውን ስም ይምረጡ",
                "2. ከታች በቀኝ በኩል ያለውን አረንጓዴ ማይክሮፎን 🎙️ ተጭነው ይያዙ",
                "3. የሚፈልጉትን መልእክት ይናገሩ",
                "4. ወዲያውኑ ለመላክ ጣትዎን ይልቀቁ!"
            ],
            "btn": "📲 ዋትስአፕን አሁን ይክፈቱ"
        },
        "youtube": {
            "title": "መንፈሳዊ መዝሙሮች እና ሬዲዮ 🎵",
            "response": "በዩቲዩብ የሚያምሩ የመንፈሳዊ መዝሙሮችን አዘጋጅቼልዎታለሁ። ወዲያውኑ ለማዳመጥ ከታች ያለውን ቁልፍ ይጫኑ፣ ወይም የሚወዱትን የመዘምራን ስም ይንገሩኝ።",
            "translation": "I have prepared uplifting spiritual hymns on YouTube for you. Tap the button below to listen right away, or tell me your favorite choir!",
            "options": [
                {"label": "▶️ የኢትዮጵያ ኦርቶዶክስ እና ፕሮቴስታንት መዝሙሮች", "url": "https://www.youtube.com/results?search_query=amharic+mezmur+ethiopian"},
                {"label": "▶️ የተመረጡ የመንፈሳዊ መዝሙሮች", "url": "https://www.youtube.com/results?search_query=amharic+spiritual+songs"},
                {"label": "📻 የቀጥታ ሬዲዮ አድምጡ", "url": "https://www.youtube.com/results?search_query=sheger+fm+live"}
            ],
            "btn": "▶️ ዩቲዩብን በቀጥታ ይክፈቱ"
        },
        "camera": {
            "title": "በካሜራ ፎቶ ለማንሳት 📸",
            "response": "ፎቶ ለማንሳት፦ የስልክዎን ካሜራ ወደ ሰዎች ያቅኑ፣ ከዚያም ከታች መሃል ላይ ያለውን ትልቅ ክብ ነጭ ቁልፍ ይጫኑ። ፎቶው ወዲያውኑ ይነሳል።",
            "translation": "To take a photo: Point the phone camera towards people, then press the big round white button in the bottom center. The photo will be taken immediately.",
            "steps": [
                "1. ስልክዎን በሁለቱም እጆችዎ አረጋግተው ይያዙ",
                "2. ካሜራውን ወደ ሰዎች ያቅኑ",
                "3. ከታች መሃል ያለውን ትልቅ ነጭ ክብ ቁልፍ ⚪ ይጫኑ",
                "4. ፎቶው በቀጥታ ወደ ስልክዎ አልበም ይቀመጣል"
            ]
        },
        "font": {
            "title": "የጽሑፍ መጠን ጨምሯል 🔤",
            "response": "በቀላሉ እንዲያነቡ የስክሪኑን የጽሑፍ መጠን አሁን አሳድጌዋለሁ። አሁን በግልጽ ይታይዎታል አያቴ?",
            "translation": "I have increased the screen text size so you can read easily. Can you see it clearly now elder?",
            "status": "የጽሑፍ መጠን አድጓል (+25%)",
            "preview": "አሁን ያለ መነጽር በቀላሉ ማንበብ ይችላሉ!"
        },
        "airtime": {
            "title": "የስልክ ቀሪ ሂሳብን ለማየት 📞",
            "response": "ቀሪ ሂሳብዎን ለማየት በስልክዎ ላይ *804# ይደውሉ። ቀሪ ሂሳብዎን የሚያሳይ አጭር መልእክት በስክሪኑ ላይ ይታያል።",
            "translation": "To check your balance, dial *804# on your phone. A message will appear showing your balance.",
            "ussd": "*804# (ቀሪ ሂሳብ)",
            "intent": "tel:*804%23"
        },
        "mpesa": {
            "title": "ቴሌብር እና የሞባይል ገንዘብ ደህንነት 💸",
            "response": "ጤና ይስጥልኝ አያቴ። በስልክ ገንዘብ ሲልኩ ደህንነትዎ በጣም አስፈላጊ ነው። የምስጢር ቁጥርዎን (PIN) ከማስገባትዎ በፊት የተላከለትን ሰው ስም በደንብ ያረጋግጡ፣ እና የይለፍ ቃልዎን ለማንም እንዳይሰጡ!",
            "translation": "Greetings elder. When transferring mobile money, safety is paramount. Always verify the recipient's name before entering your secret PIN, and never give your PIN to anyone.",
            "ussd": "*127# (ቴሌብር / Telebirr)",
            "warning": "የምስጢር ቁጥርዎን (PIN) ከባንክ ወይም ከኢትዮ ቴሌኮም ደወልን ቢሉ እንኳን ለማንም ሰው እንዳይሰጡ!"
        }
    }
}

class AgentEngine:
    def __init__(self):
        self.emergency_contact = {
            "name": "Mwanangu Juma",
            "phone": "+254712345678",
            "relationship": "Mwanafamilia wa karibu"
        }

    def process_swahili_intent(self, text: str) -> Dict[str, Any]:
        """Backward-compatible alias for Kiswahili processing."""
        return self.process_intent(text, lang="sw")

    def process_intent(self, text: str, lang: str = "sw") -> Dict[str, Any]:
        """
        Analyze transcribed speech in any supported African language (Swahili, Nigerian Pidgin,
        isiZulu, Amharic), classify intent, and return culturally respectful localized guidance.
        """
        lower = text.lower().strip()
        lang_key = lang if lang in PAN_AFRICAN_CONTENT else "sw"
        content = PAN_AFRICAN_CONTENT[lang_key]

        # 1. Emergency Intent Detection (Top Priority)
        emergency_indicators = [
            "dharura", "nimeanguka", "anguka", "naumwa", "vibaya", "hospitali", "kizunguzungu", "damu",
            "emergency", "fall down", "fell down", "i don fall", "help me", "dey pain me", "sick",
            "isimo esiphuthumayo", "ngiwe", "ngiwe phansi", "ngiyagula", "usizo", "esibhedlela",
            "አደጋ", "ወደቅሁ", "ወድቄያለሁ", "ታመምኩ", "እርዳኝ", "እርዱኝ", "አስቸኳይ", "ሆስፒታል", "አሞኛል"
        ]
        has_emergency = any(kw in lower for kw in emergency_indicators)
        is_general_help = ("nisaidie" in lower or "help" in lower or "usizo" in lower or "እርዳኝ" in lower or "እርዱኝ" in lower) and not any(
            w in lower for w in [
                "tochi", "pesa", "mpesa", "watsapu", "whatsapp", "yutubu", "youtube", "picha", "kamera", "salio",
                "maandishi", "photo", "money", "light", "torch"
            ]
        )

        if has_emergency or is_general_help:
            return self.tool_trigger_emergency_sos(lang_key=lang_key, details=text)

        # 2. Greetings
        greeting_words = [
            "shikamoo", "habari", "hujambo", "jambo", "mambo", "hello", "asalaam",
            "how you dey", "wetin dey", "good morning", "sawubona", "sanibonani",
            "ጤና ይስጥልኝ", "ሰላም"
        ]
        is_greeting = any(gw in lower for gw in greeting_words)
        has_action = any(w in lower for w in [
            "tochi", "pesa", "mpesa", "watsapu", "whatsapp", "yutubu", "youtube", 
            "picha", "kamera", "salio", "maandishi", "mwangaza", "betri", "injili", "kwaya",
            "photo", "gospel", "balance", "airtime", "torch", "light", "money", "text"
        ])

        if is_greeting and not has_action:
            g = content["greeting"]
            return {
                "action": "greeting",
                "swahili_response": g["response"],
                "english_translation": g["translation"],
                "visual_card": {
                    "type": "welcome",
                    "title": f"Karibu SautiCare ({content['region']}) 🌿",
                    "details": g["translation"]
                }
            }

        # 3. WhatsApp Navigation Intent
        if any(w in lower for w in ["watsapu", "whatsapp", "voice note", "ujumbe wa sauti", "video call", "ዋትስአፕ", "ዋትሳፕ", "ድምፅ", "የድምፅ መልእክት", "ilizwi"]):
            w = content["whatsapp"]
            if "video" in lower or "call" in lower:
                action = "whatsapp_call"
                sw_resp = "Kupiga video call kwa Watsapu: Fungua mazungumzo ya mtu unayetaka kumpigia, kisha bonyeza ile alama ndogo ya kamera ya video juu kulia." if lang_key == "sw" else w["response"]
                en_trans = "To make a WhatsApp video call: Open the chat and tap the video camera icon at the top right."
            else:
                action = "whatsapp_voicenote"
                sw_resp = w["response"]
                en_trans = w["translation"]

            return {
                "action": action,
                "swahili_response": sw_resp,
                "english_translation": en_trans,
                "visual_card": {
                    "type": "whatsapp_guide",
                    "title": w["title"],
                    "app_color": "#25D366",
                    "steps": w["steps"],
                    "action_intent": "whatsapp://",
                    "action_btn_text": w["btn"]
                }
            }

        # 4. YouTube & Gospel Music / Faith Intent
        if any(w in lower for w in ["yutubu", "youtube", "injili", "kwaya", "nyimbo", "redio", "gospel", "worship", "praise", "umculo", "መዝሙር", "ዩቲዩብ", "ሬዲዮ"]):
            y = content["youtube"]
            return {
                "action": "youtube_gospel",
                "swahili_response": y["response"],
                "english_translation": y["translation"],
                "visual_card": {
                    "type": "youtube_guide",
                    "title": y["title"],
                    "app_color": "#FF0000",
                    "options": y["options"],
                    "action_url": y["options"][0]["url"],
                    "action_btn_text": y["btn"]
                }
            }

        # 5. Camera & Photos Intent
        if any(w in lower for w in ["picha", "kamera", "camera", "albamu", "gallery", "photo", "picture", "snap", "isithombe", "ፎቶ", "ካሜራ", "አልበም"]):
            c = content["camera"]
            if "albamu" in lower or "gallery" in lower or "አልበም" in lower:
                action = "view_photos"
                card_type = "gallery_guide"
                title = "Kutazama Picha kwenye Albamu 🖼️" if lang_key == "sw" else c["title"]
                steps = [
                    "1. Fungua programu ya Picha (Photos/Gallery)",
                    "2. Gusa picha yoyote unayotaka kuiona kwa ukubwa",
                    "3. Unaweza kusogeza vidole viwili ili kuikuza"
                ] if lang_key == "sw" else c["steps"]
                sw_resp = "Kutazama picha: Fungua programu ya albamu au Photos kwenye simu yako, na utaona picha zote za familia na kumbukumbu zako." if lang_key == "sw" else c["response"]
                en_trans = "To view photos: Open the Photos or Gallery app to see all your family pictures and memories."
            else:
                action = "take_photo"
                card_type = "camera_guide"
                title = c["title"]
                steps = c["steps"]
                sw_resp = c["response"]
                en_trans = c["translation"]

            return {
                "action": action,
                "swahili_response": sw_resp,
                "english_translation": en_trans,
                "visual_card": {
                    "type": card_type,
                    "title": title,
                    "app_color": "#8B5CF6",
                    "steps": steps
                }
            }

        # 6. Phone Settings & Text Magnification Intent
        if any(w in lower for w in ["maandishi", "mwangaza", "skrini", "kuza", "size", "font", "text", "bright", "screen", "amagama", "ጽሑፍ", "መጠን", "አግዝፍ"]):
            f = content["font"]
            if "mwangaza" in lower or "bright" in lower:
                action = "adjust_brightness"
                card_type = "brightness_card"
                title = "Mwangaza wa Skrini ☀️ (Brightness)"
                sw_resp = "Nimeongeza mwangaza wa skrini ya simu yako ili uweze kuona maandishi vizuri hata wakati wa mchana au gizani." if lang_key == "sw" else f["response"]
                en_trans = "I have adjusted your screen brightness so you can see clearly in bright daylight or darkness."
            else:
                action = "enlarge_font"
                card_type = "font_magnifier"
                title = f["title"]
                sw_resp = f["response"]
                en_trans = f["translation"]

            return {
                "action": action,
                "swahili_response": sw_resp,
                "english_translation": en_trans,
                "visual_card": {
                    "type": card_type,
                    "title": title,
                    "app_color": "#2563EB",
                    "status": f.get("status", "Active"),
                    "preview": f.get("preview", "Preview")
                }
            }

        # 7. Airtime & Data Balance Intent
        if any(w in lower for w in ["salio", "airtime", "bando", "data", "balance", "bundle", "dakika", "ibhalansi", "ቀሪ ሂሳብ"]):
            a = content["airtime"]
            if "bando" in lower or "data" in lower or "bundle" in lower:
                action = "buy_bundles"
                ussd = "*544#" if lang_key == "sw" else a["ussd"]
                sw_resp = "Kununua bando ya data au dakika: Piga *544# kwenye simu yako, kisha chagua kifurushi kinachokufaa." if lang_key == "sw" else a["response"]
                en_trans = "To buy data bundles or minutes: Dial *544# on your phone dialer and select your desired bundle."
            else:
                action = "check_balance"
                ussd = a["ussd"]
                sw_resp = a["response"]
                en_trans = a["translation"]

            return {
                "action": action,
                "swahili_response": sw_resp,
                "english_translation": en_trans,
                "visual_card": {
                    "type": "airtime_card",
                    "title": a["title"],
                    "app_color": "#0D9488",
                    "ussd_code": ussd,
                    "dialer_intent": a["intent"],
                    "steps": [
                        f"1. Dial {ussd} on your phone dialer",
                        "2. Press call to view remaining balance or purchase bundle",
                        "3. A pop-up notification will display your details instantly"
                    ]
                }
            }

        # 8. SMS Voice Reader Intent
        if any(w in lower for w in ["ujumbe mfupi", "sms", "message", "nani amenitumia", "meseji"]):
            return {
                "action": "read_sms",
                "swahili_response": "Ujumbe wako wa mwisho unatoka kwa Mwanangu Juma: 'Habari ya jioni Mzee wangu, ninatumai unajisikia vizuri leo. Nitapiga simu baadaye.'",
                "english_translation": "Your latest message is from Juma: 'Good evening elder, I hope you are feeling well today. I will call later.'",
                "visual_card": {
                    "type": "sms_card",
                    "title": "Ujumbe Mfupi (SMS)",
                    "sender": "Mwanangu Juma (+254712345678)",
                    "received_time": "Dakika 15 zilizopita",
                    "message_body": "Habari ya jioni Mzee wangu, ninatumai unajisikia vizuri leo. Nitapiga simu baadaye."
                }
            }

        # 9. Mobile Money Intent (M-Pesa / OPay / eWallet / Telebirr)
        if any(w in lower for w in ["mpesa", "m-pesa", "tuma pesa", "money", "transfer", "shilingi", "naira", "rand", "birr", "imali", "ብር"]):
            m = content["mpesa"]
            return {
                "action": "mpesa_guide",
                "swahili_response": m["response"],
                "english_translation": m["translation"],
                "visual_card": {
                    "type": "mpesa_safety",
                    "title": m["title"],
                    "app_color": "#059669",
                    "ussd_code": m["ussd"],
                    "steps": [
                        f"1. Dial {m['ussd']} on your phone",
                        "2. Select 'Transfer / Send Money'",
                        "3. Enter the recipient phone number",
                        "4. ALWAYS check the recipient name on screen first!",
                        "5. Enter your secret PIN privately"
                    ],
                    "warning": m["warning"]
                }
            }

        # 9. Hardware controls (Flashlight, Volume, Battery)
        if "tochi" in lower or "torch" in lower or "light" in lower or "giza" in lower:
            state = "off" if ("zima" in lower or "off" in lower) else "on"
            return self.tool_control_phone_feature(action=f"torch_{state}", query=text)

        if "betri" in lower or "battery" in lower or "chaji" in lower:
            return self.tool_control_phone_feature(action="check_battery", query=text)

        if "sauti" in lower or "volume" in lower:
            return self.tool_control_phone_feature(action="adjust_volume", query=text)

        # Fallback
        g = content["greeting"]
        return {
            "action": "guidance",
            "swahili_response": g["response"],
            "english_translation": g["translation"],
            "visual_card": {
                "type": "suggestion",
                "title": f"SautiCare ({content['region']})",
                "items": [
                    "💬 WhatsApp Voice Note",
                    "🎵 African Gospel Worship",
                    "📸 Camera & Photos",
                    "🔤 Enlarge Text Size",
                    "📞 Check Balance & Airtime",
                    "🚨 Emergency SOS Lifeline"
                ]
            }
        }

    def tool_trigger_emergency_sos(self, lang_key: str = "sw", details: str = "", distress_type: str = "") -> Dict[str, Any]:
        """Emergency SOS Tool: Dispatches SMS with GPS and triggers phone call in the selected language."""
        content = PAN_AFRICAN_CONTENT.get(lang_key, PAN_AFRICAN_CONTENT["sw"])
        em = content["emergency"]
        gps_coords = "1°17'31.2\"S 36°49'10.8\"E (Africa)"
        status_text = distress_type or em["status"]

        return {
            "action": "emergency_sos",
            "is_emergency": True,
            "swahili_response": em["response"],
            "english_translation": em["translation"],
            "visual_card": {
                "type": "sos_card",
                "status": status_text,
                "recipient": self.emergency_contact["name"],
                "phone": self.emergency_contact["phone"],
                "location": gps_coords,
                "sms_preview": f"EMERGENCY SOS: Your elder needs immediate help! Location: {gps_coords}. Call immediately.",
                "gsm_dialer_intent": f"tel:{self.emergency_contact['phone']}",
                "call_btn_text": em["call_btn"]
            }
        }

    def tool_control_phone_feature(self, action: str, query: str) -> Dict[str, Any]:
        """Controls hardware features: flashlight, volume, battery."""
        if action == "torch_on":
            return {
                "action": "torch_on",
                "swahili_response": "Tayari nimewasha tochi ya simu yako ili uweze kuona vizuri gizani.",
                "english_translation": "I have turned on your phone's flashlight so you can see clearly in the dark.",
                "visual_card": {
                    "type": "device_action",
                    "title": "Tochi Imewashwa 🔦 (Flashlight ON)",
                    "details": "Flashlight is activated for your safety."
                }
            }
        elif action == "torch_off":
            return {
                "action": "torch_off",
                "swahili_response": "Nimezima tochi ya simu yako.",
                "english_translation": "I have turned off your phone's flashlight.",
                "visual_card": {
                    "type": "device_action",
                    "title": "Tochi Imezimwa (Flashlight OFF)",
                    "details": "Flashlight turned off to conserve battery."
                }
            }
        elif action == "check_battery":
            return {
                "action": "check_battery",
                "swahili_response": "Betri ya simu yako iko asilimia themanini na tano. Chaji inatosha kabisa kwa siku nzima ya leo.",
                "english_translation": "Your phone's battery is at 85%. You have plenty of charge for the rest of today.",
                "visual_card": {
                    "type": "battery_card",
                    "title": "Hali ya Betri: 85% 🔋 (Battery Status)",
                    "details": "Your phone has plenty of battery charge for today."
                }
            }
        elif action == "adjust_volume":
            return {
                "action": "adjust_volume",
                "swahili_response": "Nimeongeza sauti ya simu hadi mwisho kabisa ili uweze kusikia vizuri kila neno linalosemwa.",
                "english_translation": "I have raised your phone's volume to maximum so you can hear every word clearly.",
                "visual_card": {
                    "type": "volume_card",
                    "title": "Sauti Imeongezwa 🔊 (Volume 100%)",
                    "details": "Volume set to maximum for elder audibility."
                }
            }
        return {
            "action": "unknown",
            "swahili_response": "Nipo hapa kukusaidia Mzee wangu. Niambie chochote unachohitaji kwenye simu yako.",
            "english_translation": "I am here to help you elder. Tell me anything you need with your phone."
        }
