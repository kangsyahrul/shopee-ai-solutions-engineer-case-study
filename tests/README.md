# Tests

To run all tests:
```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

To run specific test file:
```bash
source .venv/bin/activate
python -m pytest tests/test_openai_embedder.py -v
```

To run tests with coverage:
```bash
source .venv/bin/activate
python -m pytest tests/ --cov=scripts --cov-report=html
```
