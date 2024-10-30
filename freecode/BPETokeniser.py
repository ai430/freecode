import re
from collections import defaultdict, Counter


class BPETokeniser:
    # constructor
    def __init__(self, vocab_size):
        self.vocab_size = vocab_size
        self.bpe_codes = {}
        self.vocab = {}

    # Dictionary or Vocabular
    def get_vocab(self, corpus):
        vocab = defaultdict(int)
        for word in corpus:
            word = " ".join(list(word)) + " </w>"
            vocab[word] += 1
        return vocab

    # Get the frequency of each token
    def get_stats(self, vocab):
        pairs = defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += freq
        return pairs

    # Merge my tokens that are appearing the most
    def merge_vocab(self, pair, v_in):
        v_out = {}
        bigram = re.escape(" ".join(pair))
        p = re.compile(r"(?<!\S)" + bigram + r"(?!\S)")
        for word in v_in:
            w_out = p.sub("".join(pair), word)
            v_out[w_out] = v_in[word]
        return v_out

    # Function to build a vocabulary from the corpus
    def fit(self, corpus):
        self.vocab = self.get_vocab(corpus)

        for i in range(self.vocab_size - len(self.vocab)):
            pairs = self.get_stats(self.vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            self.vocab = self.merge_vocab(best, self.vocab)
            self.bpe_codes[best] = len(self.bpe_codes)

    # Encode which will convert a sequence of tokens in codes
    def encode(self, word):
        word = " ".join(list(word)) + " </w>"
        pairs = self.get_stats({word: 1})

        while pairs:
            bigram = max(pairs, key=pairs.get)
            if bigram not in self.bpe_codes:
                break
            word = self.merge_vocab(bigram, {word: 1})
            word = list(word.keys())[0]
            pairs = self.get_stats({word: 1})
        return word.split()

    # Decode which will convert the token back into human readable word
    def decode(self, tokens):
        word = "".join(tokens).replace("</w", "")
        return word


corpus = ["low", "lower", "lowest"]
tokeniser = BPETokeniser(vocab_size=50)
tokeniser.fit(corpus)

print(tokeniser.bpe_codes)
