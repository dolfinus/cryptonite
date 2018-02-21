
import yaml
import os

class Caesar:

  def __init__(self, alphabet):
    self.alphabet = alphabet

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text, shift):
    return ''.join([self.alphabet.shift(char, shift) for char in text
           ])

  def decrypt(self, text, shift):
    return self.encrypt(text, -shift)