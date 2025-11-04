# Personal Digest

Personal Digest automatically fetches the latest stock news, summarizes it with AI, and sends a daily email digest.

## Run locally

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run manually:
   ```bash
   python src/main.py
   ```

## Automation

A launchd job or GitHub Action runs the script daily to send digests automatically.
