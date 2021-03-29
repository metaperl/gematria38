from dataclasses import dataclass, field
from typing import List
from loguru import logger


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def reduce(r):
    if r <= 9:
        return r
    if r <= 18:
        return r - 9
    return r - 18

@dataclass
class Cipher:
    """A way of converting letters to numbers."""
    
    letters: List[str] = field(default_factory=list)
    numbers: List[int] = field(default_factory=list)
    
    @property
    def sum(self):
        return sum(self.numbers)
    
    def decode(self, s):
        self.letters = s
        self.numbers = [self.ord(c) for c in self.letters]
        return self
             

    def __str__(self):
        return f"""
    {self.__class__.__name__} Decoding of '{self.letters}' yields {self.numbers} summing to {self.sum}
    """
        

@dataclass
class Ordinal(Cipher):

    def ord(self, c):
        if c.isupper():
            return ord(c) - 64
        if c.islower():
            return ord(c) - 96
        logger.debug(f"weird data ({c}) passed.")
        return 0
    


@dataclass
class Reduced(Ordinal):
    
    def ord(self, c):
        r = super().ord(c)
        return reduce(r)
    
@dataclass
class ReverseOrdinal(Ordinal):
    
    # 1 -> 26
    # 2 -> 25
    # 3 -> 24
    # 24 -> 3
    # 25 -> 2
    # 26 -> 1
    
    def ord(self, c):
        _ = super().ord(c)
        r = 27 - _
        return r


@dataclass
class ReverseReduced(ReverseOrdinal):
    def ord(self, c):
        r = super().ord(c)
        return reduce(r)

    
if __name__ == '__main__':
    e1 = Ordinal()
    e2 = Reduced()
    e3 = ReverseOrdinal()
    e4 = ReverseReduced()

    print(e1.decode(ALPHABET))
    print(e2.decode(ALPHABET))
    print(e3.decode(ALPHABET))
    print(e4.decode(ALPHABET))
