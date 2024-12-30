import unittest
import requests

class TestReasoning(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/v1"
        
    def test_reasoning_response(self):
        question = "If I have 3 apples and eat 1, how many do I have left?"
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={
                "messages": [{"role": "user", "content": question}],
                "model": "lmstudio"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("choices", response_data)
        # Check for reasoning patterns rather than exact phrase
        content = response_data['choices'][0]['message']['content'].lower()
        self.assertTrue(
            any(phrase in content for phrase in [
                "let's think", "let's break", "let's analyze",
                "step by step", "step-by-step", "steps",
                "reasoning", "reason", "rationale",
                "therefore", "thus", "hence",
                "because", "since", "as a result",
                "first", "second", "finally",
                "conclusion", "summary", "in summary"
            ]),
            f"Expected reasoning pattern not found in: {content}"
        )

if __name__ == '__main__':
    unittest.main()