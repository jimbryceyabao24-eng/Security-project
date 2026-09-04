import { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const checkURL = async (e) => {
    e.preventDefault();

    setError("");
    setResult(null);

    if (!url.trim()) {
      setError("Please enter a URL.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/check-url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
      }

      setResult(data);
    } catch (err) {
      setError(
        "Could not connect to the server. Make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = () => {
    if (!result) return "";

    if (result.score >= 60) {
      return "high";
    }

    if (result.score >= 30) {
      return "suspicious";
    }

    return "low";
  };

  return (
    <div className="app">
      <div className="container">

        <div className="header">
          <div className="shield">🛡️</div>

          <h1>Phishing URL Detector</h1>

          <p>
            "Detect the Trap Before You Take The Bait."
          </p>
        </div>

        <form onSubmit={checkURL} className="url-form">

          <label htmlFor="url">
            Enter URL
          </label>

          <div className="input-group">

            <input
              id="url"
              type="text"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />

            <button type="submit" disabled={loading}>
              {loading ? "Checking..." : "Check URL"}
            </button>

          </div>

        </form>

        {error && (
          <div className="error">
            ⚠️ {error}
          </div>
        )}

        {result && (
          <div className="result">

            <div className={`risk-card ${getRiskClass()}`}>

              <div className="risk-icon">
                {result.score >= 60
                  ? "🚨"
                  : result.score >= 30
                  ? "⚠️"
                  : "✅"}
              </div>

              <div>
                <h2>{result.risk}</h2>

                <p>
                  Risk Score: <strong>{result.score}/100</strong>
                </p>
              </div>

            </div>

            <div className="score-container">

              <div className="score-header">
                <span>Risk Score</span>
                <strong>{result.score}%</strong>
              </div>

              <div className="progress">
                <div
                  className={`progress-bar ${getRiskClass()}`}
                  style={{ width: `${result.score}%` }}
                ></div>
              </div>

            </div>

            <div className="checked-url">

              <h3>🔗 Checked URL</h3>

              <p>{result.url}</p>

            </div>

            <div className="warnings">

              <h3>🔍 Analysis</h3>

              {result.warnings.length === 0 ? (

                <div className="safe">
                  ✅ No common phishing indicators were detected.
                </div>

              ) : (

                result.warnings.map((warning, index) => (
                  <div className="warning" key={index}>
                    ⚠️ {warning}
                  </div>
                ))

              )}

            </div>

          </div>
        )}

        <div className="info">

          <h3>💡 Important</h3>

          <p>
            This tool checks common URL characteristics associated
            with phishing. A low-risk result does not guarantee that
            a website is safe.
          </p>

        </div>

      </div>
    </div>
  );
}

export default App;