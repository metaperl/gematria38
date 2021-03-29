import plac
from gematria38 import mappings

@plac.flg('ordinal', 'Decode in ordinal.')
@plac.flg('reduced', 'Decode in reduced.')
@plac.flg('both', "Decode in ordinal and reduced.")
def main(ordinal=False, reduced=False, both=False):
    """A script to decode English."""
    if ordinal or both:
        o = mappings.EnglishOrdinal()
        

if __name__ == '__main__':
    plac.call(main)