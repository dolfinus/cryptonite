from config import config

if 'SQLALCHEMY_DATABASE_URI' in config:
    if config['SQLALCHEMY_DATABASE_URI'].startswith('fs://'):
        from storage.fs.article import Articles
    else:
        from storage.db.article import Articles
else:
    assert 'DB path is not set!'

ArticleSingletone = Articles()