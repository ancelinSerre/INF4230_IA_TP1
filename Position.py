class Position:

    def __init__(self, r=0, c=0):
        self.row = r
        self.column = c

    def __str__(self):
        return f"({self.row}, {self.column})"

    