import json
import os

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return []

def semgrep_summary(data):
    return f"<li>🛡️ Semgrep: <strong>{len(data.get('results', []))}</strong> issues found</li>"

def trivy_summary(data):
    count = sum(len(r.get("Vulnerabilities", [])) for r in data if "Vulnerabilities" in r)
    return f"<li>🐳 Trivy: <strong>{len(data.get('results', []))}</strong> vulnerabilities</li>"

def generate_html(semgrep_data, trivy_data):
    return f"""
    <html>
    <head>
        <title>Security Scan Summary</title>
        <style>
            body {{ font-family: sans-serif; padding: 2em; }}
            h1 {{ color: #c0392b; }}
            li {{ margin: 0.5em 0; }}
        </style>
    </head>
    <body>
        <h1>🔐 Security Scan Summary</h1>
        <ul>
            {semgrep_summary(semgrep_data)}
            {trivy_summary(trivy_data)}
            <li>🕷️ ZAP: <a href="zap-report/zap.html">View full report</a></li>
        </ul>
        <p>All detailed reports are saved as Jenkins artifacts.</p>
    </body>
    </html>
    """

semgrep = load_json("semgrep-report/semgrep.json")
trivy = load_json("trivy-report/trivy.json")

html = generate_html(semgrep, trivy)
with open("summary.html", "w") as f:
    f.write(html)

