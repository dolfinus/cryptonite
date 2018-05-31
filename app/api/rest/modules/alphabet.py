class Alphabet:
  lang     = None
  alphabet = None

  def __init__(self, lang):
    self.lang = lang
    if lang == 'en':
        self.alphabet = 'ABCDEFGHIJKLMNOPRSTUVWXYZ'
    if lang == 'ru33':
        self.alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    if lang == 'ru':
        self.alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
  def get_pos(self, char):
    if not char in self.alphabet:
      return -1
    return self.alphabet.find(char)

  def mod_pos(self, pos):
    sign = 1 if pos >= 0 else -1
    pos = pos % len(self.alphabet)
    if sign < 0:
      pos -=  len(self.alphabet)

    return pos

  def get_char(self, pos):
    return self.alphabet[self.mod_pos(pos)]

  def shift(self, char, shift):
    print(char, shift)
    if not char in self.alphabet:
      return ''
    if str(shift) in self.alphabet:
      shift = self.get_pos(shift)
    result = self.get_char(self.get_pos(char) + int(shift))
    print(char, shift, result)
    return result
