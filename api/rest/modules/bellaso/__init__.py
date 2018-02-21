
import yaml
import os

class Bellaso:

  def __init__(self, alphabet):
    self.alphabet = alphabet
    self.password = password

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text, password):
    return ''.join([
              self.alphabet.shift(char,password[num])
              for pos, char in enumerate(list(text))
           ])

  def decrypt(self, text, password):
    return ''.join([
              self.alphabet.shift(char,-password[pos])
              for pos, char in enumerate(list(text))
           ])