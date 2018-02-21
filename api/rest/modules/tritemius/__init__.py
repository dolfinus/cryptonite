
import yaml
import os

class Tritemius:

  def __init__(self, alphabet):
    self.alphabet = alphabet

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text, shift):
    result = []
    for char in text:
      result.append(self.alphabet.shift(char, shift))
      ++shift
    return result

  def decrypt(self, text, shift):
    result = []
    for char in text:
      result.append(self.alphabet.shift(char, -shift))
      ++shift
    return result