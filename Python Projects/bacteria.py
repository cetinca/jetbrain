# write your program here
class Bacteria:
    def __init__(self):
        self.original_strand = ""
        self.complementary_strand = ""
        self.restriction_site = ""
        self.opposite = {"A": "T", "T": "A", "C": "G", "G": "C"}
        self.gfp = ""
        self.gfp_complementary = ""
        self.gfp_restriction_left = ""
        self.gfp_restriction_right = ""
        self.gfp_middle = ""
        self.gfp_complementary_middle = ""

    def create_complementary(self):
        for s in self.original_strand:
            self.complementary_strand += self.opposite[s]
        for s in self.gfp:
            self.gfp_complementary += self.opposite[s]

    def print_all(self):
        print(self.original_strand)
        print(self.complementary_strand)

    def cut_plasmid(self):
        index = self.original_strand.index(self.restriction_site) + 1
        self.original_strand = self.original_strand[:index] + " " + self.original_strand[index:]

    def cut_gfp(self):
        index_left = self.gfp.index(self.gfp_restriction_left) + 1
        index_right = self.gfp.rindex(self.gfp_restriction_right) + 1
        self.gfp_middle = self.gfp[index_left:index_right]

    def stitch(self):
        prefix, suffix = self.original_strand.split()
        self.original_strand = prefix + self.gfp_middle + suffix

    def read_file(self):
        file_name = input()
        with open(file_name, mode="r", encoding="utf-8") as file:
            self.original_strand = file.readline().strip()
            self.restriction_site = file.readline().strip()
            self.gfp = file.readline().strip()
            self.gfp_restriction_left, self.gfp_restriction_right = file.readline().strip().split()

    def start(self):
        self.read_file()
        self.cut_plasmid()
        self.cut_gfp()
        self.stitch()
        self.create_complementary()
        self.print_all()


def main():
    b = Bacteria()
    b.start()


if __name__ == "__main__":
    main()
