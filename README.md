🧠 N3C FinView — Real‑Time Alt‑Data Sentiment & Signal Scanner
N3C FinView is a full‑stack dashboard that scans Reddit, 4chan, and crypto tickers to detect emerging sentiment shifts, GPT‑generated summaries, and short‑term spike signals.
It uses Flask, PRAW, VADER, OpenAI, Recharts, and CoinGecko to produce a clean, real‑time intelligence dashboard.

🚀 Features
🔍 Data Sources
Reddit sentiment scanning

4chan /biz/ scraping

GPT‑powered summarization + insights

Ticker spike detection from posts

📈 Frontend Dashboard (React)
Real‑time log viewer

GPT‑generated signal summaries

Sentiment classification

Links to source posts

Automatic 24h price charts via CoinGecko

Dark/Light mode toggle

🛠 Backend (Flask)
/scan endpoint triggers alt‑data sweep

Scrapes Reddit & 4chan

Performs sentiment analysis

Detects ticker spikes

Returns structured signals + logs

📂 Project Structure
financial-indicator-dashboard/
│
├── backend/
│   ├── app.py                  # Main Flask API
│   ├── scraper.py              # Reddit + 4chan scraping logic
│   ├── sentiment.py            # VADER & GPT sentiment
│   ├── utils.py
│   ├── requirements.txt        # Backend dependencies
│   └── venv/ (ignored)
│
└── frontend/
    ├── src/
    │   ├── App.js              # React dashboard UI
    │   ├── components/         # Charts, visuals
    │   └── ...
    ├── package.json
    └── node_modules/ (ignored)
🔧 Installation & Setup
1. Clone the Repository
git clone https://github.com/KM101304/financial-indicator-dashboard.git
cd financial-indicator-dashboard
🖥 Backend Setup (Flask)
Create virtual environment (recommended)
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Environment Variables
Create a .env file in backend/:

OPENAI_API_KEY=your_key_here
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=finview/0.1
Or set manually in Windows:

set OPENAI_API_KEY=xxx
set REDDIT_CLIENT_ID=xxx
set REDDIT_CLIENT_SECRET=xxx
set REDDIT_USER_AGENT=finview
Run Backend
python app.py
The API will start on:

http://127.0.0.1:5000
🌐 Frontend Setup (React)
cd ../frontend
npm install
npm start
The dashboard opens at:

http://localhost:3000
▶️ How It Works
Click "Scan for Signals"

Backend scrapes Reddit & 4chan posts

Tickers inside posts are detected ($BTC, $ETH, etc.)

Sentiment is analyzed using VADER + GPT

Signals (summary + links + tickers) are returned

App.js fetches CoinGecko price charts for detected tickers

Dashboard displays everything in real time

❗ Important Notes
backend/venv/ and frontend/node_modules/ are ignored via .gitignore

API keys should NOT be committed to GitHub

CoinGecko supports only major crypto tickers (BTC/ETH/SOL/etc.)

🛤 Future Improvements
Websockets for continuous real‑time streaming

More subreddits

Model‑based anomaly scoring

Web deployment (Railway/Vercel/Render)

📜 License
MIT License — free to use, modify, and extend.
