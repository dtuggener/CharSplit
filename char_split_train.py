# -*- coding: utf-8 -*- 

"""
Estimate compound word boundaries based ngram probabilities of n characters at word endings
Take as input a file with one word (a noun) per line (i.e. input.news2012.NN.txt)
autor: don.tuggener@gmail.com
"""

import pdb
import re
import sys
from collections import defaultdict

# Dicts for counting the ngrams
end_ngrams = defaultdict(int)
start_ngrams = defaultdict(int)
in_ngrams = defaultdict(int)
all_ngrams = defaultdict(int)

# Counters and limits
c = 0	# Line counter
max_words = 10000000	# Words to consider
max_len = 20	# Maximum ngram length

# Gather counts
sys.stderr.write('Words analyzed (of '+str(max_words)+'):\n')
for line in open(sys.argv[1],'r'):

    line = line.strip().decode('utf8').lower()    #TODO try saving Upper/Lowercasing?
    if '-' in line: line = re.sub('.*-', '', line)	# Hypen: take part following last hyphen
    #max_len=len(line)      
    line_middle = line[1:-1]

    for n in range(3, max_len+1):   # overcount long words
    #for n in range(3, len(line)+1):   # lower performance
  
        if n <= max_len:
        
            ngram = line[:n]      # start_grams: max_len 3-5
            start_ngrams[ngram] += 1.
            all_ngrams[ngram] += 1.
            #print 'start', ngram
          
            ngram = line[-n:]     # end_grams: max_len 3-5
            end_ngrams[ngram] += 1.
            all_ngrams[ngram] += 1.
            #print 'end', ngram
        
        for m in range(len(line_middle) - n + 1):   # in_grams: max_len 3-5
            ngram = line_middle[m:m+n]
            if not ngram == '':
                in_ngrams[ngram] += 1.
                all_ngrams[ngram] += 1.
                #print 'in', ngram
             
    if c % 10000 == 0:
        sys.stderr.write('\r'+str(c))
        sys.stderr.flush()
    c += 1
    if c == max_words:
        sys.stderr.write('\n')
        break
        
print >> sys.stderr, 'Calculating start ngrams probs...',
for n in start_ngrams: start_ngrams[n] = start_ngrams[n] / all_ngrams[n]
print >> sys.stderr, 'done.'    

print >> sys.stderr, 'Calculating end ngrams probs...',
for n in end_ngrams: end_ngrams[n] = end_ngrams[n] / all_ngrams[n]
print >> sys.stderr, 'done.'        

print >> sys.stderr, 'Calculating in ngrams probs...',
for n in in_ngrams: in_ngrams[n]=in_ngrams[n] / all_ngrams[n]    
print >> sys.stderr, 'done.' 

# Remove ngrams with weight 1, very rare, save space
print >> sys.stderr, '\nCleaning up: Removing ngrams with weight 1 ...'
start_ngrams = {k:v for k,v in start_ngrams.iteritems() if v!=1}
end_ngrams = {k:v for k,v in end_ngrams.iteritems() if v!=1}
in_ngrams = {k:v for k,v in in_ngrams.iteritems() if v!=1}
print >> sys.stderr, 'done.\n'

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
