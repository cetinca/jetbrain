# write your code here
import nltk
from argparse import ArgumentParser
import math
import re

class Score:
    def __init__(self, _path, _diff_words):
        self.text = ""
        self.sentences = {}
        self.words = []
        self.difficult_words = []
        self.len_chars = 0
        self.score = ""
        self.file_name = _path
        self.path_diff_words = _diff_words
        self.syllables = 0
        self.polysyllables = 0
        self.ages = []
        self.longman = []
        self.age_group = {1: "6", 2: "7", 3: "9", 4: "10", 5: "11", 6: "12", 7: "13", 8: "14",
                          9: "15", 10: "16", 11: "17", 12: "18", 13: "24", 14: "24"}
        self.methods = {"ari": self.ari, "fk": self.fk  , "smog": self.smog, "cl": self.cl, "dc": self.dc}

    def get_longman_3000(self):
        with open(self.path_diff_words, mode="r") as file:
            self.longman = file.read().split()
        for word in self.words:
            if word not in self.longman:
                self.difficult_words.append(word)

    def read_file(self):
        with open(self.file_name, mode="r", encoding="utf-8") as file:
            self.text = file.read()

    def tokenize(self):
        sentences = nltk.sent_tokenize(self.text)  # list of sentences
        for i in range(len(sentences)):
            tokenized_text = nltk.word_tokenize(sentences[i])  # tokens
            tokens = [t.lower() for t in tokenized_text if t not in [".", ",", "!", "?", "(", ")"]]  # removing puncts
            self.words.extend(tokens)
            self.sentences.update({i: tokens})  # creating dict with tokens in sentences
            # tagged = nltk.pos_tag(tokenized_text)
        self.len_chars = len(self.text.replace(" ", ""))

    def print_statistic(self):
        print(f"Words: {len(self.words)}")
        print(f"Difficult words: {len(self.difficult_words)}")
        print(f"Sentences: {len(self.sentences)}")
        print(f"Characters: {self.len_chars}")
        print(f"Syllables: {self.syllables}")
        print(f"Polysyllables: {self.polysyllables}")

    def count_syllables(self):
        self.syllables = 0
        self.polysyllables = 0
        for word in self.words:
            vowels = len(re.findall(r"[aeiou]", word))
            if word[-1] == "e":
                vowels -= 1
            if bool(re.findall(r"[aeiou]*[aeiou][aeiou]", word)):
                vowels -= 1
            if bool(re.match(r"[0-9]+", word)):
                vowels = 1
            self.syllables += 1 if vowels == 0 else vowels
            if vowels > 2:
                self.polysyllables += 1

    def calculate_score(self):
        print("Enter the score you want to calculate (ARI, FK, SMOG, CL, DC, all):")
        entered = input().split()
        entered = ["ari", "fk", "smog", "cl", "dc"] if entered == ["all"] else entered
        for e in entered:
            self.methods[e.lower()]()

    def ari(self):
        self.score = 4.71 * (self.len_chars / len(self.words)) + 0.5 * (len(self.words) / len(self.sentences)) - 21.43
        self.score = 14 if self.score > 14 else self.score
        age_group = self.age_group[int(math.ceil(self.score))]
        self.ages.append(int(age_group))
        print(f"Automated Readability Index: {int(math.ceil(self.score))} (about {age_group} year olds).")

    def fk(self):
        self.score = 0.39 * (len(self.words) / len(self.sentences)) + 11.8 * (self.syllables / len(self.words)) - 15.59
        self.score = 14 if self.score > 14 else self.score
        age_group = self.age_group[int(math.ceil(self.score))]
        self.ages.append(int(age_group))
        print(f"Flesch–Kincaid readability tests: {int(math.ceil(self.score))} (about {age_group} year olds).")

    def smog(self):
        self.score = 1.043 * (self.polysyllables * 30 / len(self.sentences)) ** 0.5 + 3.1291
        self.score = 14 if self.score > 14 else self.score
        age_group = self.age_group[int(math.ceil(self.score))]
        self.ages.append(int(age_group))
        print(f"Simple Measure of Gobbledygook: {int(math.ceil(self.score))} (about {age_group} year olds).")

    def cl(self):
        self.score = 0.0588 * (100 * self.len_chars / len(self.words)) - 0.296 * (
                100 * len(self.sentences) / len(self.words)) - 15.8
        self.score = 14 if self.score > 14 else self.score
        age_group = self.age_group[int(math.ceil(self.score))]
        self.ages.append(int(age_group))
        print(f"Coleman–Liau index: {int(math.ceil(self.score))} (about {age_group} year olds).")

    def dc(self):
        self.score = 0.1579 * len(self.difficult_words) / len(self.words) * 100 + 0.0496 * len(self.words) / len(
            self.sentences)
        if len(self.difficult_words) / len(self.words) >= 0.05:
            self.score = self.score + 3.6365
        if self.score <= 4.9:
            age_group = 10
        elif self.score <= 5.9:
            age_group = 12
        elif self.score <= 6.9:
            age_group = 14
        elif self.score <= 7.9:
            age_group = 16
        elif self.score <= 8.9:
            age_group = 18
        else:
            age_group = 24
        self.ages.append(int(age_group))
        print(f"Dale-Chall score: {round(self.score, 2)} (about {age_group} year olds).")

    def start(self):
        self.read_file()
        self.tokenize()
        self.count_syllables()
        self.get_longman_3000()
        self.print_statistic()
        self.calculate_score()
        average_age = sum(self.ages) / len(self.ages)
        print()
        print(f"This text should be understood in average by {round(average_age, 1)} year olds.")


def main():
    parser = ArgumentParser(description="Readability Score")
    parser.add_argument("--infile", help="file to check", default="test.txt")
    parser.add_argument("--words", help="difficult words", default="my_words.txt")
    args = parser.parse_args()
    s = Score(args.infile, args.words)
    s.start()


if __name__ == "__main__":
    main()
