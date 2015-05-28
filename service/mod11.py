__author__ = 'pauloalmeida'

class CheckDigit(object):

    def __init__(self, number_str):
        self.number_str = number_str


    def sum_weighted_values(self, debug=False):
        size = len(self.number_str) + 1
        sum = 0
        for idx, val in enumerate(list(self.number_str)):
            val = int(val) * size
            if debug:
                print idx, val, size, val
            sum += val
            size -= 1
        return sum