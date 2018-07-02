import os
from base import *

ARTICLES_DIR = os.path.join(STORAGE_PATH, '/articles')

def get_list(raw=False):
    articles = {}
    files = walk_files(ARTICLES_DIR)
    for file in files:
        article = {
            'name': file.name
        }
        if raw:
            article['path'] = file.path
        parent = parent_folder(file.path)
        if parent == ARTICLES_DIR:
            article['categories'] = []
        else:
            article['categories'] = [file.parent]
        articles[get_id(file.name)] = article
    return articles

def is_exists(id):
    articles = get_list()
    return id in articles

def get(id, raw=False):
    articles = get_list(raw=True)
    if id in articles:
        article = articles[id]
        article['content'] = read_file(article.path)
        if not raw:
            del article['path']
        return article
    return None

def read(name):
    id      = get_id(name)
    article = get(id)
    if not article:
        return {'error': 'Article {} not found!'.format(id)}, 404
    return article, 200

def create(name, content, category=''):
    id = get_id(name)
    if is_exists(id):
        return {'error': 'Article with this name is already exists!'}, 400
    category_path = ARTICLES_DIR
    if category:
        category_path = create_category(category_path, category)
    path = os.path.join(category_path, '/', id)
    save(path, content)
    return None, 201

def update(name, content):
    id = get_id(name)
    article = get(id)
    if not article:
        return {'error': 'Article {} not found!'.format(id)}, 404
    save(article['path'], content)
    return None, 200

def delete(name):
    id = get_id(name)
    article = get(id)
    if not article:
        return {'error': 'Article {} not found!'.format(id)}, 404
    delete_file(article['path'])
    return None, 204

def save(path, content):
    write_file(path, content)

