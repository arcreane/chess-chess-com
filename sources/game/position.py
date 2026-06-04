class Position :
    def __init__(self, column, row):
        self.column = column
        self.row = row
    def __str__(self):
        return f'{self.column}, {self.row}'


    def __eq__(self, other):
        return isinstance(other, Position) and self.column == other.column and self.row == other.row
    def __hash__(self):
        return hash((self.column, self.row))