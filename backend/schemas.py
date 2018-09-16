"""
This module should cover the validating, serializing and deserializing
needs of this project
"""
from marshmallow import fields, Schema, UnmarshalResult


class TaskRequestSchema(Schema):
    """
    Validates requests to start an analysis.
    """

    url = fields.Url(required=True)


class TaskResultSchema(Schema):
    """
    Serializes the result of analyzing a web page
    """
    token = fields.Str(required=True)
    frequency = fields.Int(required=True)


class TokenSchema(Schema):
    """
    Deserializes the DB entry of a token, to its desencrypted form.
    """
    encrypted = fields.Str(required=True, dump_to="token")
    frequency = fields.Int()
