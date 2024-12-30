import argparse
import requests
from flask import Flask, request, jsonify
import sys
from utils import *
from datetime import datetime
import uuid

app = Flask(__name__)

class CoTServer:
    def __init__(self):
        self.args = parse_arguments()
        self.decoder = Decoder()

    def process_question(self, method, question):
        try:
            # Construct the prompt with reasoning
            prompt = f"Q: {question}\nA: Let's think step by step."
            
            # First API call for reasoning
            reasoning_response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "model": "lmstudio",
                    "temperature": 0.7,
                    "max_tokens": 256,
                    "stop": ["\n\n"],
                    "presence_penalty": 0.6,
                    "frequency_penalty": 0.6
                }
            )
            
            if reasoning_response.status_code != 200:
                return {
                    "question": question,
                    "response": f"Reasoning API Error: {reasoning_response.status_code} - {reasoning_response.text}",
                    "method": method
                }
            
            reasoning = reasoning_response.json()['choices'][0]['message']['content']
            
            # Construct final answer prompt
            final_prompt = f"{prompt}\n{reasoning}\nTherefore, the final answer is:"
            
            # Second API call for final answer
            final_response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": final_prompt}],
                    "model": "lmstudio",
                    "temperature": 0.7,
                    "max_tokens": 32,
                    "stop": ["\n\n"],
                    "presence_penalty": 0.6,
                    "frequency_penalty": 0.6
                }
            )
            
            if final_response.status_code == 200:
                final_answer = final_response.json()['choices'][0]['message']['content']
                return {
                    "question": question,
                    "response": f"{reasoning}\n\nFinal Answer: {final_answer}",
                    "method": method
                }
            else:
                return {
                    "question": question,
                    "response": f"Final Answer API Error: {final_response.status_code} - {final_response.text}",
                    "method": method
                }
        except Exception as e:
            return {
                "question": question,
                "response": f"Connection Error: {str(e)}",
                "method": method
            }

def parse_arguments():
    parser = argparse.ArgumentParser(description="Zero-shot-CoT Server")
    
    # Mode selection
    parser.add_argument("--chat", action="store_true", help="run in chat interface mode")
    parser.add_argument("--server", action="store_true", help="run as HTTP server")
    parser.add_argument("--mcp", action="store_true", help="run as MCP server")
    
    # Model parameters
    parser.add_argument("--model", type=str, default="lmstudio", help="model used for decoding")
    parser.add_argument("--method", type=str, default="auto_cot", 
                       choices=["zero_shot", "zero_shot_cot", "few_shot", "few_shot_cot", "auto_cot"], 
                       help="method")
    parser.add_argument("--max_length_cot", type=int, default=256, 
                       help="maximum length of output tokens by model for reasoning extraction")
    parser.add_argument("--max_length_direct", type=int, default=32, 
                       help="maximum length of output tokens by model for answer extraction")
    parser.add_argument("--temperature", type=float, default=0, help="temperature for GPT-3")
    parser.add_argument("--log_dir", type=str, default="./log/", help="log directory")
    parser.add_argument("--api_time_interval", type=float, default=1.0, 
                       help="time interval between API calls")
    parser.add_argument("--demo_path", type=str, default="demos/multiarith", 
                       help="path to demonstration files")
    
    args = parser.parse_args()
    
    # Set default triggers
    args.direct_answer_trigger_for_zeroshot = "The answer is"
    args.direct_answer_trigger_for_zeroshot_cot = "The answer is"
    args.direct_answer_trigger_for_fewshot = "The answer is"
    args.cot_trigger = "Let's think step by step."
    
    return args

# OpenAI-compatible API Endpoints
@app.route('/v1/models', methods=['GET'])
def list_models():
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "lmstudio",
                "object": "model",
                "created": 1677649963,
                "owned_by": "auto-cot"
            }
        ]
    })

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    messages = data.get('messages', [])
    question = messages[-1]['content'] if messages else ""
    
    server = CoTServer()
    result = server.process_question("auto_cot", question)
    
    return jsonify({
        "id": str(uuid.uuid4()),
        "object": "chat.completion",
        "created": int(datetime.now().timestamp()),
        "model": "lmstudio",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": result['response']
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(question),
            "completion_tokens": len(result['response']),
            "total_tokens": len(question) + len(result['response'])
        }
    })

@app.route('/v1/embeddings', methods=['POST'])
def create_embeddings():
    data = request.json
    input_text = data.get('input', "")
    
    # For now, return a dummy embedding
    embedding = [0.0] * 1536  # OpenAI's standard embedding size
    
    return jsonify({
        "object": "list",
        "data": [{
            "object": "embedding",
            "index": 0,
            "embedding": embedding
        }],
        "model": "text-embedding-ada-002",
        "usage": {
            "prompt_tokens": len(input_text),
            "total_tokens": len(input_text)
        }
    })

# Original API Endpoint
@app.route('/api/cot', methods=['POST'])
def cot_endpoint():
    data = request.json
    server = CoTServer()
    result = server.process_question(data.get('method', 'auto_cot'), data['question'])
    return jsonify(result)

def chat_interface():
    server = CoTServer()
    print("Welcome to the Zero-shot-CoT chat interface!")
    print("Type 'exit' to quit the chat.")
    while True:
        question = input("\nYou: ")
        if question.lower() == "exit":
            break
        print("\nModel:")
        result = server.process_question("zero_shot_cot", question)
        print(result['response'])

def main():
    args = parse_arguments()
    
    if args.chat:
        chat_interface()
    elif args.server:
        app.run(host='0.0.0.0', port=8000, debug=True)  # Enable debug mode for auto-reload
    elif args.mcp:
        try:
            from mcp import McpServer
            
            class CoTMcpServer(McpServer):
                def __init__(self):
                    super().__init__()
                    self.cot_server = CoTServer()
                    
                def get_tools(self):
                    return {
                        'process_question': {
                            'description': 'Process a question using Chain-of-Thought reasoning',
                            'input_schema': {
                                'type': 'object',
                                'properties': {
                                    'question': {'type': 'string'},
                                    'method': {'type': 'string', 'enum': ['zero_shot', 'zero_shot_cot', 'few_shot', 'few_shot_cot', 'auto_cot']}
                                },
                                'required': ['question']
                            }
                        }
                    }
                    
                def process_question(self, args):
                    return self.cot_server.process_question(args.get('method', 'auto_cot'), args['question'])
            
            mcp_server = CoTMcpServer()
            mcp_server.run()
        except ImportError:
            print("Error: mcp package not found. Please install it with:")
            print("uv add 'mcp[cli]'")
            sys.exit(1)
    else:
        # Default to importable mode
        return CoTServer()

if __name__ == "__main__":
    main()