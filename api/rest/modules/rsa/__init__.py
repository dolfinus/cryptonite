
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

  def __init__(self, mod):
    print(mod)
    self.mod = int(mod)

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def inv(self, e):
    phi_ = phi(self.mod)
    for d in range(1, phi_):
      if (d * e) % phi_ == 1:
        return d

  def encrypt(self, nums, e):
    e = int(e)
    result = []
    for num in nums:
      result.append(pow(num, e, self.mod))
    return result

  def decrypt(self, nums, d=None, e=None):
    if e:
      d = self.inv(e)
    return self.encrypt(nums, d)