class Alphabet:
  lang     = None
  alphabet = None

  def __init__(self, lang):
    self.lang = lang
    self.digits = '0123456789'
    if lang == 'en':
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if lang == 'en25':
        self.alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    if lang == 'ru33':
        self.alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    if lang == 'ru':
        self.alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    self.lowercase = self.alphabet.lower()
    self.len = len(self.alphabet)
    
  def get_pos(self, char):
    if not char in self.alphabet:
      return -1
    return self.alphabet.find(char)

  @staticmethod
  def mod(num, base):
    sign = 1 if num >= 0 else -1
    num = num % base
    if sign < 0:
      num +=  base
    return num % base

  def mod_pos(self, pos):
    return self.mod(pos, len(self.alphabet))

  def get_char(self, pos):
    return self.alphabet[self.mod_pos(pos)]

  def shift(self, char, shift):
    if not char in self.alphabet:
      return ''
    if str(shift) in self.alphabet:
      shift = self.get_pos(shift)
    result = self.get_char(self.get_pos(char) + int(shift))
    return result
