# Part-Of-Speech-Tagger-for-Catalan

Built a Hidden Markov Model part-of-speech tagger for Catalan language (in Python) which assigns part-of-speech tags to the test data.
The training data provided to the tagger is tokenized and tagged while the test data will be just tokenized, and the tagger will allocate the tags to each word.
The tagger implements Viterbi algorithm and uses add-one smoothing on the transition probabilities and no smoothing on the emission probabilities; for unknown tokens in the test data it will ignore the emission probabilities and use the transition probabilities alone.

The performance of the tagger was calculated on how well it performs on unseen test data compared to the performance of a reference tagger.

Corpus:
A file with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
A file with untagged development data, with words separated by spaces and each sentence on a new line.
A file with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.


hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data.
