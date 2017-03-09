from functools import wraps
from math import pi

def check_for_valid_args(function):
    @wraps(function)
    def inner(*args, **kwargs):
        try:
            args = [args[0]] + [float(arg) for arg in args[1:]]
            return function(*args)
        except ValueError:
            print 'Line ' + str(index + 2)  +' contains non-numerical values...'
            raise SystemExit(1)
    return inner
                
def deg_to_radians(function):
    @wraps(function)
    def convert(degree_measure):
        return function((pi / 180) * degree_measure)
    return convert
