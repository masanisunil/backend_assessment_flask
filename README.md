# 🧩 Backend Assessment - Flask (Sunil)

This is a backend-only Flask application built as part of a full-stack assessment.  
It receives payment webhooks, processes them in the background (simulating a 30-second delay),  
and provides endpoints to check transaction statuses.

---

## 🚀 Features
- `POST /v1/webhooks/transactions` — Accepts webhook JSON, responds **202 Accepted** immediately.  
- `GET /` — Health check with current UTC time.  
- `GET /v1/transactions/<transaction_id>` — Retrieve transaction status.  
- Uses **SQLite** (local file `db.sqlite`) for persistent storage.  
- Implements **background processing** via daemon threads (30s simulated delay).  
- Ensures **idempotency** — duplicate transaction IDs are ignored gracefully.

---

## ⚙️ Tech Stack
- **Flask** — lightweight Python web framework  
- **Flask-SQLAlchemy** — ORM for database management  
- **SQLite** — default local storage (no setup needed)  
- **Gunicorn** — production-ready WSGI server (for Render deployment)

---

## 🧰 How to Run Locally

### 1️⃣ Clone the repo and create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # For Windows
# or
source venv/bin/activate   # For macOS/Linux

pip install -r requirements.txt
2️⃣ Start the Flask app
bash
Copy code
flask run
or

bash
Copy code
python app.py
By default, the app runs at:

cpp
Copy code
http://127.0.0.1:5000/
🧪 Postman API Documentation
🩺 1. Health Check
Method: GET
URL: http://127.0.0.1:5000/

Response:

json
Copy code
{
  "status": "HEALTHY",
  "current_time": "2025-11-08T14:30:00Z"
}
💳 2. Receive Webhook
Method: POST
URL: http://127.0.0.1:5000/v1/webhooks/transactions
Headers:

pgsql
Copy code
Content-Type: application/json
Body (JSON):

json
Copy code
{
  "transaction_id": "txn_demo_1",
  "source_account": "acc_user_001",
  "destination_account": "acc_merchant_001",
  "amount": 500,
  "currency": "INR"
}
Response:

json
Copy code
{
  "message": "Webhook received"
}
✅ Behavior:

Returns 202 Accepted instantly.

Stores transaction in DB (status = PROCESSING).

Starts background thread (30s delay).

🔍 3. Get Transaction Status
Method: GET
URL: http://127.0.0.1:5000/v1/transactions/<transaction_id>

Example:

bash
Copy code
http://127.0.0.1:5000/v1/transactions/txn_demo_1
Response (immediately after webhook):

json
Copy code
{
  "transaction_id": "txn_demo_1",
  "source_account": "acc_user_001",
  "destination_account": "acc_merchant_001",
  "amount": 500.0,
  "currency": "INR",
  "status": "PROCESSING",
  "created_at": "2025-11-08T14:31:00Z",
  "processed_at": null
}
Response (after 30 seconds):

json
Copy code
{
  "transaction_id": "txn_demo_1",
  "source_account": "acc_user_001",
  "destination_account": "acc_merchant_001",
  "amount": 500.0,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2025-11-08T14:31:00Z",
  "processed_at": "2025-11-08T14:31:30Z"
}
✅ Behavior:

Initially returns “PROCESSING”

After 30s background thread updates to “PROCESSED”

🔁 4. Duplicate Webhook (Idempotency)
Method: POST
URL: http://127.0.0.1:5000/v1/webhooks/transactions

Body (same transaction again):

json
Copy code
{
  "transaction_id": "txn_demo_1",
  "source_account": "acc_user_001",
  "destination_account": "acc_merchant_001",
  "amount": 500,
  "currency": "INR"
}
Response:

json
Copy code
{
  "message": "Webhook received"
}
✅ Behavior:

Returns 202 again (gracefully accepted)

No duplicate transaction is created in the database

❌ 5. Invalid Webhook Request
Body (missing required fields):

json
Copy code
{
  "transaction_id": "invalid"
}
Response:

json
Copy code
{
  "message": "Missing required fields"
}
Status: 400 Bad Request

🧩 Database (SQLite)
The app automatically creates db.sqlite in the project folder.
You can inspect it using DB Browser for SQLite → Table: transactions.

Column	Description
id	Auto primary key
transaction_id	Unique transaction reference
source_account	User account
destination_account	Merchant account
amount	Transaction amount
currency	e.g., INR
status	PROCESSING / PROCESSED
created_at	Timestamp of webhook
processed_at	Timestamp after background job

☁️ Deployment (Render)
Steps:
Push your project to a public GitHub repo

Go to https://render.com

Click New → Web Service

Connect your GitHub repo

Configure:

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Deploy 🚀

Your live API will look like:

arduino
Copy code
https://backend-assessment-flask.onrender.com/
Examples:

bash
Copy code
GET https://backend-assessment-flask.onrender.com/
POST https://backend-assessment-flask.onrender.com/v1/webhooks/transactions
GET https://backend-assessment-flask.onrender.com/v1/transactions/txn_demo_1
🧠 Design Choices
Flask for simplicity and speed

SQLite for easy local persistence

SQLAlchemy ORM for clean DB interaction

Threads to simulate async background processing (30s delay)

Unique transaction_id ensures idempotency

📦 Deliverables
✅ Public GitHub Repository Link

✅ Live Deployed Link (Render)

👨‍💻 Author
Name: Sunil
Role: Full Stack Python Developer
Tech Stack: Python | Flask | SQLAlchemy | React Js | AWS | Django

