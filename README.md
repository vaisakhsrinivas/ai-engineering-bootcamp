# ai-engineering-bootcamp
##### This repo contains all the learnings from Maven AI Engineering bootcamp #####

## API

FastAPI app with:

- **GET /health** – Health check (status and timestamp)
- **POST /summarize** – Summarize text; body: `text`, `max_length`, `prompt_type` (optional: `zero_shot`, `few_shot`, `chain_of_thought`, `meta`)
- **POST /analyze-sentiment** – Sentiment analysis; body: `text`, `prompt_type` (optional). Returns `sentiment`, `confidence_score`, `explanation`

### Run locally

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
uvicorn main:app --reload
```

Docs: http://127.0.0.1:8000/docs

### Deploy on Render

1. Push this repo to GitHub and connect it to [Render](https://render.com).
2. Create a new **Web Service**; Render can auto-detect from `render.yaml` or set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. In the service **Environment** tab, add:
   - **OPENAI_API_KEY** (Secret) – your OpenAI API key
4. Deploy. The API will be available at the service URL (e.g. `https://ai-bootcamp-api.onrender.com`).

See [Render: Deploy a FastAPI app](https://docs.render.com/deploy-fastapi) for more details.
