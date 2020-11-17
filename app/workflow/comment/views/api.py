from flask import request
from flask_api import status
from flask_restful import Resource

from core.errors import ValidationError
from workflow.comment.schemas.comments_schema import CommentSchema
from workflow.models import CommentModel, db


class CommentsResource(Resource):
    def get(self, article_id):
        comment = CommentModel.query.filter_by(article=article_id)
        serializer = CommentSchema()
        data = serializer.dump(comment, many=True)
        return {"data": data}, status.HTTP_200_OK

    def post(self, article_id):
        payload = request.get_json(force=True)
        serializer = CommentSchema()
        errors = serializer.validate(payload)

        if errors:
            raise ValidationError(errors=errors)

        data = serializer.load(payload)
        comment = CommentModel(**data, article=article_id)
        db.session.add(comment)
        db.session.commit()
        return {"message": "Success"}, status.HTTP_200_OK


class CommentsManageResource(Resource):
    def get(self, article_id, _id):
        comment = CommentModel.query.filter_by(article=article_id, id=_id).first()
        if not comment:
            return {"message": "Comment not found."}, status.HTTP_404_NOT_FOUND

        serializer = CommentSchema()
        return serializer.dump(comment), status.HTTP_200_OK

    def put(self, article_id, _id):
        comment = CommentModel.query.filter_by(article=article_id, id=_id).first()
        if not comment:
            return {"message": "Comme nt not found."}, status.HTTP_404_NOT_FOUND

        payload = request.get_json(force=True)
        serializer = CommentSchema(partial=True)
        errors = serializer.validate(payload)

        if errors:
            raise ValidationError(errors=errors)

        data = serializer.load(payload)
        for key, value in data.items():
            setattr(comment, key, value)
        db.session.commit()
        return {"message": "Success"}, status.HTTP_200_OK

    def delete(self, article_id, _id):
        comment = CommentModel.query.filter_by(article=article_id, id=_id).first()
        if not comment:
            return {"message": "Comment not found."}, status.HTTP_404_NOT_FOUND

        db.session.delete(comment)
        db.session.commit()
        return {"message": "Success"}, status.HTTP_200_OK
