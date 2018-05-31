from flask import request, g
from api.rest.base import SecureResource, rest_resource, restricted
from storage import ArticleSingletone as _Articles

@rest_resource
class Articles(SecureResource):
    """ /api/articles """
    endpoints = ['/articles','/articles/']

    #@cached
    def get(self):
        if ('categorized' in request.args):
            allowed_categories = request.args.get('categories[]', [], dict) or request.args.get('categories', [], dict) or []
            return _Articles.get_list_categorized(allowed_categories)
        return [k for k in _Articles.get_list()]

    @restricted
    def post(self):
        if 'name' not in request.json:
            return {'error': 'Article name is empty!'}
        if 'content' not in request.json:
            return {'error': 'Article content is empty!'}

        content  = request.json['content' ].strip()
        name     = request.json['name'    ].strip()
        category = request.json['category'].strip() or None

        return _Articles.create(name=name, content=content, category=category)

@rest_resource
class Article(SecureResource):
    """ /api/articles/name """
    endpoints = ['/articles/<string:id>']

    #@cached
    def get(self, id):
        return _Articles.read(id=id)

    @restricted
    def put(self, id):
        if 'content' not in request.json:
            return {'error': 'Article content is empty!'}

        content  = request.json['content' ].strip()
        category = request.json['category'].strip() or None

        return _Articles.update(id=id, content=content, category=category)

    @restricted
    def delete(self, id):
        return _Articles.delete(id=id)