from config import config

if 'SQLALCHEMY_DATABASE_URI' in config:
    if config['SQLALCHEMY_DATABASE_URI'].startswith('fs://'):
        from storage.fs.user import Users
    else:
        from storage.db.user import Users
else:
    assert 'DB path is not set!'

UserSingletone = Users()