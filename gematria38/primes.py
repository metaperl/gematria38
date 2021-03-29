from primelib import isprime, find_primes
from loguru import logger

def study(i):
    """Is i prime? What ordinal prime is it?"""
    if not isprime(i):
        return False, 0
    for nth, prime_number in enumerate(find_primes(1, 10000)):
        logger.debug(f"{prime_number=}")
        if prime_number == i:
            return True, nth
        

if __name__ == '__main__':
    print(study(97))