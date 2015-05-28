__author__ = 'pauloalmeida'

from service.mod11 import CheckDigit

if __name__ == '__main__':

    check_digit = CheckDigit('239')
    print check_digit.sum_weighted_values(debug=True)