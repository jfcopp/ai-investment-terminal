# AI Investment Terminal

Mobile/PWA investment terminal with live market data, historical valuation, market breadth and financial news.

## Deploy on Render

1. Connect this GitHub repository to Render as a Blueprint/Web Service.
2. Add `FMP_API_KEY` as a secret environment variable in Render.
3. Deploy. Render will use `render.yaml` and start the Python server automatically.

## Local run

```bash
pip install -r requirements.txt
export FMP_API_KEY=YOUR_KEY
python server.py
```

Then open `http://127.0.0.1:8000`.

## Security

Never commit `.env` or an API key. `.gitignore` excludes `.env`; use `.env.example` only as a template.
