
import yaml
import math
import os

class Polibiy:

  def __init__(self, alphabet):
    self.alphabet = alphabet
    self.base = ceil(sqrt(self.alphabet.len))

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def dec_to_base(self, num, dd=False):
    if not 2 <= base <= 36:
        raise ValueError('The base number must be between 2 and 36.')
    if not dd:
        dd = dict(zip(range(36), list(string.digits+string.ascii_lowercase)))
    if num == 0: return ''
    num, rem = divmod(num, base)
    return self.dec_to_base(num, dd)+dd[rem]

  def encrypt(self, text):
    result = []
    for char in text:
      pos = self.alphabet.get_pos(char)
      first = floor(pos / self.base) + 1
      second = dec_to_base(pos) % 10 + 1
      result.append(first+second)
    return result

  def decrypt(self, nums):
    result = []
    for num in num:
      pos = int(str(int(num) - 11), self.base)
      res = self.alphabet.get_char(pos)
      result.append(res)
    return result