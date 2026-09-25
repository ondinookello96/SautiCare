"""
Unit Tests for SautiCare Agent Engine
Verifies Swahili intent classification, emergency SOS dispatch, M-Pesa tool rules,
and universal smartphone features (WhatsApp, YouTube Gospel, Camera, Settings, Airtime).
"""

import unittest
from services.agent_engine import AgentEngine

class TestSautiCareAgent(unittest.TestCase):
    def setUp(self):
        self.engine = AgentEngine()

    def test_emergency_detection(self):
        """Test that distress and emergency phrases in Swahili trigger emergency SOS."""
        queries = [
            "Nisaidie nimeanguka chini",
            "Nahitaji msaada wa dharura hospitali",
            "Najisikia vibaya sana siwezi kupumua",
            "Emergency help me"
        ]
        for q in queries:
            result = self.engine.process_swahili_intent(q)
            self.assertTrue(result.get("is_emergency"), f"Failed on: {q}")
            self.assertEqual(result["action"], "emergency_sos")
            self.assertIn("sos_card", result["visual_card"]["type"])
            self.assertIn("DHARURA", result["visual_card"]["status"])

    def test_whatsapp_guidance(self):
        """Test WhatsApp voice note and video call guidance."""
        vn_result = self.engine.process_swahili_intent("Nataka kutuma ujumbe wa sauti kwa Watsapu")
        self.assertEqual(vn_result["action"], "whatsapp_voicenote")
        self.assertIn("kinasa sauti", vn_result["swahili_response"])
        self.assertEqual(vn_result["visual_card"]["type"], "whatsapp_guide")

        call_result = self.engine.process_swahili_intent("Piga video call kwa Watsapu")
        self.assertEqual(call_result["action"], "whatsapp_call")
        self.assertIn("kamera", call_result["swahili_response"])

    def test_youtube_gospel(self):
        """Test YouTube gospel and Swahili choir access."""
        queries = [
            "Fungua nyimbo za injili kwenye Yutubu",
            "Nataka kusikiliza kwaya ya Kiswahili",
            "Washa redio ya taifa"
        ]
        for q in queries:
            result = self.engine.process_swahili_intent(q)
            self.assertEqual(result["action"], "youtube_gospel", f"Failed on: {q}")
            self.assertEqual(result["visual_card"]["type"], "youtube_guide")
            self.assertIn("youtube.com", result["visual_card"]["action_url"])

    def test_camera_and_photos(self):
        """Test camera shutter and photo album guidance."""
        cam_result = self.engine.process_swahili_intent("Nataka kupiga picha ya wajukuu")
        self.assertEqual(cam_result["action"], "take_photo")
        self.assertEqual(cam_result["visual_card"]["type"], "camera_guide")

        gal_result = self.engine.process_swahili_intent("Nionyeshe picha nilizopiga kwenye albamu")
        self.assertEqual(gal_result["action"], "view_photos")
        self.assertEqual(gal_result["visual_card"]["type"], "gallery_guide")

    def test_phone_settings_and_font(self):
        """Test accessibility font scaling and screen brightness."""
        font_result = self.engine.process_swahili_intent("Maandishi ni madogo sana ongeza ukubwa")
        self.assertEqual(font_result["action"], "enlarge_font")
        self.assertEqual(font_result["visual_card"]["type"], "font_magnifier")

        bright_result = self.engine.process_swahili_intent("Ongeza mwangaza wa skrini kuko giza")
        self.assertEqual(bright_result["action"], "adjust_brightness")
        self.assertEqual(bright_result["visual_card"]["type"], "brightness_card")

    def test_airtime_balance(self):
        """Test USSD airtime balance and data bundles guidance."""
        bal_result = self.engine.process_swahili_intent("Salio langu la simu limebaki ngapi?")
        self.assertEqual(bal_result["action"], "check_balance")
        self.assertIn("*144#", bal_result["visual_card"]["ussd_code"])

        bundle_result = self.engine.process_swahili_intent("Nataka kununua bando ya data")
        self.assertEqual(bundle_result["action"], "buy_bundles")
        self.assertIn("*544#", bundle_result["visual_card"]["ussd_code"])

    def test_sms_reader(self):
        """Test SMS voice reading."""
        result = self.engine.process_swahili_intent("Nani amenitumia ujumbe mfupi?")
        self.assertEqual(result["action"], "read_sms")
        self.assertEqual(result["visual_card"]["type"], "sms_card")

    def test_mpesa_transfer_guidance(self):
        """Test that M-Pesa requests trigger safety verification guidelines."""
        queries = [
            "Nataka kutuma pesa kwa mtoto wangu",
            "Nisaidie na miamala ya M-Pesa",
            "Tuma shilingi mia tano kwa M-Pesa"
        ]
        for q in queries:
            result = self.engine.process_swahili_intent(q)
            self.assertEqual(result["action"], "mpesa_guide", f"Failed on: {q}")
            self.assertIn("mpesa_safety", result["visual_card"]["type"])
            self.assertIn("*334#", result["visual_card"]["ussd_code"])

    def test_torch_control(self):
        """Test flashlight controls in Swahili."""
        on_result = self.engine.process_swahili_intent("Washa tochi kuko giza")
        self.assertEqual(on_result["action"], "torch_on")

        off_result = self.engine.process_swahili_intent("Zima tochi sasa")
        self.assertEqual(off_result["action"], "torch_off")

    def test_battery_check(self):
        """Test battery status query."""
        result = self.engine.process_swahili_intent("Betri ya simu ikoje?")
        self.assertEqual(result["action"], "check_battery")

    def test_cultural_greeting(self):
        """Test culturally respectful greeting response."""
        result = self.engine.process_swahili_intent("Shikamoo SautiCare")
        self.assertEqual(result["action"], "greeting")
        self.assertIn("Marahaba", result["swahili_response"])

    def test_pan_african_multilingual(self):
        """Test intent classification and response localization across 4 African regions."""
        # 1. Nigerian Pidgin (West Africa)
        ng_sos = self.engine.process_intent("Help me abeg I don fall down", lang="ng")
        self.assertTrue(ng_sos.get("is_emergency"))
        self.assertIn("SOS SENT", ng_sos["visual_card"]["status"])

        ng_greet = self.engine.process_intent("How you dey SautiCare", lang="ng")
        self.assertEqual(ng_greet["action"], "greeting")
        self.assertIn("Respect Elder", ng_greet["swahili_response"])

        ng_wa = self.engine.process_intent("I wan send voice note for WhatsApp", lang="ng")
        self.assertEqual(ng_wa["action"], "whatsapp_voicenote")
        self.assertIn("microphone", ng_wa["swahili_response"])

        # 2. isiZulu (Southern Africa)
        zu_sos = self.engine.process_intent("Ngifuna usizo ngiwe phansi", lang="zu")
        self.assertTrue(zu_sos.get("is_emergency"))
        self.assertIn("USIZO LUTHUNYELWE", zu_sos["visual_card"]["status"])

        zu_greet = self.engine.process_intent("Sawubona SautiCare", lang="zu")
        self.assertEqual(zu_greet["action"], "greeting")
        self.assertIn("Sawubona", zu_greet["swahili_response"])

        zu_wa = self.engine.process_intent("Ngifuna ukuthumela umyalezo wezwi ku-WhatsApp", lang="zu")
        self.assertEqual(zu_wa["action"], "whatsapp_voicenote")
        self.assertIn("inkinobho", zu_wa["swahili_response"])

        # 3. Amharic (Horn of Africa)
        am_sos = self.engine.process_intent("ወድቄያለሁ እባክዎን በአስቸኳይ እርዱኝ", lang="am")
        self.assertTrue(am_sos.get("is_emergency"))
        self.assertIn("የአደጋ ጊዜ", am_sos["visual_card"]["status"])

        am_greet = self.engine.process_intent("ጤና ይስጥልኝ ሳውቲኬር", lang="am")
        self.assertEqual(am_greet["action"], "greeting")
        self.assertIn("ጤና ይስጥልኝ", am_greet["swahili_response"])

        am_wa = self.engine.process_intent("በዋትስአፕ የድምፅ መልእክት መላክ እፈልጋለሁ", lang="am")
        self.assertEqual(am_wa["action"], "whatsapp_voicenote")
        self.assertIn("የድምፅ መልእክት", am_wa["swahili_response"])

if __name__ == "__main__":
    unittest.main()
