from dataclasses import dataclass, field
from typing import List



@dataclass
class EnglishOrdinal:
    
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
        raise Exception(f"weird data ({c}) passed.")
    
    def decode(self, s):
        self.letters = s
        self.numbers = [self.ord(c) for c in self.letters]
             

@dataclass
class EnglishReduced(EnglishOrdinal):
    
    def ord(self, c):
        r = super().ord(c)
        if r <= 9:
            return r
        if r <= 18:
            return r - 9
        return r - 18
    # raise Exception(f"weird data ({c}) passed.") 
    
    
if __name__ == '__main__':
    test_data = 'ABZIabzi'
    e = EnglishOrdinal()
    for c in test_data:
        r = e.ord(c)
        print(f"{c=} -> {r=}.")
    
    e2 = EnglishReduced()
    for c in test_data:
        r = e2.ord(c)
        print(f"{c=} -> {r=}.")
    
    e2.decode("English")
    print(f"{e2}")
 