import yaml
import os
from ..alphabet import Alphabet

class Atbash:

  def __init__(self, alphabet):
    self.alphabet = Alphabet(alphabet)

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    return ''.join([
              self.alphabet.get_char(-self.alphabet.get_pos(char) - 1) for char in text
           ])

  decrypt = encrypt