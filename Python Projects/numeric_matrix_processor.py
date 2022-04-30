import sys
import numpy as np


class Matrix:
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.matrix_one = []
        self.matrix_two = []
        self.matrix_three = []
        self.options = {"1": "Add matrices", "2": "Multiply matrix by a constant", "3": "Multiply matrices",
                        "4": "Transpose matrix", "5": "Calculate a determinant", "6": "Inverse matrix", "0": "Exit"}
        self.sequence = {"1": self.sum_sequence, "2": self.mul_constant_sequence, "3": self.mul_matrix_sequence,
                         "4": self.transpose_sequence, "5": self.determinant_sequence, "6": self.inverse_sequence}
        self.transpose_options = {"1": "Main diagonal", "2": "Side diagonal", "3": "Vertical lines",
                                  "4": "Horizontal line"}
        self.matrix_methods = {"1": self.transpose_matrix, "2": self.transpose_side, "3": self.transpose_vertical,
                               "4": self.transpose_horizontal, "5": self.determinant_matrix, "6": self.inverse_matrix}

    @staticmethod
    def sum_matrix(one, two):
        matrix = []
        for i in range(len(one)):
            row = []
            for j in range(len(one[0])):
                row.append(one[i][j] + two[i][j])
            matrix.append(row)
        return matrix

    @staticmethod
    def mul_constant(one, constant):
        matrix = []
        for i in range(len(one)):
            row = []
            for j in range(len(one[0])):
                row.append(one[i][j] * constant)
            matrix.append(row)
        return matrix

    @staticmethod
    def transpose_matrix(one):
        matrix = []
        for i in range(len(one[0])):
            row = []
            for j in range(len(one)):
                row.append(one[j][i])
            matrix.append(row)
        return matrix

    @staticmethod
    def transpose_side(one):
        matrix = []
        for i in range(-1, -len(one[0]) - 1, -1):
            row = []
            for j in range(-1, -len(one[0]) - 1, -1):
                row.append(one[j][i])
            matrix.append(row)
        return matrix

    @staticmethod
    def transpose_vertical(one):
        matrix = []
        for i in range(len(one[0])):
            row = []
            for j in range(-1, -len(one[0]) - 1, -1):
                row.append(one[i][j])
            matrix.append(row)
        return matrix

    @staticmethod
    def transpose_horizontal(one):
        matrix = []
        for i in range(-1, -len(one[0]) - 1, -1):
            row = []
            for j in range(len(one)):
                row.append(one[i][j])
            matrix.append(row)
        return matrix

    @staticmethod
    def determinant_matrix(one):
        det = np.linalg.det(one)
        return round(det, 2)

    @staticmethod
    def inverse_matrix(one):
        inv = np.linalg.inv(one)
        return inv

    def mul_matrix(self, one, two):
        two = self.transpose_matrix(two)
        matrix = []
        for i in range(len(one)):
            row = []
            for j in range(len(two)):
                row.append(sum(map(lambda x, y: x * y, one[i], two[j])))
            matrix.append(row)
        return matrix

    @staticmethod
    def print_result(matrix):
        print("The result is:")
        for row in matrix:
            print(*row, sep=" ", end="\n")

    def get_matrix(self):
        matrix = []
        for _ in range(self.rows):
            row = [int(i) if i.isdigit() else float(i) for i in input().split()]
            if len(row) != self.columns:
                print("The operation cannot be performed.")
            else:
                matrix.append(row)
        return matrix

    def get_size(self):
        try:
            self.rows, self.columns = (int(i) if i.isdigit() else None for i in input().split())
        except:
            print("The operation cannot be performed.")
            sys.exit()

    def sum_sequence(self):
        print("Enter size of first matrix:", end=" ")
        self.get_size()
        print("Enter first matrix:")
        self.matrix_one = self.get_matrix()
        print("Enter size of second matrix:", end=" ")
        self.get_size()
        print("Enter second matrix:")
        self.matrix_two = self.get_matrix()
        if len(self.matrix_one) == len(self.matrix_two) and len(self.matrix_one[0]) == len(self.matrix_two[0]):
            self.matrix_three = self.sum_matrix(self.matrix_one, self.matrix_two)
            self.print_result(self.matrix_three)
        else:
            print("The operation cannot be performed.")

    def mul_constant_sequence(self):
        print("Enter size of matrix:", end=" ")
        self.get_size()
        print("Enter matrix:")
        self.matrix_one = self.get_matrix()
        print("Enter constant:", end=" ")
        constant = int(input())
        self.matrix_three = self.mul_constant(self.matrix_one, constant)
        self.print_result(self.matrix_three)

    def mul_matrix_sequence(self):
        print("Enter size of first matrix:", end=" ")
        self.get_size()
        print("Enter first matrix:")
        self.matrix_one = self.get_matrix()
        print("Enter size of second matrix:", end=" ")
        self.get_size()
        print("Enter second matrix:")
        self.matrix_two = self.get_matrix()
        if len(self.matrix_one[0]) == len(self.matrix_two):
            self.matrix_three = self.mul_matrix(self.matrix_one, self.matrix_two)
            self.print_result(self.matrix_three)
        else:
            print("The operation cannot be performed.")

    def transpose_sequence(self):
        while True:
            for k, v in self.transpose_options.items():
                print(f"{k}. {v}")
            print("Your choice:", end=" ")
            option = input()
            if option not in self.transpose_options.keys():
                continue
            else:
                break
        print("Enter size of matrix:", end=" ")
        self.get_size()
        print("Enter matrix:")
        self.matrix_three = self.matrix_methods[option](self.get_matrix())
        self.print_result(self.matrix_three)

    def determinant_sequence(self):
        print("Enter matrix size:", end=" ")
        self.get_size()
        print("Enter matrix:")
        result = self.determinant_matrix(self.get_matrix())
        print(f"The result is:")
        print(result)

    def inverse_sequence(self):
        print("Enter matrix size:", end=" ")
        self.get_size()
        print("Enter matrix:")
        result = self.inverse_matrix(self.get_matrix())
        self.print_result(result)

    def start(self):
        while True:
            print()
            for k, v in self.options.items():
                print(f"{k}. {v}")
            print("Your choice:", end=" ")
            option = input()
            if option not in self.options.keys():
                continue
            elif option == "0":
                break
            else:
                self.sequence[option]()


def main():
    m = Matrix()
    m.start()


if __name__ == "__main__":
    main()
