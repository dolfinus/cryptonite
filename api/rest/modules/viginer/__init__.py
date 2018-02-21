
import yaml
import os

class Viginer:

  def __init__(self, alphabet):
    self.alphabet = alphabet

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text, password):
    passw = password + text
    result = [self.alphabet.shift(char, self.alphabet.get_pos(passw[i]    )) for i, char in enumerate(list(text))]
    return ''.join(result)

  def decrypt(self, text, password):
    result = [self.alphabet.shift(char, -self.alphabet.get_pos(password[i])) for i, char in enumerate(list(text))]
    return ''.join(result)