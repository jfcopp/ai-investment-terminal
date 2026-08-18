import os
from flask import Flask, jsonify, send_from_directory, request
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='.', static_url_path='')
FMP_API_KEY = os.getenv('FMP_API_KEY', '')
FMP_BASE = 'https://financialmodelingprep.com/stable'


def fmp(path, params=None):
    if not FMP_API_KEY:
        raise RuntimeError('FMP_API_KEY is not configured')
    p = dict(params or {})
    p['apikey'] = FMP_API_KEY
    r = requests.get(f'{FMP_BASE}/{path}', params=p, timeout=20)
    r.raise_for_status()
    return r.json()


@app.get('/')
def home():
    return send_from_directory('.', 'index.html')


@app.get('/health')
def health():
    return jsonify({'ok': True, 'market_data_configured': bool(FMP_API_KEY)})


@app.get('/api/quote/<symbol>')
def quote(symbol):
    try:
        data = fmp('quote', {'symbol': symbol.upper()})
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 502


@app.get('/api/markets')
def markets():
    symbols = request.args.get('symbols', 'AAPL,MSFT,NVDA,SPY,QQQ').split(',')
    out = []
    for symbol in symbols[:12]:
        symbol = symbol.strip().upper()
        if not symbol:
            continue
        try:
            d = fmp('quote', {'symbol': symbol})
            if isinstance(d, list) and d:
                out.append(d[0])
        except Exception:
            pass
    return jsonify(out)


@app.get('/api/news')
def news():
    symbols = request.args.get('symbols', 'AAPL,MSFT,NVDA')
    try:
        data = fmp('news/stock-latest', {'symbols': symbols, 'limit': 30})
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 502


@app.get('/api/pe/<symbol>')
def pe_history(symbol):
    try:
        data = fmp('ratios', {'symbol': symbol.upper(), 'period': 'annual', 'limit': 15})
        rows = []
        for x in data if isinstance(data, list) else []:
            pe = x.get('priceToEarningsRatio') or x.get('priceEarningsRatio')
            if pe is not None:
                rows.append({'date': x.get('date'), 'pe': pe})
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 502


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    app.run(host='0.0.0.0', port=port)
