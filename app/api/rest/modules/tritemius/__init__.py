
import yaml
import os
from ..alphabet import Alphabet

class Tritemius:

  def __init__(self, alphabet, shift):
    self.alphabet = Alphabet(alphabet)
    self.shift    = int(shift)

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    result = []
    shift = self.shift
    for char in text:
      result.append(self.alphabet.shift(char, shift))
      ++shift
    return ''.join(result)

  def decrypt(self, text):
    result = []
    shift = self.shift
    for char in text:
      result.append(self.alphabet.shift(char, -shift))
      ++shift
    return ''.join(result)