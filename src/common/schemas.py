from typing import Dict, Any

from marshmallow import Schema, fields, post_load

from src.common.models import Transaction, SignedTransaction, Block


class TransactionSchema(Schema):
    uuid = fields.UUID()
    sender = fields.String()
    receiver = fields.String()
    amount = fields.Float()
    fees = fields.Float()

    @post_load
    def _make_model(self, data: Dict[str, Any]) -> Transaction:
        return Transaction(**data)


class SignedTransactionSchema(Schema):
    transaction = fields.Nested(TransactionSchema)
    signature = fields.String()

    @post_load
    def _make_model(self, data: Dict[str, Any]) -> SignedTransaction:
        return SignedTransaction(**data)


class BlockSchema(Schema):
    prev_hash = fields.String(required=False)
    signed_transactions = fields.List(fields.Nested(SignedTransactionSchema))
    nounce = fields.Int(required=False)

    @post_load
    def _make_model(self, data: Dict[str, Any]) -> Block:
        return Block(**data)
