# write your code here
import re

pattern, text = input().split("|")


def compare(_pattern, _text, stack=None, letter=None):
    if '\\' in _pattern:
        p = _pattern.find("\\")
        letter = _pattern[p + 1]
        _pattern = _pattern.replace("\\"+letter, "_")
        _text = _text.replace(letter, "_")

    if "^" in _pattern and "$" in _pattern and ("+" in _pattern or "*" in _pattern):
        _pattern = _pattern[1:-1]
        p = _pattern.find("+") or _pattern.find("*")
        s = len(_pattern) - p - 1
        _text = _text[:p] + _text[-s:]
    elif "^" in _pattern:
        if ("*" or "+") in _pattern:
            _pattern = _pattern[1:]
            _text = _text[:_pattern.find("*")] or _text[:_pattern.find("+")]
        else:
            _pattern = _pattern[1:]
            _text = _text[:len(_pattern)]
    elif "$" in _pattern:
        if ("+" or "*") in _pattern:
            _pattern = _pattern[:-1]
            _text = _text
        else:
            _pattern = _pattern[:-1]
            _text = _text[-len(_pattern):]

    if _pattern == "" or _pattern == ".?" or _pattern == ".*" or (_pattern == ".+" and _text != ""):
        return True
    elif _pattern == "*" or _pattern == "+":
        if _text == "":
            return True

    if _text == "":
        return False
    if _pattern[0] == "." or _pattern[0] == _text[0]:
        return compare(_pattern[1:], _text[1:], _pattern[0], _text[0])
    elif pattern[0] == _text[0]:
        return compare(_pattern, _text[1:], _pattern[0], _text[0])
    elif _pattern[0] != _text[0] and _pattern[0] == "?" and len(stack) <= 1:
        return compare(_pattern[1:], _text, _pattern[0], _text[0])

    elif _pattern[0] == "*" and stack[-1] == _text[0]:
        return compare(_pattern, _text[1:], _pattern[0], _text[0])
    elif _pattern[0] == "*" and stack[-1] != _text[0]:
        return compare(_pattern[1:], _text, _pattern[0], _text[0])
    elif _pattern[0] == "+" and stack[-1] == _text[0]:
        return compare(_pattern, _text[1:], _pattern[0], _text[0])
    elif _pattern[0] == "+" and stack[-1] != _text[0]:
        if stack == letter or stack == ".":
            return compare(_pattern[1:], _text, _pattern[0], _text[0])
        else:
            return False
    elif "?" in _pattern or "*" in _pattern or "+" in _pattern:
        return compare(_pattern[1:], _text, _pattern[0], _text[0])
    elif len(pattern) <= len(_text):
        return compare(pattern, _text[1:], _pattern[0], _text[0])
    else:
        return False


print(compare(pattern, text))
