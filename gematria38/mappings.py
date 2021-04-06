from dataclasses import dataclass, field
from typing import List
from loguru import logger
from pickle import FALSE, TRUE


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
    
    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"""
    {self.name} Decoding of '{self.letters}' yields {self.numbers} summing to {self.sum}
    """
        

@dataclass
class Ordinal(Cipher):
    pass

class HasAlternates:

    def should_alternate(self, c):
        if c in self.alternates and getattr(self, c):
            return True
        else:
            return False

@dataclass
class Reduced(Ordinal,HasAlternates):
    
    k: bool = False
    s: bool = False
    v: bool = False
    
    
    def __post_init__(self):
        if self.k: 
            self.v = True
        if self.v:
            self.k = True
        self.alternates = {
            'k' : 11,
            's' : 10,
            'v' : 22
        }
    
    def ord(self, c):
        if self.should_alternate(c):
            return self.alternates[c]
        
        r = super().ord(c)
        return reduce(r)
    
    @property
    def name(self):
        return f"{self.__class__.__name__} ({self.k=}, {self.s=}, {self.v=})"



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
class ReverseReduced(ReverseOrdinal,HasAlternates):
    
    p: bool = False
    h: bool = False
    e: bool = False
    
    def __post_init__(self):
        if self.p: 
            self.e = True
        if self.e:
            self.p = True
        self.alternates = {
            'p' : 11,
            'h' : 10,
            'e' : 22
        }
    
    def ord(self, c):
        if c == 'p' and self.p:
            return self.alternates[c]
        if c == 'h' and self.h:
            return self.alternates[c]      
        if c == 'e' and self.e:
            return self.alternates[c]
    
        r = super().ord(c)
        return reduce(r)
    
    @property
    def name(self):
        return f"{self.__class__.__name__} ({self.p=}, {self.h=}, {self.e=})"

@dataclass
class Sumerian(Ordinal):
    
    # 1 -> 26
    # 2 -> 25
    # 3 -> 24
    # 24 -> 3
    # 25 -> 2
    # 26 -> 1
    
    def ord(self, c):
        _ = super().ord(c)
        r = 6 * _
        return r


@dataclass
class ReverseSumerian(ReverseOrdinal):
    
    p: bool = False
    h: bool = False
    e: bool = False
    
    def ord(self, c):

        r = super().ord(c)
        return 6 * r
    
    
if __name__ == '__main__':
    e1 = Ordinal()
    e2 = Reduced()
    e3 = ReverseOrdinal()
    e4 = ReverseReduced()
    e5 = Sumerian()
    e6 = ReverseSumerian()

    
    _ = "abcxyz"

#     print(e1.decode(_))
#     print(e2.decode(_))
#     print(e3.decode(_))
#     print(e4.decode(_))
    print(e5.decode(_))
    print(e6.decode(_))
    
#     k = Reduced(k=True)
#     print(k.decode("kabbalah"))
#     
#     v = Reduced(v=True)
#     print(k.decode("value"))
#     
#     print(e2.decode("english"))
#     e2.s = True
#     print(e2.decode("english"))
    
    

    