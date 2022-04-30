import sys
import time
from bs4 import BeautifulSoup
import requests as requests
import argparse
import sys


class Translator:
    def __init__(self, source, target, word):
        self.URL = "https://context.reverso.net/translation/"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.languages = {"0": "All", "1": "Arabic", "2": "German", "3": "English", "4": "Spanish", "5": "French",
                          "6": "Hebrew", "7": "Japanese", "8": "Dutch", "9": "Polish", "10": "Portuguese",
                          "11": "Romanian", "12": "Russian", "13": "Turkish"}
        try:
            self.source = [k for k, v in self.languages.items() if v.lower() == source][0]
        except:
            print(f"Sorry, the program doesn't support {source}")
            sys.exit()
        try:
            self.target = [k for k, v in self.languages.items() if v.lower() == target][0]
        except:
            print(f"Sorry, the program doesn't support {target}")
            sys.exit()
        self.word = word


    def start(self):
        # self.get_input
        self.clear_file()
        if self.target == "0":
            for k, _ in self.languages.items():
                if k != "0" and k != self.source:
                    self.target = k
                    r = self.connect_url()
                    self.get_all_translation(r)
        else:
            r = self.connect_url()
            self.get_single_translation(r)

    def get_input(self):
        while True:
            print("Hello, you're welcome to the translator. Translator supports:")
            for k, v in self.languages.items(): print(k, v)
            print("Type the number of your language:")
            self.source = input()
            if self.source not in self.languages.keys():
                continue
            print("Type the number of a language you want to translate to or '0' to translate to all languages:")
            self.target = input()
            if self.target not in self.languages.keys():
                continue
            print("Type the word you want to translate:")
            self.word = input()
            return

    def connect_url(self):
        while True:
            try:
                full_url = self.URL + self.languages[self.source].lower() + "-" + self.languages[
                    self.target].lower() + "/" + self.word
                # print(full_url)
                r = requests.get(full_url, headers=self.headers)
            except TimeoutError:
                print("Something wrong with your internet connection")
            else:
                if r.status_code != 200:
                    print(f"Sorry, unable to find {self.word}")
                    time.sleep(3)
                    sys.exit()
                else:
                    break
        return r

    def get_single_translation(self, r):
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        print()
        print(f"{self.languages[self.target]} Translations:")
        self.write_file(f"{self.languages[self.target]} Translations:" + "\n")
        elements = soup.find_all("a", {"class": "dict"})
        translation = [e.text.strip() for e in elements]
        for text in translation:
            print(text)
            self.write_file(text + "\n")
        self.write_file("\n")
        print()
        print(f"{self.languages[self.target]} Examples:")
        self.write_file(f"{self.languages[self.target]} Examples:" + "\n")
        elements = soup.find("section", {"id": "examples-content"}).find_all("div", {"class": "src"})
        source = [e.text.strip() for e in elements]
        elements = soup.find("section", {"id": "examples-content"}).find_all("div", {"class": "trg"})
        target = [e.text.strip() for e in elements]
        for i in range(len(source)):
            print(source[i])
            print(target[i])
            self.write_file(source[i] + "\n")
            self.write_file(target[i] + "\n")

    def get_all_translation(self, r):
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        print()
        print(f"{self.languages[self.target]} Translations:")
        self.write_file(f"{self.languages[self.target]} Translations:" + "\n")
        elements = soup.find("a", {"class": "dict"})
        translation = [e.text.strip() for e in elements if len(e.text.strip()) > 0]
        for text in translation:
            print(text)
            self.write_file(text + "\n")
        self.write_file("\n")
        print()
        print(f"{self.languages[self.target]} Examples:")
        self.write_file(f"{self.languages[self.target]} Examples:" + "\n")
        elements = soup.find("section", {"id": "examples-content"}).find("div", {"class": "src"})
        source = [e.text.strip() for e in elements if len(e.text.strip()) > 0]
        elements = soup.find("section", {"id": "examples-content"}).find("div", {"class": "trg"})
        target = [e.text.strip() for e in elements if len(e.text.strip()) > 0]
        for i in range(len(source)):
            print(source[i])
            print(target[i])
            self.write_file(source[i] + "\n")
            self.write_file(target[i] + "\n")
        self.write_file("\n")

    def write_file(self, text):
        with open(f"{self.word}.txt", "a", encoding="utf-8") as file:
            file.write(text)

    def clear_file(self):
        with open(f"{self.word}.txt", "w", encoding="utf-8") as file:
            file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multilingual Translator")
    parser.add_argument("source", help="Source language")
    parser.add_argument("target", help="Target language")
    parser.add_argument("word", help="Word to translate")

    args = parser.parse_args()

    t = Translator(args.source, args.target, args.word)
    t.start()
