from storage.common.base import Format
from storage.db import db, generate_id, DbModel, Model

class Article(db.Model, DbModel):
    __tablename__ = 'articles'
    id = db.Column(db.String(80), primary_key=True, default=generate_id)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    category_id  = db.Column(db.String(80), db.ForeignKey('article_categories.id'), index=True, nullable=True)
    content = db.Column(db.Text, unique=False, nullable=True)

    def __repr__(self):
        return '<Article %r>' % self.name

class ArticleCategory(db.Model, DbModel):
    __tablename__ = 'article_categories'
    id = db.Column(db.String(80), primary_key=True, default=generate_id)
    name  = db.Column(db.String(120), index=True, unique=True, nullable=False)
    articles = db.relationship("Article", backref="category", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return '<ArticleCategory %r>' % self.name

class Articles(Model):
    type     = Article
    ids      = ['id', 'name']
    hide     = ['category_id']
    filter   = ['id', 'name', '@category.name', 'content']
    category = ArticleCategory
