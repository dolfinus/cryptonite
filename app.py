import os
import yaml

from flask import Flask as BaseFlask, Config as BaseConfig
from api import api_rest, api_bp
from web import client_bp

class Config(BaseConfig):
    def from_yaml(self, config_file):
        env = os.environ.get('FLASK_ENV', 'development')
        self['ENVIRONMENT'] = env.lower()
        
        with open(config_file) as f:
            conf = yaml.load(f)['app']
        conf = conf.get(env, conf)
        for key in conf.keys():
            self[key.upper()] = conf[key]
                
class Flask(BaseFlask):   
    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)

app = Flask(__name__, static_url_path='')
app.register_blueprint(api_bp)
app.register_blueprint(client_bp)

app.config.from_yaml(os.path.join(app.root_path, 'config.yml'))
if __name__ == '__main__':
  #one-thread debug run, use nginx + uswgi instead
  host, port = app.config['WEB']['http-socket'].split(':')
  app.run(host=host, port=int(port))