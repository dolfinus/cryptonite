
import yaml
import os
from ..alphabet import Alphabet

class Viginer2:

  def __init__(self, alphabet, password):
    self.alphabet = Alphabet(alphabet)
    self.password = password

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    result = []
    for i, char in enumerate(list(text)):
      passw = self.password + ''.join(result)
      result.append(self.alphabet.shift(char, self.alphabet.get_pos(passw[i])))
    return ''.join(result)

  def decrypt(self, text,):
    passw = self.password + text
    result = []
    for i, char in enumerate(list(text)):
      res = self.alphabet.shift(char, -self.alphabet.get_pos(passw[i]))
      passw += res
      result.append(res)
    return ''.join(result)