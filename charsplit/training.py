#!/usr/bin/env python
"""
Estimate compound word boundaries based ngram probabilities of n characters at word endings
Take as input a file with one word (a noun) per line
"""

import re
import argparse
import sys
from collections import defaultdict
import json


def parse_args():
    parser = argparse.ArgumentParser(description='Computes ngram probabilities')
    parser.add_argument('input_file', help='filename, one word per line')
    parser.add_argument('output_file', help='output file with probabilities')
    return parser.parse_args()


def main(input_file: str, output_file: str, max_words: int = 10000000, max_len: int = 20) -> None:
    """
    Calculate ngram probabilities at different positions
    :param input_file: List of words, one per line
    :param output_file: JSON file where ngram probabilities are stored
    :param max_words: Max. no. of words to analyse
    :param max_len: Max. ngram length
    :return: None
    """
    # Dicts for counting the ngrams
    end_ngrams = defaultdict(int)
    start_ngrams = defaultdict(int)
    in_ngrams = defaultdict(int)
    all_ngrams = defaultdict(int)

    # Gather counts
    print('Words analyzed of max.', str(max_words))
    c = 0   # Line counter

    for line in open(input_file, 'r'):
        line = line.strip().lower()

        if '-' in line:
            line = re.sub('.*-', '', line)  # Hyphen: take part following last hyphen

        line_middle = line[1:-1]

        for n in range(3, max_len+1):   # "Overcount" long words
        # for n in range(3, len(line)+1):   # Lower performance

            if n <= max_len:
                ngram = line[:n]      # start_grams: max_len 3-5
                start_ngrams[ngram] += 1
                all_ngrams[ngram] += 1

                ngram = line[-n:]     # end_grams: max_len 3-5
                end_ngrams[ngram] += 1
                all_ngrams[ngram] += 1

            for m in range(len(line_middle) - n + 1):   # in_grams: max_len 3-5
                ngram = line_middle[m:m+n]
                if not ngram == '':
                    in_ngrams[ngram] += 1
                    all_ngrams[ngram] += 1

        if c % 10000 == 0:
            sys.stderr.write('\r'+str(c))
            sys.stderr.flush()
        c += 1

        if c == max_words:
            break

    sys.stderr.write('\n')

    print('Calculating ngrams probabilities')
    start_ngrams = {k: v/all_ngrams[k] for k,v in start_ngrams.items() if v > 1}
    end_ngrams = {k: v/all_ngrams[k] for k,v in end_ngrams.items() if v > 1}
    in_ngrams = {k: v/all_ngrams[k] for k,v in in_ngrams.items() if v > 1}

    # Write dicts to file
    with open(output_file, "w") as f:
        json.dump({
            "prefix": start_ngrams,
            "infix": in_ngrams,
            "suffix": end_ngrams
        }, f)


if __name__ == "__main__":
    args = parse_args()
    main(args.input_file, args.output_file)