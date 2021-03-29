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

if __name__ == '__main__':
    date_str = "Feb 13, 2016"
    print(day_of_year(date_str))
    
    date_str = "April 7 2016"
    mandd, a = month_and_day_of(date_str)
    print(type(a))
    print(day_of_year(a))