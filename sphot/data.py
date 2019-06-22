import pandas as pd
from re import search


class Columns:
    """Handle an argument of columns list."""

    def __init__(self, columns):
        self.columns = columns
        self.indexes = self.indexes()

    def indexes(self):
        indexes = []

        for column in self.columns:
            arg_type = self.argument_type(column)

            if arg_type == "number":
                indexes.append(int(column) - 1)
            elif arg_type == "range":
                n, m = self.split_range(column)
                self.validate_range(n, m)
                indexes.extend([i - 1 for i in range(n, m + 1)])

        return indexes

    def argument_type(self, column):

        if search('^[0-9]{1,}$', column):
            return "number"
        elif search('^[0-9]{1,}:[0-9]{1,}$', column):
            return "range"
        else:
            raise ValueError("Invalid column argument {}".format(column))
            exit(1)

    @staticmethod
    def split_range(column):
        start, end = map(int, column.split(":"))
        return start, end

    def validate_range(self, start, end):
        if start >= end:
            column = str(start) + ":" + str(end)
            raise ValueError("Invalid column argument {}".format(column))
            exit(1)
