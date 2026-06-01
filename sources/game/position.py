class Position :
    def __init__(self, column, row):
        self.column = column
        self.row = row
    def __str__(self):
        return f'{self.column}, {self.row}'