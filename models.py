from db import db
from datetime import datetime, timezone

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(128), nullable=False, unique=True, index=True)
    source_account = db.Column(db.String(128), nullable=False)
    destination_account = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(8), nullable=False)
    status = db.Column(db.String(32), nullable=False)  # PROCESSING or PROCESSED
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    processed_at = db.Column(db.DateTime(timezone=True), nullable=True)
