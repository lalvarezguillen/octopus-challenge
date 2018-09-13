from marshmallow import fields, Schema, UnmarshalResult


class URLSchema(Schema):
    value = fields.Url(required=True)
