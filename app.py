import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from db import db, init_db
from models import Transaction
from worker import enqueue_processing

app = Flask(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

# ---------------- Health Check ----------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "HEALTHY",
        "current_time": datetime.now(timezone.utc).isoformat()
    }), 200


# ---------------- Webhook Receiver ----------------
@app.route("/v1/webhooks/transactions", methods=["POST"])
def receive_webhook():
    data = request.get_json()
    if not data:
        abort(400, "Invalid JSON")

    required = {"transaction_id", "source_account", "destination_account", "amount", "currency"}
    if not required.issubset(data):
        abort(400, "Missing required fields")

    txn_id = data["transaction_id"]

    try:
        txn = Transaction(
            transaction_id=txn_id,
            source_account=data["source_account"],
            destination_account=data["destination_account"],
            amount=float(data["amount"]),
            currency=data["currency"],
            status="PROCESSING",
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(txn)
        db.session.commit()
        enqueue_processing(txn.id)
    except IntegrityError:
        db.session.rollback()
        # Duplicate transaction_id → ignore gracefully
    except Exception:
        db.session.rollback()

    return jsonify({"message": "Webhook received"}), 202


# ---------------- Get Transaction Status ----------------
@app.route("/v1/transactions/<transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    txn = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not txn:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "transaction_id": txn.transaction_id,
        "source_account": txn.source_account,
        "destination_account": txn.destination_account,
        "amount": txn.amount,
        "currency": txn.currency,
        "status": txn.status,
        "created_at": txn.created_at.isoformat() if txn.created_at else None,
        "processed_at": txn.processed_at.isoformat() if txn.processed_at else None
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
