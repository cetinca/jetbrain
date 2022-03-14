import os
import requests
import sys
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from colorama import init

init(autoreset=True)


class WebBrowser:

    def __init__(self):
        self.directory = sys.argv[1]
        # self.directory = "./test"
        self.user_input = ""
        self.file_name = ""
        self.stack = []
        self.prefix = "https://"
        self.len_prefix = len(self.prefix)
        self.tags = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"]  # tags from another student.

    def connect_url(self, url):
        try:
            r = requests.get(url)
        except TimeoutError:
            print("Incorrect URL")
            sys.exit()

        if r.status_code != 200:
            print(f"The URL returned {r.status_code}")
            sys.exit()
        else:
            content = r.content
            soup = BeautifulSoup(content, "html.parser")
            all_text_in_url = ""
            # for element in soup.find_all():
            for element in soup.find_all(self.tags):
                if element.name == "a":
                    # txt = self.remove_spaces(line.text)
                    txt = f"{Fore.BLUE}{element.text.strip()}"
                    all_text_in_url += txt
                else:
                    # txt = self.remove_spaces(line.text)
                    txt = f"{Fore.WHITE}{element.text.strip()}"
                    all_text_in_url += txt
            return all_text_in_url

    @staticmethod
    def remove_spaces(_text):
        new_text = ""
        for i in range(len(_text) - 1):
            if _text[i] != "\n" or (_text[i] == "\n" and _text[i + 1] != "\n"):
                new_text += _text[i]
        return new_text

    def create_dir(self):
        if not os.access(self.directory, os.F_OK):
            os.mkdir(self.directory)
        os.chdir(self.directory)

    def get_user_input(self):
        while True:
            self.user_input = input()
            if self.user_input == "exit":
                break
            elif self.user_input == "back":
                self.stack.pop() if self.stack != [] else ""
                print(self.stack[-1])
                continue
            elif self.check_cache():
                with open(self.user_input, "r") as file:
                    out = file.read()
                    self.stack.append(out)
                    print(out)
                    continue
            elif "." not in self.user_input:
                print("Error: Incorrect URL")
                continue
            else:
                if self.user_input[:self.len_prefix] != self.prefix:
                    url = "https://" + self.user_input
                    out = self.connect_url(url)
                    print(out)
                    self.stack.append(out)
                    self.create_file(url, out)
                    continue
        return

    def create_file(self, _url, _out):
        index = _url.rfind(".")
        self.file_name = _url[self.len_prefix:index]
        with open(self.file_name, "w", encoding="utf-8") as file:
            file.write(_out)

    def check_cache(self):
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if name == self.user_input:
                    return True


def main():
    w = WebBrowser()
    w.create_dir()
    w.get_user_input()


if __name__ == "__main__":
    main()
