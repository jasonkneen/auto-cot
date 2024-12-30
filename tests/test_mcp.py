import unittest
import requests

class TestMCPFunctionality(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/v1"
        
    def test_mcp_tools_listing(self):
        response = requests.get(f"{self.base_url}/models")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("data", response_data)
        self.assertEqual(response_data['data'][0]['id'], "lmstudio")

if __name__ == '__main__':
    unittest.main()