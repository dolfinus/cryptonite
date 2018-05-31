
import yaml
import os
from ..alphabet import Alphabet

class Viginer:

  def __init__(self, alphabet, password):
    self.alphabet = Alphabet(alphabet)
    self.password = password

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    passw = self.password + text
    result = [self.alphabet.shift(char, self.alphabet.get_pos(passw[i]    )) for i, char in enumerate(list(text))]
    return ''.join(result)

  def decrypt(self, text):
    passw = self.password
    result = [self.alphabet.shift(char, -self.alphabet.get_pos(passw[i])) for i, char in enumerate(list(text))]
    return ''.join(result)