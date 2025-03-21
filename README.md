# Technical Writing Checker

A Python tool that analyzes technical writing for compliance with standard technical writing rules using LangChain and OpenAI's GPT-4.

## Features

- Checks for technical writing rule violations
- Provides suggestions for improvements
- Supports both synchronous and asynchronous processing
- Includes detailed error explanations
- Formats output in a readable format

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SahityaBhaskar/Safran.git
cd Safran
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI credentials:

```
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=your-base-url-here
```

## Project Structure

```
technical-writing-checker/
├── src/                # Source code
│   ├── checker/        # Core checker functionality
│   └── utils/          # Utility functions
├── tests/              # Test cases
├── examples/           # Usage examples
└── README.md           # Documentation
```

## Usage

You can use the tool in two different ways:

**1. Through CLI:**
```bash
python3 cli.py "Your text here"
```

**2. In Python code:**
```python
from src.checker.technical_writing_checker import TechnicalWritingChecker

checker = TechnicalWritingChecker()
analysis = checker.check_text("Your text here")
print(checker.format_analysis(analysis))
```

See `examples/usage_example.py` for more detailed examples.

## Running Tests

```bash
pytest tests/
```

## Rules Checked

1. **Article Usage**: Use articles (*the*, *a*, *an*) or demonstrative adjectives.
2. **Active Voice**: Use active voice in procedural writing.
3. **Single Instructions**: One instruction per sentence.
4. **Imperative Form**: Write instructions in command form.
5. **Sentence Length**: Maximum 20 words per sentence.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Create a Pull Request.