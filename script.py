__author__ = 'pauloalmeida'

from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA, Selectors, Mutators, Consts
import textwrap
import csv
from service.mod11 import CheckDigit
data_set = []

def csv_reader(file_obj):
    with open(file_obj, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data_set.append("".join(row))

def eval_func(chromosome, debug=False):
    score = 0

    if isinstance(chromosome, str):
        parts = textwrap.wrap(chromosome, 35)
    else:
        parts = textwrap.wrap(''.join(map(str, chromosome.genomeList)), 35)
    for training_value in data_set:

        sum = 0
        for idx, part in enumerate(parts):
            training_value_number = int(training_value[idx])

            part_sum_op = int(part[0])
            part_sum_value = int(part[1:5],2)

            if part_sum_op == 1:
                sum += training_value_number + part_sum_value

            part_sub_op = int(part[5])
            part_sub_value = int(part[6:10],2)

            if part_sub_op == 1:
                sum += training_value_number- part_sub_value

            part_div_op = int(part[10])
            part_div_value = int(part[11:15],2)

            if part_div_op == 1 and part_div_value != 0:
                sum += training_value_number / part_div_value

            part_mul_op = int(part[15])
            part_mul_value = int(part[16:20],2)

            if part_mul_op == 1:
                sum += training_value_number * part_mul_value

            part_sqt_op = int(part[20])
            part_sqt_value = int(part[21:25],2)

            if part_sqt_op == 1 and part_sqt_value != 0:
                sum += training_value_number ** (1.0 / part_sqt_value)

            part_pow_op = int(part[25])
            part_pow_value = int(part[26:30],2)

            if part_pow_op == 1:
                sum += training_value_number ** part_pow_value

            part_mod_op = int(part[30])
            part_mod_value = int(part[31:35],2)

            if part_mod_op == 1 and part_mod_value != 0:
                sum += training_value_number % part_mod_value

        check_digit_service = CheckDigit(training_value[0:3])

        if debug:
            print sum, check_digit_service.sum_weighted_values()
        score += abs(sum - check_digit_service.sum_weighted_values())

    return score

def run_main():
    # Example of genome
    # (sum,0000,subtract,0000,divide,0000,multiply,0000,sqrt,0000,power,0000,mod,0000) * 3
    genome = G1DBinaryString.G1DBinaryString(105)
    genome.setParams(bestrawscore=0.00, rounddecimal=2)
    # The evaluator function (objective function)
    genome.evaluator.set(eval_func)
    genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.minimax = Consts.minimaxType["minimize"]
    ga.selector.set(Selectors.GTournamentSelector)
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
    ga.setMutationRate(0.8)
    ga.setGenerations(200000)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=20)

    # Best individual
    print ga.bestIndividual()

if __name__ == "__main__":
    csv_reader('dataset/training_examples.txt')
    # run_main()

    # First solution found
    # 000110111001100101000000100001001110010101000111001001100000011110001011000110000101000011000100000000010
    #
    # Breaking it
    # 1-) 00011011100110010100000010000100111
    # 2-) 00101010001110010011000000111100010
    # 3-) 11000110000101000011000100000000010
    #
    # Human readable
    # 1-) multiply * 4
    # 2-) divide 12 (if not zero) + multiply * 3
    # 3-) sum 8 + subtract 8
    #

    print eval_func('000110111001100101000000100001001110010101000111001001100000011110001011000110000101000011000100000000010', debug=True)