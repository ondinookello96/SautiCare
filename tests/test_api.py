"""
API Integration Tests for SautiCare
Tests HTTP endpoints, health check, and text processing.
"""

import unittest
from fastapi.testclient import TestClient
from main import app

class TestSautiCareAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "SautiCare Swahili Voice Agent")
        self.assertTrue(data["offline_support"])

    def test_emergency_simulation(self):
        response = self.client.post("/api/emergency/sos")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_emergency"])
        self.assertIn("Tulia", data["swahili_response"])
        self.assertIn("DHARURA", data["visual_card"]["status"])

    def test_process_text_endpoint(self):
        response = self.client.post("/api/process-text", json={"text": "Nataka kutuma pesa kwa mtoto"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["action"], "mpesa_guide")
        self.assertIn("tts", data)

    def test_index_page_serves_html(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("SautiCare", response.text)
        self.assertIn("BONYEZA KUONGEA", response.text)

if __name__ == "__main__":
    unittest.main()
