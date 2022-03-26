from typing import Dict, Any

from marshmallow import Schema, fields, post_load

from common.models import PubKey, Transaction, SignedTransaction, Block, MINING_REWARD_ADDRESS


class PubKeyField(fields.Field):
    def _serialize(self, value: PubKey, attr: str, obj: Any, **kwargs) -> str:
        return value.dumps()

    def _deserialize(self, value: str, attr, data, **kwargs) -> PubKey:
        if value == MINING_REWARD_ADDRESS:
            return PubKey(MINING_REWARD_ADDRESS)
        return PubKey.load_from_bytes(value.encode("utf-8"))


class _TransactionSchema(Schema):
    uuid = fields.String()
    receiver = PubKeyField()
    sender = PubKeyField()
    amount = fields.Float()
    fees = fields.Float()

    @post_load
    def _make_model(self, data: Dict[str, Any], **kwargs) -> Transaction:
        return Transaction(**data)


TransactionSchema = _TransactionSchema()


class _SignedTransactionSchema(Schema):
    transaction = fields.Nested(TransactionSchema)
    signature = fields.String()

    @post_load
    def _make_model(self, data: Dict[str, Any], **kwargs) -> SignedTransaction:
        return SignedTransaction(**data)


SignedTransactionSchema = _SignedTransactionSchema()


class _BlockSchema(Schema):
    prev_hash = fields.String()
    height = fields.Int()
    signed_transactions = fields.List(fields.Nested(SignedTransactionSchema))
    nonce = fields.Int(required=False)

    @post_load
    def _make_model(self, data: Dict[str, Any], **kwargs) -> Block:
        return Block(**data)


BlockSchema = _BlockSchema()
