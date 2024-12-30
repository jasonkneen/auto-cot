# Auto-CoT: Automatic Chain of Thought Prompting in Large Language Models (ICLR 2023)

[![Open Auto-CoT in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amazon-science/auto-cot/blob/main/try_cot_colab.ipynb)

Cheer AI up with the "let's think step by step" prompt? More plz. *Let’s think not just step by step, but also one by one.*

Auto-CoT uses more cheers & diversity to SAVE huge manual efforts in chain of thought prompt design, matching or even exceeding performance of manual design on GPT-3.

Check out our [25-page paper](https://arxiv.org/pdf/2210.03493.pdf) for more information.

![](https://user-images.githubusercontent.com/22279212/194787183-a1f8dff8-a0ad-43a1-827f-819671503860.png)

![](https://user-images.githubusercontent.com/22279212/194787130-d28c9191-588c-41d2-a259-62377f19c934.png)

## Requirements

Python>=3.8
```
pip install torch==1.8.2+cu111 torchtext==0.9.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
pip install -r requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-repo/auto-cot.git
cd auto-cot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install MCP with CLI extras using uv:
```bash
uv add 'mcp[cli]'
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Usage

The server.py script can be used in four different ways:

### 1. Chat Interface
Run an interactive chat session:
```bash
python server.py --chat
```

### 2. Importable Module
Use as a Python module:
```python
from server import CoTServer

server = CoTServer()
result = server.process_question("auto_cot", "your question")
print(result)
```

### 3. HTTP Server
Run as a web server:
```bash
python server.py --server
```
The server will be available at http://localhost:5000

#### API Endpoints
- POST /api/cot
  Request body:
  ```json
  {
    "question": "your question",
    "method": "auto_cot"  # optional, default is auto_cot
  }
  ```
  Response:
  ```json
  {
    "question": "your question",
    "response": "model response",
    "method": "auto_cot"
  }
  ```

### 4. MCP Server
Run as a Model Context Protocol server:
```bash
python server.py --mcp
```
The MCP server exposes a `process_question` tool that can be used via the MCP Python SDK.

## Configuration

You can configure the server using command-line arguments:
```bash
python server.py --chat --model gpt-4 --temperature 0.7
```

Available options:
- --model: Model to use (default: gpt-4o-mini)
- --method: CoT method (default: auto_cot)
- --temperature: Sampling temperature (default: 0)
- --max_length_cot: Max tokens for CoT (default: 256)
- --max_length_direct: Max tokens for direct answer (default: 32)

## Datasets

Download the datasets from the following:
```
https://github.com/kojima-takeshi188/zero_shot_cot/tree/main/dataset
https://github.com/kojima-takeshi188/zero_shot_cot/tree/main/log
```

## Citing Auto-CoT
```
@inproceedings{zhang2023automatic,
  title={Automatic Chain of Thought Prompting in Large Language Models},
  author={Zhang, Zhuosheng and Zhang, Aston and Li, Mu and Smola, Alex},
  booktitle={The Eleventh International Conference on Learning Representations (ICLR 2023)},
  year={2023}
}
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
