
import yaml
import os

def phi(num):
  result = 0
  for i in range(1,num-1):
    if nod(num, i) == 1:
      ++result
  return result

def nod(a,b):
  while a != b:
    if a > b:
      a = a - b
    else:
      b = b - a
  return b

class RSA:

  def __init__(self, mod, e):
    self.mod = int(mod)
    self.e   = int(e)

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml', 'r') as cfg:
      return yaml.load(cfg)

  def inv(self):
    phi_ = phi(self.mod)
    for d in range(1, phi_):
      if (d * self.e) % phi_ == 1:
        return d

  def encrypt(self, nums, e=None):
    result = []
    if not e:
      e = self.e
    if isinstance(nums, str):
      if not nums.isdigit():
        nums = bytearray(nums, 'UTF-8')
    for num in nums:
      num = int(num)
      result.append(pow(num, e, self.mod))
    #if isinstance(nums, str):
    #  result = ''.join(map(chr, result))
    return result

  def decrypt(self, nums, d=None):
    if not d:
      d = self.inv()
    else:
      d = int(d)
    return self.encrypt(nums, d)