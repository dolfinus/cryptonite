from config import config
from flask import Flask
app = Flask(__name__, static_url_path='')
app.config.update(config)

from api import api_bp
app.register_blueprint(api_bp)

@app.cli.command('createdb')
def initdb_command():
    print('Initializing a database...')
    from storage.db import db
    from storage.common.user import UserSingletone
    db.create_all()
    user = UserSingletone.get(name=config['ADMIN']['NAME'])
    if user is None:
        print('Create admin user...')
        UserSingletone.create(name=config['ADMIN']['NAME'], password=config['ADMIN']['PASSWORD'], is_admin=True)
    print('Done!')

if __name__ == '__main__':
    #one-thread debug run, use nginx + uswgi instead
    host, port = app.config['WEB']['HTTP-SOCKET'].split(':')
    app.run(host, int(port))
