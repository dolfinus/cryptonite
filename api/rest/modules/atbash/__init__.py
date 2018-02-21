import yaml
import os

class Atbash:

  def __init__(self, alphabet):
    self.alphabet = alphabet
  
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    return ''.join([
              self.alphabet.get_char(-self.alphabet.get_pos(char)) for char in text
           ])

  decrypt = encrypt