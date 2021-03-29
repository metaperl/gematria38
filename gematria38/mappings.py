from dataclasses import dataclass, field
from typing import List
from loguru import logger


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

@dataclass
class Ordinal:
    
    letters: List[str] = field(default_factory=list)
    numbers: List[int] = field(default_factory=list)
    
    @property
    def sum(self):
        return sum(self.numbers)

    def __str__(self):
        return f"""
    Decoding of '{self.letters}' yields {self.numbers} summing to {self.sum}
    """
    
    def ord(self, c):
        if c.isupper():
            return ord(c) - 64
        if c.islower():
            return ord(c) - 96
        logger.debug(f"weird data ({c}) passed.")
        return 0
    
    def decode(self, s):
        self.letters = s
        self.numbers = [self.ord(c) for c in self.letters]
        return self
             

@dataclass
class Reduced(Ordinal):
    
    def ord(self, c):
        r = super().ord(c)
        if r <= 9:
            return r
        if r <= 18:
            return r - 9
        return r - 18

    
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
        logger.debug(f"The character '{c}' {_=}, {r=}")
        if r <= 9:
            return r
        if r <= 18:
            return r - 9
        return r - 18


@dataclass
class ReverseReduced(ReverseOrdinal):
    def ord(self, c):
        r = super().ord(c)
        if r <= 9:
            return r
        if r <= 18:
            return r - 9
        return r - 18

    
if __name__ == '__main__':
    test_data = 'azlm'
    e = Ordinal()
    for c in test_data:
        r = e.ord(c)
        print(f"{c=} -> {r=}.")
    
    e2 = Reduced()
    for c in test_data:
        r = e2.ord(c)
        print(f"{c=} -> {r=}.")
    
    e3 = ReverseOrdinal()
    for c in test_data:
        r = e3.ord(c)
        print(f"{c=} -> {r=}.")
        
    e4 = ReverseReduced()
    for c in test_data:
        r = e4.ord(c)
        print(f"{c=} -> {r=}.")
            
#     print(e2.decode("Morals and Dogma"))
#  
#     print(e.decode("Washington, D.C."))
