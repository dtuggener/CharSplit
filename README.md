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
```
python char_split_train.py <your_train_file>
```
where `<your_train_file>` contains one word (noun) per line.

**Compound splitting**

From command line:
```
python char_split.py <word>
```
Which outputs all possible splits, ranked by their score, e.g.
```
python char_split.py Autobahnraststätte
0.84096566854	Autobahn	Raststätte
-0.54568851959	Auto	Bahnraststätte
-0.719082070993	Autobahnrast	Stätte
...
```


As a module:
```python
>>> import char_split
>>> char_split.split_compound('Autobahnraststätte')
[[0.7945872450631273, 'Autobahn', 'Raststätte'], [-0.7143290887876655, 'Auto', 'Bahnraststätte'], [-1.1132332878581173, 'Autobahnrast', 'Stätte'], [-1.4010051533086552, 'Aut', 'Obahnraststätte'], [-2.3447843979244944, 'Autobahnrasts', 'Tätte'], [-2.4761904761904763, 'Autobahnra', 'Ststätte'], [-2.4761904761904763, 'Autobahnr', 'Aststätte'], [-2.5733333333333333, 'Autob', 'Ahnraststätte'], [-2.604651162790698, 'Autobahnras', 'Tstätte'], [-2.7142857142857144, 'Autobah', 'Nraststätte'], [-2.730248306997743, 'Autobahnrastst', 'Ätte'], [-2.8033113109925973, 'Autobahnraststä', 'Tte'], [-3.0, 'Autoba', 'Hnraststätte']]
```
