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
    def ord(self, c):
        if c.isupper():
            return ord(c) - 64
        if c.islower():
            return ord(c) - 96
        logger.debug(f"weird data ({c}) passed.")
        return 0    

class HasAlternates:

    def should_alternate(self, c):
        if c in self.alternates and getattr(self, c):
            return True
        else:
            return False
        
class HasLetterMap:
    
    def debug(self):
        logger.debug(f"{self.name} has {self.mapping=}")
        
    
    def letter_map(self, numbers):
        z1 = zip(ALPHABET, numbers)
        result = { k:v for (k,v) in z1}
        for c, i in zip(ALPHABET.lower(), numbers):
            result[c] = i
        return result
    
    
    def ord(self, c):
        try:
            return self.mapping[c]
        except KeyError:
            logger.debug(f"ignoring character {c}.")
            return 0    

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


@dataclass
class FrancisBacon(Cipher):
    """Case-sensitive cipher."""
    
    def ord(self, c):
        if c.isupper():
            return ord(c) - 38  
        if c.islower():
            return ord(c) - 96
        logger.debug(f"weird data ({c}) passed.")
        return 0    
    

@dataclass
class FrancBaconis(Ordinal):
    """Case-sensitive cipher."""
    
    def ord(self, c):
        parent = super().ord(c) * 2
        if c.isupper():
            return parent - 1
        if c.islower():
            return parent


@dataclass
class Jewish(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            1,2,3,4,5,6,7,8,9,
            600,10,20,30,40,50,60,70,80,90,
            100,200,700,900,300,400,500
            ])
        logger.debug(f"{self.mapping=}")



@dataclass
class EnglishExtended(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            1,2,3,4,5,6,7,8,9,
            10,20,30,40,50,60,70,80,90,
            100,200,300,400,500,600,700,800
            ])
        logger.debug(f"{self.mapping=}")

@dataclass
class Septenary(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            1,2,3,4,5,6,7,
            6,5,4,3,2,1,
            1,2,3,4,5,6,7,
            6,5,4,3,2,1,
            ])
        logger.debug(f"{self.mapping=}")
        
@dataclass
class Chaldean(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            1,2,3,4,5,8,
            3,5,
            1,1,2,3,4,5,7,8,
            1,2,3,4,
            6,6,6,
            5,1,7
            ])
        logger.debug(f"{self.mapping=}")                

@dataclass
class Satanic(Ordinal):
    
    # 1 -> 26
    # 2 -> 25
    # 3 -> 24
    # 24 -> 3
    # 25 -> 2
    # 26 -> 1
    
    def ord(self, c):
        _ = super().ord(c)
        r = 35 + _
        return r
    
    
@dataclass
class ALWKabbalah(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            1,20,13,6,25,18,11,4,23,16,9,
            2,21,14,7,26,19,12,5,24,17,10,
            3,22,15,8
            ])
        self.debug()  
        

@dataclass
class KFWKabbalah(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            9,20,13,6,17,
            2,19,12,23,16,1,18,5,
            22,15,26,11,4,21,8,25,10,3,14,7,24
            ])
        self.debug()  
        
@dataclass
class LCHKabbalah(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            5,20,2,23,13,12,11,3,0,7,17,1,21,24,10,4,16,14,15,9,25,22,8,6,18,19
            ])
        self.debug()  
        
        
@dataclass
class PrimeNumbers(Cipher,HasLetterMap):
    
    def __post_init__(self):
        self.mapping = self.letter_map([
            2, 3, 5, 7, 11,  13, 17, 19,  23, 
            29, 31, 37, 41, 43, 47, 53, 59,  61,
            67, 71, 73, 79,  83,  89,  97,  101 
            ])
        self.debug()  

if __name__ == '__main__':
    e1 = Ordinal()
    e2 = Reduced()
    e3 = ReverseOrdinal()
    e4 = ReverseReduced()
    e5 = Sumerian()
    e6 = ReverseSumerian()
    e7 = FrancisBacon()
    e8 = FrancBaconis()
    e9 = Jewish()
    e10 = EnglishExtended()
    e11 = Satanic()
    e12 = Septenary()
    e13 = Chaldean()
    e14 = ALWKabbalah()
    e15 = KFWKabbalah()
    e16 = LCHKabbalah()
    e17 = PrimeNumbers()

    
    _ = "ritual sacrifice"

#     print(e1.decode(_))
#     print(e2.decode(_))
#     print(e3.decode(_))
#     print(e4.decode(_))
    # print(e5.decode(_))
    #print(e14.decode(_))
    # print(e14.decode(_))
    print(e17.decode(_))
    
    
#     k = Reduced(k=True)
#     print(k.decode("kabbalah"))
#     
#     v = Reduced(v=True)
#     print(k.decode("value"))
#     
#     print(e2.decode("english"))
#     e2.s = True
#     print(e2.decode("english"))
    
    

    