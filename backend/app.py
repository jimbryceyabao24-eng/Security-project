from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import ipaddress
import re

app = Flask(__name__)
CORS(app)


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "verification",
    "account",
    "update",
    "secure",
    "security",
    "bank",
    "password",
    "signin",
    "confirm",
    "wallet",
    "payment",
    "credential"
]

SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "ow.ly",
    "buff.ly",
    "cutt.ly"
]


def is_ip_address(hostname):
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def analyze_url(url):
    score = 0
    warnings = []

    # Make URL easier to parse
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "http://" + url

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    hostname = parsed.hostname or ""
    full_url = url.lower()

    # Check HTTPS
    if scheme != "https":
        score += 15
        warnings.append("URL does not use HTTPS.")

    # Check IP address
    if hostname and is_ip_address(hostname):
        score += 25
        warnings.append("URL uses an IP address instead of a domain name.")

    # Check @ symbol
    if "@" in parsed.netloc:
        score += 25
        warnings.append("URL contains '@', which can hide the real destination.")

    # Check URL length
    if len(url) > 100:
        score += 10
        warnings.append("URL is unusually long.")

    # Check number of subdomains
    if hostname:
        parts = hostname.split(".")

        if len(parts) > 4:
            score += 15
            warnings.append("URL contains an unusually large number of subdomains.")

    # Check suspicious keywords
    found_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in full_url:
            found_keywords.append(keyword)

    if found_keywords:
        score += min(len(found_keywords) * 5, 20)
        warnings.append(
            "Suspicious keywords detected: "
            + ", ".join(found_keywords)
        )

    # Check URL shortener
    if hostname in SHORTENERS:
        score += 20
        warnings.append("URL uses a URL shortening service.")

    # Check excessive hyphens
    if hostname.count("-") >= 3:
        score += 10
        warnings.append("Domain contains many hyphens.")

    # Check excessive dots
    if hostname.count(".") >= 4:
        score += 10
        warnings.append("Domain contains many subdomain levels.")

    # Check suspicious characters
    suspicious_chars = re.findall(r"[%$&*!]", url)

    if len(suspicious_chars) >= 3:
        score += 10
        warnings.append("URL contains many unusual special characters.")

    # Limit score
    score = min(score, 100)

    # Determine risk
    if score >= 60:
        risk = "High Risk"
    elif score >= 30:
        risk = "Suspicious"
    else:
        risk = "Low Risk"

    return {
        "url": url,
        "score": score,
        "risk": risk,
        "warnings": warnings
    }


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "API is running"
    })


@app.route("/api/check-url", methods=["POST"])
def check_url():

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({
            "error": "URL is required."
        }), 400

    url = data["url"].strip()

    if not url:
        return jsonify({
            "error": "Please enter a URL."
        }), 400

    if len(url) > 2048:
        return jsonify({
            "error": "URL is too long."
        }), 400

    try:
        result = analyze_url(url)

        return jsonify(result)

    except Exception as error:
        return jsonify({
            "error": "Unable to analyze URL."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    