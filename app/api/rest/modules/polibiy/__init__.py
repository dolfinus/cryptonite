
import yaml
import os
from math import *
from ..alphabet import Alphabet

class Polibiy:

  def __init__(self, alphabet):
    self.alphabet = Alphabet(alphabet)
    self.base = ceil(sqrt(self.alphabet.len))
    self.digits = dict(zip(range(36), self.alphabet.digits+self.alphabet.lowercase))

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def int2base(self, x, base=10):
    if x < 0:
        sign = -1
    elif x == 0:
        return self.digits[0]
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(self.digits[int(x % base)])
        x = int(x / base)
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)

  def get_coord(self, char):
    pos = self.alphabet.get_pos(char)
    first = str(floor(pos / self.base) + 1)
    second = str(int(self.int2base(pos, self.base)) % 10 + 1)
    return first, second

  def get_char(self, coord):
    pos = int(str(int(coord) - 11), self.base)
    return self.alphabet.get_char(pos)

  def encrypt(self, text):
    horizontals = []
    verticals   = []
    result      = []
    for char in text:
      print(char)
      vertical, horizontal = self.get_coord(char)
      horizontals.append(horizontal)
      verticals.append(vertical)
    coords = horizontals + verticals
    for i in range(0, len(coords), 2):
      j = i + 1
      coord = coords[j]+coords[i]
      result.append(self.get_char(coord))
    return ''.join(result)

  def decrypt(self, text):
    firsts  = []
    seconds = []
    coords  = []
    result  = []
    for char in text:
      vertical, horizontal = self.get_coord(char)
      coords.append(horizontal)
      coords.append(vertical)
    firsts  = coords[:len(coords)//2]
    seconds = coords[(len(coords)+1)//2:]
    print(firsts, seconds)
    for i, x in enumerate(firsts):
      y = seconds[i]
      coord = y+x
      print(coord)
      result.append(self.get_char(coord))
    return ''.join(result)