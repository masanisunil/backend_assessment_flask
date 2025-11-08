# Backend Assessment - Flask (Sunil)

This is a complete backend implementation for the assessment. It accepts transaction webhooks,
processes them in the background (simulated 30s delay), and exposes endpoints to check status.

## Features
- `POST /v1/webhooks/transactions` — Accepts webhook JSON, responds **202 Accepted** immediately.
- `GET /` — Health check with current UTC time.
- `GET /v1/transactions/<transaction_id>` — Query transaction status.
- Uses SQLite by default (`db.sqlite`) for persistence with SQLAlchemy ORM.
- Simple background processing implemented with daemon threads (30s delay).
- Idempotency: `transaction_id` has a UNIQUE constraint; duplicates are ignored gracefully.

## How to run locally

1. Make a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:
```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

3. Test endpoints (example):
```bash
# Health
curl http://127.0.0.1:5000/

# Send webhook
curl -X POST http://127.0.0.1:5000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{{"transaction_id":"txn_test_1","source_account":"acc_user_1","destination_account":"acc_merchant_1","amount":100,"currency":"INR"}}'

# Immediately returns 202. Wait ~30s then:
curl http://127.0.0.1:5000/v1/transactions/txn_test_1
```

## Deployment (Render / Railway / Heroku)
1. Create a public GitHub repo and push these files.
2. Create a new Web Service on Render (or Railway/Heroku).
3. Set the start command (Render autoguess) or use Procfile:
   ```
   web: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
   ```
4. If using PostgreSQL in production, set `DATABASE_URL` env var. Otherwise SQLite works on Render if writable.

## Notes on design choices
- **Flask**: lightweight and fast to develop for this assessment.
- **SQLite**: zero-config persistence for quick delivery; swap to Postgres by setting `DATABASE_URL`.
- **Idempotency**: enforced at DB level (unique constraint on `transaction_id`) to prevent duplicate processing.
- **Background**: A production system would use Celery/RQ with a real message broker to ensure durability.
  For the assignment, an in-process thread executor simulates background work and keeps the code small.

## What I deliver (as requested)
- Public GitHub repo link: (push this folder to GitHub)
- Deployed link: (deploy the repo to Render/Heroku and provide the live URL)
