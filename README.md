# 🧩 Backend Assessment - Flask (Sunil)

This is a backend-only Flask application built as part of a technical assessment.  
It receives payment webhooks, processes them in the background (simulating a 30-second delay),  
and provides endpoints to check transaction statuses.

🌍 **Live API:** [https://web-production-40bb4.up.railway.app/](https://web-production-40bb4.up.railway.app/)

---

## 🚀 Features

✅ `POST /v1/webhooks/transactions` — Accepts webhook JSON, responds **202 Accepted** immediately.  
✅ `GET /` — Health check with current UTC time.  
✅ `GET /v1/transactions/<transaction_id>` — Retrieve transaction status.  
✅ Uses **SQLite** for persistent storage (via SQLAlchemy).  
✅ Implements **background processing** with a 30-second simulated delay.  
✅ Ensures **idempotency** — duplicate `transaction_id`s are ignored gracefully.

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Server | Gunicorn |
| Language | Python 3.11 |

---

## 🧰 Setup Instructions (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/masanisunil/backend_assessment_flask.git
cd backend_assessment_flask
2️⃣ Create a virtual environment and install dependencies
bash
Copy code
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate   # On macOS/Linux

pip install -r requirements.txt
3️⃣ Run the application
bash
Copy code
flask run
# or
python app.py
App runs locally at:

cpp
Copy code
http://127.0.0.1:5000/
🧪 API Endpoints (Postman Ready)
1️⃣ Health Check
Method: GET
URL:

arduino
Copy code
https://web-production-40bb4.up.railway.app/
Response:

json
Copy code
{
  "status": "HEALTHY",
  "current_time": "2025-11-08T15:51:07.346602+00:00"
}
2️⃣ Receive Webhook
Method: POST
URL:

bash
Copy code
https://web-production-40bb4.up.railway.app/v1/webhooks/transactions
Headers:

pgsql
Copy code
Content-Type: application/json
Body (JSON):

json
Copy code
{
  "transaction_id": "txn_test_10",
  "source_account": "acc_user_001",
  "destination_account": "acc_merchant_001",
  "amount": 200,
  "currency": "INR"
}
Response:

json
Copy code
{"message": "Webhook received"}
✅ Behavior:

Immediately returns 202 Accepted

Saves transaction as PROCESSING

After 30 seconds → updates status to PROCESSED

3️⃣ Get Transaction Status
Method: GET
URL:

bash
Copy code
https://web-production-40bb4.up.railway.app/v1/transactions/txn_test_10
Response (after 30 seconds):

json
Copy code
{
  "transaction_id": "txn_test_10",
  "source_account": "acc_user_001",
  "destination_account": "acc_merchant_001",
  "amount": 200.0,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2025-11-08T15:56:27.309226",
  "processed_at": "2025-11-08T15:56:57.393601"
}
4️⃣ Duplicate Webhook Test
Body:

json
Copy code
{
  "transaction_id": "txn_test_10",
  "source_account": "acc_user_001",
  "destination_account": "acc_merchant_001",
  "amount": 200,
  "currency": "INR"
}
✅ Behavior:

Returns {"message": "Webhook received"}

No duplicate transaction created (idempotency enforced)

5️⃣ Invalid Webhook Example
Body:

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
🧩 Database Schema (SQLite)
Column	Type	Description
id	Integer (PK)	Auto primary key
transaction_id	String	Unique transaction reference
source_account	String	Account sending the money
destination_account	String	Account receiving the money
amount	Float	Transaction amount
currency	String	Transaction currency (e.g., INR)
status	String	PROCESSING / PROCESSED
created_at	DateTime	Webhook received timestamp
processed_at	DateTime	Timestamp after background job completes

☁️ Deployment (Railway)
✅ Deployed on Railway.app
✅ Python version: 3.11.8
✅ Start command:

nginx
Copy code
gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
Live API URL:
👉 https://web-production-40bb4.up.railway.app/

🧠 Design Highlights
Flask + SQLAlchemy — lightweight, simple, and efficient backend stack

SQLite — easy persistent database for assessment use

Thread-based background job — simulates async processing

Idempotent — prevents duplicate transactions

Gunicorn — production-ready deployment server

📦 Deliverables
Item	Description
🗂️ GitHub Repo	https://github.com/masanisunil/backend_assessment_flask
🌍 Live API	https://web-production-40bb4.up.railway.app/

👨‍💻 Author
Name: Sunil
Role: Full Stack Python Developer
Stack: Python | Flask | SQLAlchemy | React.js | AWS | Django
