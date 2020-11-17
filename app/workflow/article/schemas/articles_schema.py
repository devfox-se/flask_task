from marshmallow import Schema, fields


class ArticlesSchema(Schema):
    id = fields.Integer(required=False)
    title = fields.String(required=True)
    date = fields.DateTime(required=True)
    content = fields.String(required=True)
