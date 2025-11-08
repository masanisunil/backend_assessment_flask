import time
import threading
from datetime import datetime, timezone
from db import db
from models import Transaction

# FIX: pass Flask app instance explicitly so background thread has context
def _process(app, txn_db_id):
    with app.app_context():
        try:
            print(f"⏳ Started background processing for txn ID {txn_db_id}")
            # Simulate external API delay
            time.sleep(30)
            
            txn = Transaction.query.get(txn_db_id)
            if not txn:
                print("⚠️ Transaction not found in DB.")
                return

            txn.status = "PROCESSED"
            txn.processed_at = datetime.now(timezone.utc)
            db.session.commit()
            print(f"✅ Transaction {txn.transaction_id} marked as PROCESSED")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Background worker failed: {e}")

def enqueue_processing(txn_db_id):
    from app import app  # Import the Flask app instance
    t = threading.Thread(target=_process, args=(app, txn_db_id), daemon=True)
    t.start()
