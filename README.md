# 🧩 Backend Assessment - Flask (Sunil)

This project is a **backend-only Flask application** developed as part of a technical assessment.  
It receives payment webhooks, processes them in the background (simulating a 30-second delay),  
and provides endpoints to check transaction statuses.

---

## 🚀 Features

✅ `POST /v1/webhooks/transactions` — Accepts webhook JSON, responds **202 Accepted** immediately.  
✅ `GET /` — Health check with current UTC time.  
✅ `GET /v1/transactions/<transaction_id>` — Retrieve transaction status.  
✅ Uses **SQLite** (`db.sqlite`) for data persistence with SQLAlchemy ORM.  
✅ Implements background processing via **threads (30s delay)**.  
✅ Enforces **idempotency** — duplicate transaction IDs are ignored gracefully.  

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite (default) |
| Server | Gunicorn (for Render deployment) |
| Language | Python 3 |

---

## 🧰 Setup Instructions

### 🧩 1️⃣ Create a Virtual Environment and Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
# or
source venv/bin/activate   # For macOS/Linux

pip install -r requirements.txt
🚀 2️⃣ Run the Flask Application
bash
Copy code
flask run
# OR
python app.py
By default, the app will start at:

cpp
Copy code
http://127.0.0.1:5000/
🧪 API Documentation (Postman Friendly)
🩺 1. Health Check
Method: GET
Endpoint: /
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
Endpoint: /v1/webhooks/transactions
URL: http://127.0.0.1:5000/v1/webhooks/transactions

Headers:

pgsql
Copy code
Content-Type: application/json
Request Body:

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
Behavior:

Responds instantly with 202 Accepted.

Saves transaction in the database (status = PROCESSING).

Starts background thread that marks it as PROCESSED after 30 seconds.

🔍 3. Get Transaction Status
Method: GET
Endpoint: /v1/transactions/<transaction_id>
Example URL:

bash
Copy code
http://127.0.0.1:5000/v1/transactions/txn_demo_1
Response (Immediately after POST):

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
Response (After 30 seconds):

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
Behavior:

PROCESSING → PROCESSED transition after background task completes.

🔁 4. Duplicate Webhook (Idempotency Check)
Method: POST
Endpoint: /v1/webhooks/transactions
Request Body (same transaction again):

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
Behavior:

Returns 202 again.

No duplicate row is created in the database.

❌ 5. Invalid Webhook Request
Request Body (missing fields):

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
The database is automatically created as db.sqlite when the app starts.

🗃️ Table: transactions
Column	Type	Description
id	Integer (PK)	Auto-increment primary key
transaction_id	String	Unique transaction reference
source_account	String	Account sending the money
destination_account	String	Account receiving the money
amount	Float	Transaction amount
currency	String	Transaction currency (e.g., INR)
status	String	PROCESSING / PROCESSED
created_at	DateTime	Time when webhook was received
processed_at	DateTime	Time when background task finished

You can open this file using DB Browser for SQLite to verify records.

☁️ Deployment (Render)
🌍 Steps to Deploy
Push your project to a public GitHub repository

Go to https://render.com

Click New → Web Service

Connect your GitHub repository

Set configurations:

Setting	Value
Build Command	pip install -r requirements.txt
Start Command	gunicorn app:app
Environment	Python 3
Region	Singapore (closest to India)

Click Deploy 🚀

Wait for Render to build and deploy your service.

Once deployed, you’ll get a live URL like:

arduino
Copy code
https://backend-assessment-flask.onrender.com/
🌐 Live API Examples
Action	Method	Example URL
Health Check	GET	https://backend-assessment-flask.onrender.com/
Send Webhook	POST	https://backend-assessment-flask.onrender.com/v1/webhooks/transactions
Get Transaction	GET	https://backend-assessment-flask.onrender.com/v1/transactions/txn_demo_1

🧠 Design Choices
Flask for simplicity and rapid development

SQLite for easy persistence (swappable with PostgreSQL for production)

SQLAlchemy for clean database ORM handling

Threads simulate asynchronous background processing

Unique constraint on transaction_id enforces idempotency

📦 Deliverables
Deliverable	Description
🗂️ GitHub Repo Link	Public repository containing this project
🌍 Deployed Link	Live API hosted on Render

👨‍💻 Author
Name: Sunil
Role: Full Stack Python Developer
Tech Stack: Python | Flask | SQLAlchemy | React.js | AWS | Django
