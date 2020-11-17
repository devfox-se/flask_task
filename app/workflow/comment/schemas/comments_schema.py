from marshmallow import Schema, fields


class CommentSchema(Schema):
    id = fields.Integer(required=False)
    message = fields.String(required=True)
    date = fields.DateTime(required=True)
