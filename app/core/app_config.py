from dynaconf import settings
from flask import Flask
from flask_restful import Api

from core.errors import handle_exception, ServiceException
from workflow.article.views.api import ArticlesResource, ArticlesManageResource
from workflow.comment.views.api import CommentsResource, CommentsManageResource
from workflow.models import db


def create_app(name, testing=False):
    app = Flask(name)
    app.testing = testing
    app.url_map.strict_slashes = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.POSTGRES_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    api = Api(app)
    api.add_resource(ArticlesResource, '/api/v1/articles/', endpoint="articles")
    api.add_resource(ArticlesManageResource, '/api/v1/articles/<int:_id>', endpoint="manage_articles")
    api.add_resource(CommentsResource, '/api/v1/articles/<int:article_id>/comments/', endpoint="comments")
    api.add_resource(CommentsManageResource, '/api/v1/articles/<int:article_id>/comments/<int:_id>', endpoint="manage_comments")

    app.errorhandler(ServiceException)(handle_exception)

    db.init_app(app)

    return app
