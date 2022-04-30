# Write your code here
# Write your code here
import nltk
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer
from itertools import islice
import random
import string


class TextGenerator:
    def __init__(self):
        self.path = input() or "../test/corpus.txt"
        self.text = ""
        self.tokens = []
        self.bigrams = None
        self.trigrams = None
        self.markov_model = {}
        self.unique_tokens = set()
        self.random_text = []

    def open_file(self):
        with open(self.path, mode="r", encoding="utf-8") as file:
            self.text = file.read()

    def tokenize(self):
        self.tokens = WhitespaceTokenizer().tokenize(self.text)
        self.bigrams = list(nltk.bigrams(self.tokens))
        self.trigrams = list(ngrams(self.tokens, 3))
        self.unique_tokens = set(self.tokens)

    def print_stats(self):
        # print("Corpus statistics")
        # print(f"All tokens: {len(self.tokens)}")
        # print(f"Unique tokens: {len(self.unique_tokens)}")
        print(f"Number fo bigrams: {len(self.bigrams)}")

    def create_markov_model(self):
        for head, tail in self.bigrams:
            tails = self.markov_model.setdefault(head, {})
            tails.setdefault(tail, 0)
            number = self.markov_model[head][tail]
            self.markov_model[head][tail] = number + 1

    def create_markov_model_2(self):
        for head, mid, tail in self.trigrams:
            self.markov_model.update({f"{head} {mid}": tail})

    def find_token(self):
        entered = input()
        if entered == "exit":
            return
        else:
            try:
                tails = self.markov_model[entered]
                tails = dict(sorted(tails.items(), key=lambda x: (-x[1], x[0])))
                print(f"Head: {entered}")
                for k, v in tails.items():
                    print(f'Tail: {k:12} Count: {v}')
                print()
                self.find_token()
            except KeyError:
                print(f"Head: {entered}")
                print("Key Error. The requested word is not in the model. Please input another word.")
                print()
                self.find_token()

    def generate_sentence(self):
        sentence = []
        while True:
            head, mid = random.choice(list(self.markov_model.keys())).split()
            if head.isupper() and head[-1] not in [p for p in string.punctuation] and mid not in [".", "!", "?"]:
                sentence.append(head)
                sentence.append(mid)
                break
            else:
                continue
        while len(sentence) < 10:
            followed = self.markov_model[f"{sentence[-2]} {sentence[-1]}"]
            sentence.append(followed)
            if followed[-1] in [".", "!", "?"]:
                break
            else:
                continue
        if len(sentence) >= 5 and sentence[-1][-1] in [".", "!", "?"]:
            return sentence
        else:
            self.generate_sentence()

    def generate_random_text(self):
        self.random_text = []
        while len(self.random_text) < 10:
            sentence = self.generate_sentence()
            if sentence:
                self.random_text.append(sentence)
            else:
                continue

    def start(self):
        self.open_file()
        self.tokenize()
        self.create_markov_model_2()
        self.generate_random_text()
        [print(*s, sep=" ") for s in self.random_text]


def main():
    t = TextGenerator()
    t.start()


if __name__ == "__main__":
    main()
