class EnglishOrdinal:
    
    def ord(self, c):
        if c.isupper():
            return ord(c) - 64
        if c.islower():
            return ord(c) - 96
        raise Exception(f"weird data ({c}) passed.")


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

 