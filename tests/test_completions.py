import unittest
import requests

class TestCompletionsEndpoint(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/v1"
        
    def test_completions_response(self):
        prompt = "What is the capital of France?"
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={
                "messages": [{"role": "user", "content": prompt}],
                "model": "lmstudio"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("choices", response_data)
        self.assertIn("Paris", response_data['choices'][0]['message']['content'])

if __name__ == '__main__':
    unittest.main()