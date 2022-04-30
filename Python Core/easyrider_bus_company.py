import json
import re


class Bus:
    def __init__(self):
        self.user_input = ""
        self.content = ""
        self.stop_type = {"", "F", "O", "S"}
        self.check_dict = {"bus_id": self.check_bus_id, "stop_id": self.check_stop_id,
                           "stop_name": self.check_stop_name, "next_stop": self.check_stop_id,
                           "stop_type": self.check_stop_type, "a_time": self.check_a_time}
        self.error_list = ["bus_id", "stop_id", "stop_name", "next_stop", "stop_type", "a_time"]
        self.result = {}
        self.lines = {}
        self.start_stops = set()
        self.transfer_stops = set()
        self.finish_stops = set()
        self.time = {}

    @staticmethod
    def save_to_file(_txt):
        with open("log_file.txt", "a", encoding="utf-8") as file:
            file.write(_txt + "\n")

    def load_from_file(self):
        with open("test.json", "r", encoding="utf-8") as file:
            self.content = file.read()
        return self.content

    def add_error(self, _key, _value):
        try:
            temp = self.result[_key]
            temp += 1
        except KeyError as err:
            temp = 1
        finally:
            self.result[_key] = temp
            self.save_to_file(f"{_key}: {_value}")

    def check_bus_id(self, _key, _val):
        if not isinstance(_val, int):
            self.add_error(_key, _val)

    def check_stop_id(self, _key, _val):
        if not isinstance(_val, int):
            self.add_error(_key, _val)

    def check_stop_name(self, _key, _val):
        _val = str(_val)
        template = r"^([A-Z][a-z]+ )+(Avenue|Street|Road|Boulevard)$"
        match = re.match(template, _val)
        if not match:
            self.add_error(_key, _val)

    def check_next_stop(self, _key, _val):
        if not isinstance(_val, int):
            self.add_error(_key, _val)

    def check_stop_type(self, _key, _val):
        if _val not in self.stop_type:
            self.add_error(_key, _val)

    def check_a_time(self, _key, _val):
        regex = "^([01][0-9]|[2][0-3]):[0-5][0-9]$"
        test = re.search(regex, str(_val))
        if not bool(test):
            self.add_error(_key, _val)

    def print_errors(self):
        errors = sum(self.result.values())

        print(f"Type and required field validation: {errors} errors")
        for e in self.error_list:
            try:
                val = self.result[e]
            except:
                val = 0
            finally:
                print(f"{e}: {val}")

    def check_stops(self):
        for item in self.user_input:
            line = item["bus_id"]
            stop_type = item["stop_type"]

            if stop_type == "S":
                self.start_stops.add(item["stop_name"])
            elif stop_type == "F":
                self.finish_stops.add(item["stop_name"])

            try:
                temp = self.lines[line]
                temp.append(stop_type)
            except:
                temp = [stop_type]
            finally:
                self.lines.update({line: temp})

        for k, v in self.lines.items():  # valid lines has, one start, one finish stop.
            if v.count("S") != 1 or v.count("F") != 1:
                print(f"There is no start or end stop for the line: {k}.")
                return

        print(f"Start stops: {len(self.start_stops)} {sorted(self.start_stops)}")
        print(f"Transfer stops: {len(self.transfer_stops)} {sorted(self.transfer_stops)}")
        print(f"Finish stops: {len(self.finish_stops)} {sorted(self.finish_stops)}")

    def find_intersection(self):
        for item in self.user_input:
            line = item["bus_id"]
            stop_name = item["stop_name"]
            for _item in self.user_input:
                _line = _item["bus_id"]
                _stop_name = _item["stop_name"]
                if line != _line and stop_name == _stop_name:
                    self.transfer_stops.add(stop_name)

    def check_time(self):
        _time, _line = "", ""
        _test = []
        _lines = []
        print("Arrival time test:")
        for item in self.user_input:
            line = item["bus_id"]
            stop_name = item["stop_name"]
            time = item["a_time"]
            if _line not in _lines and _line == line and _time > time:
                print(f"bus_id line {line}: wrong time on station {stop_name}")
                _test.append(False)
                _lines.append(_line)
            else:
                _test.append(True)
            _time = time
            _line = line
        if all(_test):
            print("OK")

    def check_on_demand(self):
        test = set()
        for item in self.user_input:
            stop_name = item["stop_name"]
            stop_type = item["stop_type"]
            for _item in self.user_input:
                _stop_type = _item["stop_type"]
                _stop_name = _item["stop_name"]
                if stop_type == "O" and stop_type != _stop_type and stop_name == _stop_name:
                    test.add(stop_name)
                    self.add_error("stop_name", stop_name)

        if test:
            print(f"Wrong stop type: {sorted(test)}")
        else:
            print(f"OK")

    def start(self):
        self.user_input = input("user input: ") or self.load_from_file()
        self.user_input = json.loads(self.user_input)

        self.check_on_demand()


def main():
    b = Bus()
    b.start()


if __name__ == "__main__":
    main()
