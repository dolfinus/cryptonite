
import yaml
import os
from ..alphabet import Alphabet

class Bellaso:

  def __init__(self, alphabet, password):
    self.alphabet = Alphabet(alphabet)
    self.password = password

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    return ''.join([
              self.alphabet.shift(char, self.alphabet.get_pos(self.password[pos]))
              for pos, char in enumerate(list(text))
           ])

  def decrypt(self, text):
    return ''.join([
              self.alphabet.shift(char, -self.alphabet.get_pos(self.password[pos]))
              for pos, char in enumerate(list(text))
           ])