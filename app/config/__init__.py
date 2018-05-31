import os
import yaml

CONFIG_FILE = 'config.yml'
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = '{}/{}'.format(CURRENT_PATH, CONFIG_FILE)

def recursive_key_uppercase(dictionary):
    result = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            value = recursive_key_uppercase(value)
        result[key.upper()] = value
    return result

def load_config(path):
  result = {}
  env = os.environ.get('FLASK_ENV', 'development')
  result['ENVIRONMENT'] = env

  with open(path) as f:
      conf = yaml.load(f)['app']
        
  conf = recursive_key_uppercase(conf.get(env, conf))
  for key in conf.keys():
      if key == 'DB' and isinstance(conf[key],dict):
          result.update({'SQLALCHEMY_'+k:v for k,v in conf[key].items()})
      else:
          result[key] = conf[key]
  return result

config = load_config(CONFIG_PATH)