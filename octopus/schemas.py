from marshmallow import fields, Schema, UnmarshalResult


class TaskRequestSchema(Schema):
    url = fields.Url(required=True)


class TaskResultSchea(Schema):
    token = fields.Str(required=True)
    frequency = fields.Int(required=True)
