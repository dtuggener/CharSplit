"""
Split German compound words
"""

from pathlib import Path
from typing import List, Tuple
import re
import sys
import json
import math

NGRAM_PATH = Path(__file__).parent / "ngram_probs.json"

with open(NGRAM_PATH) as f:
    ngram_probs = json.load(f)


def softmax(logits: List[float], temperature=1.0) -> List[float]:
    exp_logits = [math.exp(x / temperature) for x in logits]

    denom = sum(exp_logits)
    return [x / denom for x in exp_logits]


def weight_probs(inp: List[Tuple[float, int]]) -> float:
    """
    Weight probs using a softmax of ngram lengths
    i. e. longer ngrams contribute more to the score
    """
    probs, weights = zip(*inp)
    weights = softmax(weights, 4.0)  # temperature of 4 works well on GermaNet

    return sum(prob * weight for prob, weight in zip(probs, weights))


class Splitter:
    """
    Wrapper around the split_compound function
    """
    def split_compound(self, word: str) -> List[Tuple[float, str, str]]:
        """Return list of possible splits, best first.
        :param word: Word to be split
        :return: List of all splits
        """
        word = word.lower()

        # If there is a hyphen in the word, return part of the word behind the last hyphen
        if '-' in word:
            return [(1., re.search('(.*)-', word.title()).group(1), re.sub('.*-', '', word.title()))]

        scores = list() # Score for each possible split position

        # Iterate through characters, start at forth character, go to 3rd last
        for n in range(3, len(word)-2):
            pre_slice = word[:n]

            # Cut of Fugen-S
            if pre_slice.endswith('ts') or pre_slice.endswith('gs') or pre_slice.endswith('ks') \
                    or pre_slice.endswith('hls') or pre_slice.endswith('ns'):
                if len(word[:n-1]) > 2: pre_slice = word[:n-1]

            # Start, in, and end probabilities
            pre_slice_prob = list()
            in_slice_prob = list()
            start_slice_prob = list()

            # Extract all ngrams
            for k in range(len(word)+1, 2, -1):

                # Probability of first compound, given by its ending prob
                if k <= len(pre_slice):
                    end_ngram = pre_slice[-k:]  # Look backwards
                    pre_slice_prob.append((ngram_probs["suffix"].get(end_ngram, -1), len(end_ngram)))   # Punish unlikely pre_slice end_ngram

                # Probability of ngram in word, if high, split unlikely
                in_ngram = word[n:n+k]
                in_slice_prob.append(ngram_probs["infix"].get(in_ngram, 1)) # Favor ngrams not occurring within words

                # Probability of word starting
                if n + k <= len(word):
                    ngram = word[n:n+k]
                    # Cut Fugen-S
                    if ngram.endswith('ts') or ngram.endswith('gs') or ngram.endswith('ks') \
                            or ngram.endswith('hls') or ngram.endswith('ns'):
                        if len(ngram[:-1]) > 2:
                            ngram = ngram[:-1]

                    start_slice_prob.append((ngram_probs["prefix"].get(ngram, -1), len(ngram)))

            if not pre_slice_prob or not start_slice_prob:
                continue

            start_slice_prob = weight_probs(start_slice_prob)
            pre_slice_prob = weight_probs(pre_slice_prob)
            in_slice_prob = min(in_slice_prob)  # Lowest, punish splitting of good in_grams

            score = start_slice_prob - in_slice_prob + pre_slice_prob
            scores.append((score, word[:n].title(), word[n:].title()))

        scores.sort(reverse=True)

        if not scores:
            scores = [[0, word.title(), word.title()]]

        return sorted(scores, reverse = True)

    def germanet_evaluation(self,
                            germanet_file: str = 'split_compounds_from_GermaNet13.0.txt',
                            print_errors: bool = False) -> None:
        """
        Test on GermaNet compounds
        from http://www.sfs.uni-tuebingen.de/lsd/compounds.shtml
        """
        cases, correct = 0, 0

        for line in open(germanet_file,'r').readlines()[2:]:
            cases += 1
            sys.stderr.write('\r'+str(cases))
            sys.stderr.flush()
            line = line.strip().split('\t')

            if not len(line) == 3:
                continue   # A few corrupted lines

            split_result = self.split_compound(line[0])
            if split_result[0][2] == line[2]:
                correct += 1
            elif print_errors:
                print(line, split_result)

            if cases % 10000 == 0:
                print(' Accuracy (' + str(correct) + '/' + str(cases) + '): ', 100 * correct/cases)

        print(' Accuracy (' + str(correct) + '/' + str(cases) + '): ', 100 * correct/cases)


if __name__ == '__main__':

    splitter = Splitter()

    scores = splitter.split_compound('Autobahnraststätte')
    for score in scores:
        print(score)

    splitter.germanet_evaluation()