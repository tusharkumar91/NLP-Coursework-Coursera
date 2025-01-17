import math, collections

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
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
            self.total += 1
        trigrams = [words[i:i+3] for i in xrange(len(words)-2)]
        for trigram in trigrams:
            self.trigramCounts[tuple(trigram)] += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    trigrams = [sentence[i:i+3] for i in xrange(len(sentence)-2)]
    for trigram in trigrams:
        count = self.trigramCounts[tuple(trigram)]
        if count > 0:
            score += math.log(count)
            score -= math.log(self.bigramCounts[tuple([trigram[0], trigram[1]])])
        else:
            count = self.bigramCounts[tuple([trigram[1], trigram[2]])]
            if count > 0:
                score += math.log(count)
                score -= math.log(self.unigramCounts[trigram[1]])
            else:
                score += math.log(self.unigramCounts[trigram[2]]+1)
                score -= math.log(self.total + len(self.unigramCounts))
    return score
