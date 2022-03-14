# write your code here
import re
import os
import argparse
import ast
from pprintast import pprintast


class StaticCodeAnalyzer:
    def __init__(self, _target):
        self.target = _target
        self.path = ""
        self.content = []
        self.problems = []
        self.stack = []
        self.files = []
        self.it_is_file = None
        self.line_no = 0
        self.tree = None

    def read_file_content(self):
        with open(self.path, mode="r", encoding="utf-8") as file:
            self.content = []
            data = list(file.readlines())
            for d in data:
                self.content.append(d)

    def check_class(self):
        path = self.path
        script = open(path).read()
        tree = ast.parse(script)
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and not isinstance(node.body[0], ast.Pass):
                class_name = node.name
                for n in node.body:
                    function_name = n.name
                    if isinstance(n, ast.FunctionDef):
                        self.check_function(n)
            elif isinstance(node, ast.FunctionDef):
                self.check_function(node)
            else:
                self.check_code_line(node)

    def check_function(self, _node):
        _function_name = _node.name
        no = _node.lineno
        for a in _node.args.args:  # node.args.args is list of arguments
            if not bool(re.match(r"^[_a-z0-9]+$", a.arg)):
                self.problems.append(f"{self.path}: Line {no}: S010 Argument name '{a.arg}' should be snake_case")
        if any([True for ls in _node.args.defaults if isinstance(ls, ast.List)]):
            self.problems.append(f"{self.path}: Line {no}: S012 The default argument value is mutable")
        if isinstance(_node.body[0], ast.Pass):
            pass

        elif _function_name == "__init__":
            for n in _node.body:
                line_no = n.lineno
                if isinstance(n, ast.Assign):
                    try:
                        variable_id = n.targets[0].value.id + "." + n.targets[0].attr
                        if not bool(re.match(r"^self\.[_a-z]+$", variable_id)):
                            self.problems.append(
                                f"{self.path}: Line {line_no}: S011 Variable name '{variable_id}' should be snake_case")
                    except:
                        variable_id = n.targets[0].id
                        self.problems.append(
                            f"{self.path}: Line {line_no}: S011 Variable name '{variable_id}' should be snake_case")

        else:
            for n in _node.body:
                line_no = n.lineno
                if isinstance(n, ast.Assign):
                    variable_id = n.targets[0].id
                    if not bool(re.match(r"^[_a-z]+$", variable_id)):
                        self.problems.append(f"{self.path}: Line {line_no}: S011 Variable name '{variable_id}' should be snake_case")

    def check_code_line(self, _node):
        if isinstance(_node, ast.Assign):
            line_no = _node.lineno
            variable_id = _node.targets[0].id
            if not bool(re.match(r"^[_a-z]+$|^[A-Z]+$", variable_id)):
                self.problems.append(f"{self.path}: Line {line_no}: S011 Variable name '{variable_id}' should be snake_case")

    def check_problems(self, _line_of_code, _line_no):
        prefix = _line_of_code[:8]

        # S001 long line check check
        if len(_line_of_code) > 79:
            self.problems.append(f"{self.path}: Line {_line_no}: S001 Too long")

        # S002 indentation check
        non_space_index = re.search(r"[^ ]", _line_of_code).span()[0]
        if non_space_index:
            if non_space_index % 4 != 0:
                self.problems.append(f"{self.path}: Line {_line_no}: S002 Indentation is not a multiple of four")

        # S003 semicolon check
        if ";" in _line_of_code:
            if bool(re.match(r"[^;]*#.*;$", _line_of_code)):
                pass
            elif bool(re.match(r"[^;]*'.*;+.*'[^;]*", _line_of_code)):
                pass
            else:
                self.problems.append(f"{self.path}: Line {_line_no}: S003 Unnecessary semicolon")

        # S004 space before inline comment check
        if "#" in _line_of_code:
            if _line_of_code[0] == "#":
                pass
            elif bool(re.match(r".*[ ][ ]#.*", _line_of_code)):
                pass
            else:
                self.problems.append(
                    f"{self.path}: Line {_line_no}: S004 At least two spaces required before inline comments")

        # S005 todo found
        if bool(re.match(r".*#.*[tT][oO][dD][oO]", _line_of_code)):
            self.problems.append(f"{self.path}: Line {_line_no}: S005 TODO found")

        # S006 more than two blank lines preceding in code line
        try:
            if _line_no == self.stack[-1] + 1 and _line_no == self.stack[-2] + 2 and _line_no == self.stack[-3] + 3:
                self.problems.append(
                    f"{self.path}: Line {_line_no}: S006 More than two blank lines used before this line")
        except:
            pass

        # S007
        if "class" in _line_of_code:
            if bool(re.match(r"^class[ ][ ]", _line_of_code)):
                self.problems.append(f"{self.path}: Line {_line_no}: S007 Too many spaces after 'class'")
        if "def" in _line_of_code:
            if bool(re.match(r"^[ ]*def[ ][ ]", _line_of_code)):
                self.problems.append(f"{self.path}: Line {_line_no}: S007 Too many spaces after 'def'")

        # S008
        if "class" in _line_of_code:
            match = re.match(r"^(class[ ]+)([A-z]+)", _line_of_code)
            if bool(match):
                class_name = match.group(2)
                if not bool(re.match(r"^([A-Z][a-z]+)([A-Z][a-z]+)*", class_name)):
                    self.problems.append(
                        f"{self.path}: Line {_line_no}: S008 Class name '{class_name}' should use CamelCase")

        # S009
        if "def" in _line_of_code:
            match = re.match(r"^(.*def[ ]+)([_A-z0-9]+)", _line_of_code)
            if bool(match):
                function_name = match.group(2)
                if bool(re.match(r"^__init__", function_name)):
                    pass
                elif not bool(re.match(r"^[_a-z0-9]+$", function_name)):
                    self.problems.append(
                        f"{self.path}: Line {_line_no}: S009 Function name '{function_name}' should use snake_case")

    def print_problems(self):
        print(*self.problems, sep="\n")

    def is_file(self):
        if os.path.isdir(self.target):
            self.it_is_file = False
        elif os.path.isfile(self.target):
            self.it_is_file = True

    def play(self):
        self.read_file_content()
        self.line_no = 0
        self.stack = []
        self.problems = []
        for line_of_code in self.content:
            self.line_no += 1
            if line_of_code == "\n" or re.match(r"[ ]*#", line_of_code):
                self.stack.append(self.line_no)
            self.check_problems(line_of_code, self.line_no)
        self.check_class()

    def get_paths(self):
        for root, dirs, files in os.walk(self.target, topdown=True):
            for name in files:
                path = os.path.join(root, name)
                self.files.append(path)

    def start(self):
        self.is_file()
        if self.it_is_file is True:
            self.path = self.target
            self.play()
            self.print_problems()
        elif self.it_is_file is False:
            self.get_paths()
            files = sorted(self.files, reverse=False)
            for file in files:
                if file[-3:] == ".py":
                    self.path = file
                    self.play()
                    self.print_problems()
                else:
                    # print(files)
                    pass
        elif self.it_is_file is None:
            print(f"Error, {self.path} file or directory not found")


def main():
    parser = argparse.ArgumentParser(description="Code Analyzer")
    parser.add_argument("path", help="directory or file", nargs="?", default="..\\test\\this_stage\\test_5.py")
    # parser.add_argument("path", help="directory or file", nargs="?", default="..\\test")
    args = parser.parse_args()
    s = StaticCodeAnalyzer(args.path)
    s.start()


if __name__ == "__main__":
    main()
