import unittest
import json
from app import app, security_alerts, plc_state

class TestSOCApi(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_status(self):
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('speed', data)
        self.assertIn('temperature', data)

    def test_get_alerts(self):
        response = self.client.get('/api/alerts')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_post_report_valid(self):
        payload = {
            "message": "Unauthorized ARP spoofing detected on OT network",
            "severity": "HIGH",
            "source": "Snort-OT-Sensor"
        }
        response = self.client.post('/api/report', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['alert']['message'], payload['message'])
        self.assertEqual(data['alert']['severity'], 'HIGH')

    def test_post_report_invalid(self):
        response = self.client.post('/api/report', json={})
        self.assertEqual(response.status_code, 400)

    def test_update_plc(self):
        payload = {
            "status": "RUN",
            "speed": 1800,
            "temperature": 52.0
        }
        response = self.client.post('/api/update_plc', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['state']['speed'], 1800)

    def test_plc_auto_alert_on_stop(self):
        payload = {"status": "STOP"}
        response = self.client.post('/api/update_plc', json=payload)
        self.assertEqual(response.status_code, 200)
        alerts_res = self.client.get('/api/alerts')
        alerts = alerts_res.get_json()
        self.assertTrue(any("CRITICAL: PLC Status changed to STOP!" in a['message'] for a in alerts))

if __name__ == '__main__':
    unittest.main()
