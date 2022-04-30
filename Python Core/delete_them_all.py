# write your code here
import os
import sys
import hashlib


class DuplicateFileHandler:
    def __init__(self, args=sys.argv):
        self.args = args
        self.file_format = ""
        self.sorting_option = ""
        self.sort = False
        self.files = {}
        self.duplicate_files = {}
        self.hashes = {}
        self.hash_sizes = {}
        self.duplicate_hashes = {}
        self.files_id = {}
        self.ids_to_delete = []

    @staticmethod
    def find_duplicates(start_file, end_file):
        length = len(start_file)
        keys = list(start_file.keys())
        values = list(start_file.values())
        for i in range(length):
            for j in range(i + 1, length):
                if values[i] == values[j]:
                    end_file.update({keys[i]: values[i]})
                    end_file.update({keys[j]: values[j]})

    @staticmethod
    def ask_to_continue(msg):
        while True:
            print(msg)
            user_input = input()
            if user_input == "yes":
                break
            elif user_input == "no":
                sys.exit()

    def get_directory(self):
        if len(self.args) == 1:
            print("Directory is not specified")
            sys.exit()

    def find_files(self):
        os.chdir(self.args[1])
        # os.chdir(self.args)
        full_path = os.getcwd()
        for root, dirs, files in os.walk(full_path, topdown=False):
            for name in files:
                file = os.path.join(root, name)
                size = os.path.getsize(file)
                ext = name.split(".")[-1]
                if self.file_format == "":
                    self.files.update({file: size})
                elif self.file_format == ext:
                    self.files.update({file: size})

    def get_file_format(self):
        print("Enter file format")
        self.file_format = input()
        while True:
            print("Size sorting options:")
            print("1. Descending")
            print("2. Ascending")
            self.sorting_option = input()
            if self.sorting_option not in ["1", "2"]:
                print("Wrong option")
            elif self.sorting_option == "1":
                self.sort = True
                return
            elif self.sorting_option == "2":
                self.sort = False
                return

    def print_duplicates(self):
        sorted_dict = dict(sorted(self.duplicate_files.items(), key=lambda x: x, reverse=self.sort))
        values_set = sorted(set(sorted_dict.values()), reverse=self.sort)
        for value in values_set:
            print(f"{value} bytes")
            for k, v in sorted_dict.items():
                if value == v:
                    print(k)

    def print_duplicate_hashes(self):
        self.hash_sizes = {v: self.duplicate_files[k] for k, v in self.duplicate_hashes.items()}
        sizes = list(set(self.hash_sizes.values()))
        sizes = sorted(sizes, reverse=self.sort)
        self.hash_sizes = dict(sorted(self.hash_sizes.items(), key=lambda x: x, reverse=self.sort))
        self.duplicate_hashes = dict(sorted(self.duplicate_hashes.items(), key=lambda x: x, reverse=self.sort))
        i = 1
        for s in sizes:
            print(f"{s} bytes")
            for _hash, size in self.hash_sizes.items():
                if s == size:
                    print(f"Hash: {_hash}")
                    for k, v in self.duplicate_hashes.items():
                        if _hash == v:
                            print(f"{i}. {k}")
                            self.files_id.update({i: k})
                            i += 1

    def calculate_hash(self):
        for k, v in self.duplicate_files.items():
            md5_hash = hashlib.md5()
            with open(k, "rb") as file:
                content = file.read()
                md5_hash.update(content)
                digest = md5_hash.hexdigest()
                self.hashes.update({k: digest})

    def get_file_ids(self):
        print("Enter file numbers to delete:")
        while True:
            test = []
            try:
                self.ids_to_delete = [int(i) for i in input().split(" ")]
            except:
                print("Wrong format")
                continue

            for i in self.ids_to_delete:
                if i not in self.files_id.keys():
                    print("Wrong format")
                    test.append(False)
                else:
                    test.append(True)
            if all(test): break

    def delete_files(self):
        size = 0
        for i in self.ids_to_delete:
            file = self.files_id[i]
            os.remove(file)
            size += self.duplicate_files[file]
        print(f"Total freed up space: {size} bytes")


def main():
    # test = "c:/temp"
    # d = DuplicateFileHandler(test)
    d = DuplicateFileHandler()  # create class
    d.get_directory()  # user input
    d.get_file_format()  # user input
    d.find_files()  # find all files in the root and sub directories
    d.find_duplicates(d.files, d.duplicate_files)  # finds duplicate files
    d.print_duplicates()  # prints duplicate files
    d.ask_to_continue("Check for duplicates?")  # user input, terminating program if "no"
    d.calculate_hash()  # calculates hash for files
    d.find_duplicates(d.hashes, d.duplicate_hashes)  # checks for duplicate hashes
    d.print_duplicate_hashes()
    d.ask_to_continue("Delete files?")  # user input, terminating program if "no"
    d.get_file_ids()
    d.delete_files()


if __name__ == "__main__":
    main()
