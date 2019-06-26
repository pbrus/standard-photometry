import pandas as pd
from .columns import Columns


class Header(Columns):

    __suffixes = [
        "_ins",
        "_ierr",
        "_std",
        "_serr"
    ]

    def __init__(self, filename, columns):
        self.filename = filename
        super().__init__(columns)
        self.check_column_numbers()

    def check_column_numbers(self):
        total, rest = divmod(len(self.indexes), 4)

        if (rest != 1) or not total:
            raise ValueError("Invalid column amount.")
