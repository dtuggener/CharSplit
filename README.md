# CharSplit - An *ngram*-based compound splitter for German

Splits a German compound into its body and head, e.g.
> Autobahnraststätte -> Autobahn - Raststätte

Implementation of the method decribed in the appendix of the thesis:

Tuggener, Don (2016). *Incremental Coreference Resolution for German.* University of Zurich, Faculty of Arts.

**TL;DR**: The method calculates probabilities of ngrams occurring at the beginning, end and in the middle of words and identifies the most likely position for a split.

The method achieves ~95% accuracy for head detection on the [Germanet compound test set](http://www.sfs.uni-tuebingen.de/lsd/compounds.shtml).

A model is provided, trained on 1 Mio. German nouns from Wikipedia.

### Usage ###
**Train** a new model:
```bash
training.py --input_file --output_file
```
from command line, where `input_file` contains one word (noun) per line.

**Compound splitting**

In python

```python
>> from charsplit import Splitter
>> splitter = Splitter()
>> splitter.split_compound("Autobahnraststätte")
```
returns a list of all possible splits, ranked by their score, e.g.
```
[[0.7945872450631273, 'Autobahn', 'Raststätte'], 
[-0.7143290887876655, 'Auto', 'Bahnraststätte'], 
[-1.1132332878581173, 'Autobahnrast', 'Stätte'], ...]
```


