"""
Estimate compound word boundaries based ngram probabilities of n characters at word endings
Take as input a file with one word (a noun) per line
"""

__author__ = 'don.tuggener@gmail.com'

import re
import sys
from collections import defaultdict

# Dicts for counting the ngrams
end_ngrams = defaultdict(int)
start_ngrams = defaultdict(int)
in_ngrams = defaultdict(int)
all_ngrams = defaultdict(int)

# Counters and limits
c = 0   # Line counter
max_words = 10000000    # Words to consider
max_len = 20    # Maximum ngram length

# Gather counts
print('Words analyzed of max.', str(max_words))
for line in open(sys.argv[1],'r'):

    line = line.strip().lower()
    if '-' in line: 
        line = re.sub('.*-', '', line)  # Hyphen: take part following last hyphen      
    line_middle = line[1:-1]

    for n in range(3, max_len+1):   # "Overcount" long words
    #for n in range(3, len(line)+1):   # Lower performance
  
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

# Write dicts to python file
with open('ngram_probs.py','w') as f:
    f.write('prefix=')
    f.write(str(dict(start_ngrams)))
    f.write('\n')
    f.write('infix=')
    f.write(str(dict(in_ngrams)))
    f.write('\n')    
    f.write('suffix=')
    f.write(str(dict(end_ngrams)))
    f.write('\n')
