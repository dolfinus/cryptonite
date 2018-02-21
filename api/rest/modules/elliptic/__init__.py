
import yaml
import os

class EllipticPoint:
  def __init__(self, x, y, a, b, mod):
    self.x   = x
    self.y   = y

    self.a   = a
    self.b   = b
    self.mod = mod

  def __str__(self):
    return '({x},{y})'.format(x=self.x, y=self.y)

  def __repr__(self):
    return {'x': self.x, 'y': self.y}

  def _check_a_b_mod(self, other):
    if self.a   != other.a or \
       self.b   != other.b or \
       self.mod != other.mod:
       raise ValueError("""
a, b, c and mod of points should be equal!
 Found:
  {self.a} vs {other.a}
  {self.b} vs {other.b}
  {self.mod} vs {other.mod}
""".format(self=self, other=other))
    pass

  def _check_type(self, other):
    if type(other) != EllipticPoint:
       raise TypeError('Right operand is wrong type {}. Elliptic point is required!'.format(type(other)))
    pass

  def _reverse(self, x):
    for i in range(0, mod):
      if ((x*i) % self.mod) == 1:
        return i
    return x

  def __add__(self, other):
    self._check_type(other)
    self._check_a_b_mod(other)
    if self.x == other.x:
      _lambda = ((3*self.x*other.x + a) * self.reverse(2*self.y)) % mod
    else:
      _lambda = ((other.y-self.y) * self.reverse(other.x-self.x)) % mod
    x = (_lambda**2 - self.x - other.x) % self.mod
    y = (_lambda*(self.x - x) - self.y) % self.mod
    return EllipticPoint(x, y, self.a, self.b, self.mod)

  def __rmult__(self, k):
    if type(k) != int:
      raise TypeError('Right operand is wrong type {}. int is required!'.format(type(k)))
    result = EllipticPint(x, y, a, b, mod)
    for i in range(0, k-1):
      result += self
    return result

class Elliptic:

  def __init__(self, a, b, mod):
    self.a   = a
    self.b   = b
    self.mod = mod

  def config():
    with open(os.path.dirname(__file__)+'/config.yml','r') as cfg:
      return yaml.load(cfg)

  def encrypt(nums, p, q=None, d=None, rand=None):
    P = EllipticPoint(p['x'], p['y'], self.a, self.b, self.mod)
    if d:
      Q = P * d
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

  def decrypt(M, p, d):
    if len(p) != len(M):
      raise ValueError('Points vector and cipher text should be equal length!')
    result = []
    for i, num in enumerate(p):
      P = EllipticPoint(p['x'], p['y'], self.a, self.b, self.mod)
      Q = P * d

      res = (M[i] * Q.reverse(Q.x)) % mod
      result.append(res)
    return result