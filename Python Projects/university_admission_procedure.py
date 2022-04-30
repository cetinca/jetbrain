import csv


def read_list():
    with open("applicant_list_7.txt", newline="") as file:
        _applicants = list(csv.reader(file, delimiter=" "))
    for a in _applicants:
        for i in range(2, 7): a[i] = float(a[i])
        phi = a[2] / 2 + a[4] / 2  # physics + mathematics
        if phi < a[6]: phi = a[6]
        eng = a[4] / 2 + a[5] / 2  # computer + mathematics
        if eng < a[6]: eng = a[6]
        bio = a[2] / 2 + a[3] / 2  # chemistry + physics
        if bio < a[6]: bio = a[6]
        for i in range(2, 6):
            if a[i] < a[6]: a[i] = a[6]
        a.extend([phi, eng, bio, False])
    return _applicants


def get_user_input(_spots):
    spot = int(input())
    for d in _spots.keys():
        _spots[d] = spot
    return _spots


def sort_list(_department, _applicants, _indexes):
    index = _indexes[_department]
    _sorted_applicants = sorted(_applicants, key=lambda x: (-float(x[index]), x[0], x[1]), reverse=False)
    return _sorted_applicants, index


def set_applicants(_spots, _applicants, _final_list, indexes):
    for column in range(7, 10):
        for department, spot in _spots.items():
            _sorted_applicants, index = sort_list(department, _applicants, indexes)
            for applicant in _sorted_applicants:
                if _spots[department] == 0: break
                if department == applicant[column] and _spots[department] != 0 and applicant[-1] == False:
                    temp = _final_list[department]
                    temp.append([applicant[0], applicant[1], float(applicant[index])])
                    _final_list.update({department: temp})
                    _spots[department] = _spots[department] - 1
                    applicant[-1] = True
                    if _spots[department] == 0: break
    return _final_list


def print_final_list(_final_list):
    for department, applicants in _final_list.items():
        print(department)
        _sorted = sorted(applicants, key=lambda x: (-x[2], x[0], x[1]), reverse=False)
        for s in _sorted:
            print(f"{s[0]} {s[1]} {s[2]}")


def save_final_list(_final_list):
    for department, applicants in _final_list.items():
        with open(f"{department.lower()}.txt", "w") as file:
            _sorted = sorted(applicants, key=lambda x: (-x[2], x[0], x[1]), reverse=False)
            for s in _sorted:
                file.write(f"{s[0]} {s[1]} {s[2]}\n")


"physics and math for the Physics department (2, 4)"
"chemistry for the Chemistry department (3,)"
"math for the Mathematics department (4,)"
"computer science and math for the Engineering Department (4,5)"
"chemistry and physics for the Biotech department (2,3)"
"physics(2), chemistry(3), math(4), computer science(5)"

def main():
    spots = {"Biotech": 0, "Chemistry": 0, "Engineering": 0, "Mathematics": 0, "Physics": 0}
    indexes = {"Biotech": -2, "Chemistry": 3, "Engineering": -3, "Mathematics": 4, "Physics": -4}
    final_list = {"Biotech": [], "Chemistry": [], "Engineering": [], "Mathematics": [], "Physics": []}
    applicants = read_list()
    spots = get_user_input(spots)
    final_list = set_applicants(spots, applicants, final_list, indexes)
    print_final_list(final_list)
    save_final_list(final_list)


if __name__ == "__main__":
    main()
