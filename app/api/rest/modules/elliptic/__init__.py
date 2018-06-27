
import yaml
import os
from ..point import EllipticPoint
class Elliptic:
  def __init__(self, a, b, mod, p, d=None):
    self.a   = a
    self.b   = b
    self.mod = mod
    self.p   = p
    self.d   = d

  @staticmethod
  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(self, nums, q=None, rand=None):
    P = EllipticPoint(self.p['x'], self.p['y'], self.a, self.b, self.mod)
    if self.d:
      Q = P * self.d
    else:
      Q = EllipticPoint(q['x'], q['y'], self.a, self.b, self.mod)
    if rand and len(rand) != len(nums):
      raise ValueError('Random vector and input text should be equal length!')
    P_vector = []
    M_vector = []
    for i, num in enumerate(nums):
      if rand:
        k = rand[i]
      else:
        k = os.urandom()
      Pk = P * k
      Qk = Q * k

      P_vector.append(Pk)
      M_vector.append((num * Qk.x) % Qk.mod)
    return P_vector, M_vector

  def decrypt(self, M):
    if len(self.p) != len(M):
      raise ValueError('Points vector and cipher text should be equal length!')
    result = []
    for i, num in enumerate(self.p):
      P = EllipticPoint(self.p['x'], self.p['y'], self.a, self.b, self.mod)
      Q = P * self.d

      res = (M[i] * Q.reverse(Q.x)) % self.mod
      result.append(res)
    return result

  def sign(self, nums, q=None, rand=None):
    P = EllipticPoint(self.p['x'], self.p['y'], self.a, self.b, self.mod)
    if self.d:
      Q = P * self.d
    else:
      Q = EllipticPoint(q['x'], q['y'], self.a, self.b, self.mod)
    if rand and len(rand) != len(nums):
      raise ValueError('Random vector and input text should be equal length!')
    P_vector = []
    M_vector = []
    for i, num in enumerate(nums):
      if rand:
        k = rand[i]
      else:
        k = os.urandom()
      Pk = P * k
      Qk = Q * k

      P_vector.append(Pk)
      M_vector.append((num * Qk.x) % Qk.mod)
    return P_vector, M_vector

  def check(self, M):
    if len(self.p) != len(M):
      raise ValueError('Points vector and cipher text should be equal length!')
    result = []
    for i, num in enumerate(self.p):
      P = EllipticPoint(self.p['x'], self.p['y'], self.a, self.b, self.mod)
      Q = P * self.d

      res = (M[i] * Q.reverse(Q.x)) % self.mod
      result.append(res)
    return result