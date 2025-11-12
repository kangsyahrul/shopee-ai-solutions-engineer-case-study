# Shopee - AI Solutions Engineer Case Study

Engineering Knowledge AI Agent Test: [Docs](docs/knowledge_test.md)

Coding Test: 
- Number 1-3: `notebooks/task_1.ipynb`
- No. 4: [URL](http://shopee-streamlit-app-alb-1045798762.ap-southeast-3.elb.amazonaws.com/custom_vectordb)
- No. 5: [URL](http://shopee-streamlit-app-alb-1045798762.ap-southeast-3.elb.amazonaws.com/)


# Setup Environment
1. Download Dataset and put into `data/` folder.
    ```bash
    data
    ├── customers-100000.csv
    └── customers-2000000.csv
    ```

2. **Initialize Python environment** using `uv`:
   ```bash
   uv init
   uv pip install -r pyproject.toml
   source .venv/bin/activate
   ```

3. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Testing

Run the test suite:
```bash
pytest tests/ -v
python -m pytest tests/test_openai_embedder.py -v
```

## Docker

### Local Docker
```bash
# Build and run locally
docker build -t shopee-ai-solutions-engineer-case-study .
docker run -p 8501:8501 shopee-ai-solutions-engineer-case-study

# Or use Docker Compose to run Streamlit and Qdrant
docker compose up -d
```

### Local Qdrant
```bash
./qdrant.sh
```