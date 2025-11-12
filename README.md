# shopee-ai-solutions-engineer-case-study
Shopee - AI Solutions Engineer Case Study


# Setup Environment
1. Download Dataset and put into `data/` folder.
    ```bash
    data
    ├── customers-100000.csv
    └── customers-2000000.csv
    ```

2. Initialize python env using `uv`
    ```bash
    uv init
    ```

3. Install dependencies
    ```bash
    uv pip install -r pyproject.toml
    ```

4. Activate environment
    ```bash
    source .venv/bin/activate
    ```


# Run the test
```bash
pytest tests/ -v
python -m pytest tests/test_openai_embedder.py -v
```

# Run the app
```bash
streamlit run app.py
```

# Docker Build & Run
```bash
docker build -t shopee-ai-solutions-engineer-case-study .
docker run -p 8501:8501 shopee-ai-solutions-engineer-case-study
```