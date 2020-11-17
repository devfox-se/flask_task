from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ArticleModel(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    date = db.Column(db.DateTime())

    def __init__(self, title, content, date):
        self.title = title
        self.content = content
        self.date = date

    def __repr__(self):
        return f"<Article {self.title}>"


class CommentModel(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String())
    date = db.Column(db.DateTime())
    article = db.Column(db.Integer(), db.ForeignKey(ArticleModel.id))

    # author = db.Column()

    def __init__(self, message, date, article):
        self.message = message
        self.date = date
        self.article = article

    def __repr__(self):
        return f"<Comment {self.message}>"
