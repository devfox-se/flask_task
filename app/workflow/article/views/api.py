from flask import request
from flask_api import status
from flask_restful import Resource

from core.errors import ValidationError
from workflow.article.schemas.articles_schema import ArticlesSchema
from workflow.models import ArticleModel, db


class ArticlesResource(Resource):

    def get(self):
        articles = ArticleModel.query.all()
        serializer = ArticlesSchema()
        data = serializer.dump(articles, many=True)
        return {"data": data}, status.HTTP_200_OK

    def post(self):
        payload = request.get_json(force=True)
        serializer = ArticlesSchema()
        errors = serializer.validate(payload)

        if errors:
            raise ValidationError(errors=errors)

        data = serializer.load(payload)
        article = ArticleModel(**data)
        db.session.add(article)
        db.session.commit()
        return {"message": "Success"}, status.HTTP_200_OK


class ArticlesManageResource(Resource):

    def get(self, _id):
        article = ArticleModel.query.filter_by(id=_id).first()
        if not article:
            return {"message": "Article not found."}, status.HTTP_404_NOT_FOUND
        serializer = ArticlesSchema()
        return serializer.dump(article), status.HTTP_200_OK

    def put(self, _id):
        article = ArticleModel.query.filter_by(id=_id).first()
        if not article:
            return {"message": "Article not found."}, status.HTTP_404_NOT_FOUND

        payload = request.get_json(force=True)
        serializer = ArticlesSchema(partial=True)
        errors = serializer.validate(payload)

        if errors:
            raise ValidationError(errors=errors)

        data = serializer.load(payload)
        for key, value in data.items():
            setattr(article, key, value)
        db.session.commit()
        return {"message": "Success"}, status.HTTP_200_OK

    def delete(self, _id):
        article = ArticleModel.query.filter_by(id=_id).first()
        if not article:
            return {"message": "Article not found."}, status.HTTP_404_NOT_FOUND
        db.session.delete(article)
        db.session.commit()
        return {"message": "Success"}, status.HTTP_200_OK
