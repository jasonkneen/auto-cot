import unittest
import requests

class TestChatInterface(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/v1"
        
    def test_chat_response(self):
        messages = [
            {"role": "user", "content": "What is 2 + 2?"}
        ]
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={
                "messages": messages,
                "model": "lmstudio"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("choices", response_data)
        self.assertIn("4", response_data['choices'][0]['message']['content'])

if __name__ == '__main__':
    unittest.main()