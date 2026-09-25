"""
Unit Tests for SautiCare Agent Engine
Verifies Swahili intent classification, emergency SOS dispatch, M-Pesa tool rules, and phone controls.
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

    def test_mpesa_transfer_guidance(self):
        """Test that M-Pesa requests trigger safety verification guidelines."""
        queries = [
            "Nataka kutuma pesa kwa mtoto wangu",
            "Nisaidie na miamala ya M-Pesa",
            "Kuangalia salio la M-Pesa",
            "Tuma shilingi mia tano"
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

if __name__ == "__main__":
    unittest.main()
