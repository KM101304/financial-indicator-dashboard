import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

function App() {
  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  const [logs, setLogs] = useState([]);
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [charts, setCharts] = useState({});
  const [darkMode, setDarkMode] = useState(true);
  const [previousSignalIds, setPreviousSignalIds] = useState(new Set());

  const handleScan = async () => {
    setLoading(true);
    setLogs([]);
    setCharts({});

    const response = await fetch('http://localhost:5000/scan');
    const data = await response.json();

    setLogs(data.logs);

    const backendCharts = data.charts || {};  
    setCharts(backendCharts);             

    const newSignals = data.signals.filter(signal => {
      const id = `${signal.title}-${signal.timestamp}`;
      return !previousSignalIds.has(id);
    }).slice(0, 3);

    const updatedSignalIds = new Set(previousSignalIds);
    newSignals.forEach(signal => {
      const id = `${signal.title}-${signal.timestamp}`;
      updatedSignalIds.add(id);
    });

    setPreviousSignalIds(updatedSignalIds);
    setSignals(newSignals);

    const allTickers = new Set(newSignals.flatMap(sig => sig.spike_tickers || []));

for (let ticker of allTickers) {
  // If backend (yfinance) already provided a chart (e.g. NVDA, ORCL),
  // don’t bother calling CoinGecko.
  if (backendCharts[ticker] && backendCharts[ticker].length > 0) {
    continue;
  }

  // Fallback: try CoinGecko for crypto tickers only
  const coin = mapTickerToCoinId(ticker);
  if (!coin) continue;

  try {
    const res = await fetch(
      `https://api.coingecko.com/api/v3/coins/${coin}/market_chart?vs_currency=usd&days=1`
    );
    const priceData = await res.json();
    const chartData = priceData.prices.map(([timestamp, price]) => ({
      time: new Date(timestamp).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      }),
      price,
    }));
    setCharts(prev => ({ ...prev, [ticker]: chartData }));
  } catch (err) {
    console.error('Chart error for', ticker, err);
  }
}


    setLoading(false);
  };

  const mapTickerToCoinId = ticker => {
    const symbol = ticker.replace('$', '').toLowerCase();
    const map = {
      btc: 'bitcoin',
      eth: 'ethereum',
      sol: 'solana',
      link: 'chainlink',
      xrp: 'ripple',
      doge: 'dogecoin',
      ada: 'cardano',
      shib: 'shiba-inu',
    };
    return map[symbol] || null;
  };

  const themeStyles = {
    backgroundColor: darkMode ? '#1a1a1a' : '#fef7e0',
    color: darkMode ? '#c2b280' : '#1a1a1a',
    minHeight: '100vh',
  };

  const accentColor = darkMode ? '#3a5c27' : '#ff7a00';
  const highlightColor = darkMode ? '#00ff00' : '#008000';

  return (
    <div style={{ padding: '0px', fontFamily: 'Inter, sans-serif', ...themeStyles }}>
      <div style={{
        backgroundColor: '#000',
        color: accentColor,
        overflow: 'hidden',
        whiteSpace: 'nowrap',
        fontFamily: 'monospace',
        padding: '10px 0',
        width: '100%',
        fontSize: '16px',
        position: 'relative'
      }}>
        <span style={{
          display: 'inline-block',
          paddingLeft: '100%',
          animation: 'scroll-left 25s linear infinite'
        }}>
          N3C – FinView • Real-time Alt-Data Scanning • Reddit • 4chan • GPT Analysis • Ticker Spike Detection
        </span>
        <style>
          {`@keyframes scroll-left {
              0% { transform: translateX(0); }
              100% { transform: translateX(-100%); }
          }`}
        </style>
      </div>

      <header style={{ margin: '40px' }}>
        <h1 style={{ fontSize: '4rem', fontWeight: 800, margin: 0, color: accentColor }}>
          N3C<span style={{ fontSize: '1.2rem', fontWeight: 600, color: accentColor, marginLeft: '8px' }}>FinView</span>
        </h1>
        <button
          onClick={() => setDarkMode(!darkMode)}
          style={{
            marginTop: '16px',
            padding: '8px 16px',
            backgroundColor: accentColor,
            color: darkMode ? '#1a1a1a' : '#fff6e6',
            border: 'none',
            cursor: 'pointer',
            borderRadius: '0px',
            fontWeight: '600'
          }}
        >
          Toggle {darkMode ? 'Light' : 'Dark'} Mode
        </button>
      </header>

      <div style={{ padding: '0 40px' }}>
        <p style={{ fontSize: '1.1rem', fontWeight: 500, marginBottom: '30px' }}>
          Real-time alt-data from Reddit & 4chan. Powered by GPT and no-code innovation.
        </p>

        <button
          onClick={handleScan}
          disabled={loading}
          style={{
            padding: '14px 28px',
            fontSize: '1rem',
            fontWeight: 600,
            backgroundColor: accentColor,
            color: darkMode ? '#1a1a1a' : '#fff6e6',
            border: 'none',
            borderRadius: '0px',
            cursor: 'pointer',
            marginBottom: '30px'
          }}
        >
          {loading ? 'Scanning...' : 'Scan for Signals'}
        </button>

        <div style={{
          background: '#000',
          color: highlightColor,
          padding: '15px',
          height: '160px',
          overflowY: 'scroll',
          borderRadius: '0px',
          fontFamily: 'monospace',
          marginBottom: '30px',
          boxShadow: 'inset 0 0 8px #00ff00'
        }}>
          {logs.length === 0 ? <p>No logs yet.</p> : logs.map((log, i) => <p key={i}>> {log}</p>)}
        </div>

        {signals.map((signal, idx) => (
          <div
            key={idx}
            style={{
              backgroundColor: darkMode ? '#2a2a2a' : '#fff',
              padding: '24px',
              borderRadius: '0px',
              marginBottom: '35px',
              boxShadow: '0 6px 16px rgba(0,0,0,0.5)',
              borderLeft: `6px solid ${accentColor}`
            }}
          >
            <h3 style={{ marginBottom: '8px', fontSize: '1.3rem', fontWeight: 700, color: accentColor }}>{signal.title}</h3>
            <p><strong>Time:</strong> {signal.timestamp}</p>
            <p><strong>Summary:</strong> {signal.summary}</p>
            <p><strong>Sentiment:</strong> {signal.sentiment}</p>
            <div style={{ marginBottom: '12px' }}>
              <strong>Sources:</strong>
              {signal.sources.map((src, i) => (
                <div key={i}>
                  <a href={src} target="_blank" rel="noopener noreferrer" style={{ color: accentColor }}>
                    {src}
                  </a>
                </div>
              ))}
            </div>

            {(signal.spike_tickers || []).map(ticker => (
              <div key={ticker} style={{ marginTop: '25px' }}>
                <h4 style={{ marginBottom: '10px', fontWeight: 600, color: highlightColor }}>{ticker} – 24h Price Chart</h4>
                {charts[ticker] ? (
                  <ResponsiveContainer width="100%" height={200}>
                    <LineChart data={charts[ticker]}>
                      <XAxis dataKey="time" hide />
                      <YAxis domain={['auto', 'auto']} />
                      <Tooltip />
                      <Line
                        type="monotone"
                        dataKey="price"
                        stroke={accentColor}
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <p style={{ color: '#aaa' }}>No chart data (unsupported or unavailable).</p>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
