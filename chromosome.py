import random
import string

class Chromosome(object):
    def __init__(self, length):
        self.charset = string.ascii_letters.join([' ', ',', '.', '!', '?'])
        self.string = ''.join([random.choice(self.charset) for _ in range(length)])
        self.heuristic_value = 0

    def __str__(self):
        return f'Heuristic: {self.heuristic_value}, Text: {self.string}'
