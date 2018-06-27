
import yaml
import os
from ..alphabet import Alphabet

class Enigma:

  def __init__(self, keys='ABC', rings='123', reflector='A', flip=''):
    self.alphabet = Alphabet('en')
    chars = self.alphabet.alphabet
    self.keys          = keys

    self.rotations     = []
    self.flips         = []

    self.rings         = []
    self.reflector     = []

    self.rings_inv     = []
    self.reflector_inv = []

    for num in rings:
      num = int(num)
      ring = self.get_ring(num)
      self.rings.append(self.maketrans(chars, ring))
      self.rings_inv.append(self.maketrans(ring, chars))
      self.rotations.append(self.get_rotations(num))

    refl  = self.get_reflector(str(reflector))
    self.reflector = self.maketrans(chars, refl)

    flips = self.get_flips(flip)
    if flips[0] and flips[1]:
      self.flips     = self.maketrans(flips[0], flips[1])

  def get_ring(self, no):
    if no:
      config = self.config()
      return config['rings'][no]

  def get_rotations(self, no):
    if no:
      config = self.config()
      return config['rotations'][no]

  def get_reflector(self, name):
    if name:
      config = self.config()
      return config['reflectors'][name]

  def get_flips(self, input_string):
    firsts  = ''
    seconds = ''
    for i in range(0, len(input_string), 2):
      j = i + 1
      first  = input_string[i]
      second = input_string[j]

      firsts  += first
      seconds += second
    return firsts+seconds, seconds+firsts

  def rotate(self, pos):
    for i in range(len(self.rings)-1, 0, -1):
        if self.alphabet.get_char(pos[i]) in self.rotations[i]:
          pos[i-1] += 1
    pos[-1] += 1

  @staticmethod
  def maketrans(from_, to_):
    return {char: to_[i] for i, char in enumerate(from_)}

  @staticmethod
  def translate(table, text):
    result = []
    for char in text:
      if char in table:
        result.append(table[char])
      else:
        result.append(char)
    return ''.join(result)

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, text):
    result = []
    pos    = [self.alphabet.get_pos(char) for char in self.keys]
    for char in text:
      self.rotate(pos)
      
      if self.flips:
        char = self.translate(self.flips, char)

      for i, ring in reversed(list(enumerate(self.rings))):
        k = pos[i]
        if i < len(self.rings)-1:
          k -= pos[i+1]
        char = self.alphabet.shift(char, k)
        char = self.translate(ring, char)

      char = self.translate(self.reflector, char)

      for i, ring in enumerate(self.rings):
        k = pos[i]
        if i < len(self.rings)-1:
          k -= pos[i+1]
        char = self.translate(self.rings_inv[i], char)
        char = self.alphabet.shift(char, -k)
      
      if self.flips:
        char = self.translate(self.flips, char)

      result.append(char)

    return ''.join(result)

  decrypt = encrypt 