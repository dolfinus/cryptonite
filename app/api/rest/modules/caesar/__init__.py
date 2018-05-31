
import yaml
import os
from ..alphabet import Alphabet

class Caesar:

  def __init__(self, alphabet, shift):
    self.alphabet = Alphabet(alphabet)
    self.shift    = int(shift)

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    print(text)
    return ''.join([self.alphabet.shift(char, self.shift) for char in text
           ])

  def decrypt(self, text):
    return ''.join([self.alphabet.shift(char, -self.shift) for char in text
           ])