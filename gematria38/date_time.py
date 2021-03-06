import arrow
import dateparser


def arrow_from_date_item(date_item):
    if isinstance(date_item, arrow.arrow.Arrow):
        a = date_item
    elif isinstance(date_item, str):
        a = arrow.get(dateparser.parse(date_item))
    return a


def day_of_year(date_item):
    """Return day of year and arrow given a human-readable date string or arrow instance."""
    a = arrow_from_date_item(date_item)
    return a.format('DDDD'), a
    
def month_and_day_of(date_item):
    a = arrow_from_date_item(date_item)
    return (a.month, a.day), a

def month_day_as_integers(date_item):
    (month, day), _ = month_and_day_of(date_item)
    result1 = f"{month}{day}"
    result2 = f"{day}{month}"

    return [int(r) for r in (result1, result2)]

def remove_decimal_from(number):
    """"3.14 -> 314"""
    pass

def factors_of(number):
    """Return all factor of a number."""
    pass

# TODO: perfect numbers
# - nth perfect number... p.45 L&N

if __name__ == '__main__':
    date_str = "Feb 13, 2016"
    print(day_of_year(date_str))
    
    date_str = "April 7 2016"
    mandd, a = month_and_day_of(date_str)
    print(type(a))
    print(day_of_year(a))
    
    date_str = "Feb 11, 1929"
    print(month_day_as_integers(date_str))
    