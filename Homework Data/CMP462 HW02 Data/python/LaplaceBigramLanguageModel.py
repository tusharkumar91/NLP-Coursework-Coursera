import math, collections

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
        words = [data.word for data in sentence.data]
        bigrams = [ bigram for bigram in zip(words[:-1], words[1:])]
        for bigram in bigrams:
            self.bigramCounts[bigram] = self.bigramCounts[bigram] + 1
            self.unigramCounts[bigram[0]] += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    bigrams = [ bigram for bigram in zip(sentence[:-1], sentence[1:])]
    for bigram in bigrams:
      count = self.bigramCounts[bigram]
      count = count if count > 0 else 0
      score += math.log(count+1)
      score -= math.log(self.unigramCounts[bigram[0]]+len(self.unigramCounts))
    return score
