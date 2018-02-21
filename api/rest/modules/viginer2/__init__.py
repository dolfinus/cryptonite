
import yaml
import os

class Viginer2:

  def __init__(self, alphabet):
    self.alphabet = alphabet

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text, password):
    result = []
    for i, char in enumerate(list(text)):
      passw = password + ''.join(result)
      result.append(self.alphabet.shift(char, self.alphabet.get_pos(passw[i])))
    return ''.join(result)

  def decrypt(self, text, password):
    passw = password + text
    result = []
    for i, char in enumerate(list(text)):
      res = self.alphabet.shift(char, -self.alphabet.get_pos(passw[i]))
      passw += res
      result.append(res)
    return ''.join(result)