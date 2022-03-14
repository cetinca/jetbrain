example = ("""
# John Lennon
or ***John Winston Ono Lennon*** was one **great** of *The Beatles*.
Here are the songs he wrote I like the most:
* Imagine
* Norwegian Wood
* Come Together
* In My Life
* ~~Hey Jude~~ (that was *McCartney*)
""")


class Formatter:
    def __init__(self):
        self.entered = ""
        self.commands = ['!help', '!done']
        self.formatters = {'plain': self.plain, 'bold': self.bold, 'italic': self.italic, 'header': self.header,
                           'link': self.link, 'inline-code': self.inline_code, 'new-line': self.new_line,
                           "ordered-list": self.ordered_list, "unordered-list": self.unordered_list}
        self.content = []

    def plain(self):
        entered = input("Text:")
        self.content.append(entered)

    def bold(self):
        entered = input("Text:")
        last_item = self.content.pop()
        self.content.append(last_item + f"**{entered}**")

    def italic(self):
        entered = input("Text:")
        self.content.append(f"*{entered}*")

    def header(self):
        while True:
            level = int(input("Level:"))
            if not 1 <= level <= 6:
                print("The level should be within the range of 1 to 6")
            else:
                break
        entered = input("Text:")
        self.content.append(level * "#" + " " + entered + "\n")

    def link(self):
        label = input("Label:")
        entered = input("URL:")
        self.content.append(f"[{label}]({entered})")

    def inline_code(self):
        entered = input("Text:")
        last_item = self.content.pop()
        self.content.append(last_item + f"`{entered}`")

    def new_line(self):
        self.content.append("\n")

    def ordered_list(self):
        while True:
            rows = int(input("Number of rows:"))
            if not 0 < rows:
                print("The number of rows should be greater than zero")
            else:
                break
        temp = ""
        for i in range(1, rows + 1):
            entered = input("Text:")
            temp += f"{i}. {entered}\n"
        self.content.append(temp)

    def unordered_list(self):
        while True:
            rows = int(input("Number of rows:"))
            if not 0 < rows:
                print("The number of rows should be greater than zero")
            else:
                break
        temp = ""
        for _ in range(rows):
            entered = input("Text:")
            temp += f"* {entered}\n"
        self.content.append(temp)

    def write_file(self):
        with open("./output.md", "w", encoding="utf-8") as file:
            for c in self.content:
                file.write(f"{c}")

    def start(self):
        while True:
            print("Choose a formatter:", end="")
            entered = input()
            if entered == "!done":
                self.write_file()
                break
            elif entered == "!help":
                print("Available formatters:", *self.formatters.keys())
                print("Special commands:", *self.commands)
            elif entered in self.formatters.keys():
                self.formatters[entered]()
                for c in self.content:
                    print(c, end="\r")
            else:
                print("Unknown formatting type or command")


def main():
    f = Formatter()
    f.start()


if __name__ == "__main__":
    main()
