"""
The Columns class handles a list of integers. These numbers are pointers
to indexes of columns of a text file.
"""
from re import search


class Columns:
    """Handle an argument of columns list."""

    def __init__(self, columns):
        """
        Set a list of columns.

        Parameters
        ----------
        columns : list
            A list of columns. Each column should be represented
            by a string. The string must contain an integer or a range
            of integers. For example ['2', '4', '7:11', '15'].
        """
        self.columns = columns
        self.indexes = self.indexes(columns)

    def indexes(self, columns):
        """
        Transform a list of columns to another form. For example:
        ['2', '4', '7:11', '15'] -> [1, 3, 6, 7, 8, 9, 10, 14]

        Parameters
        ----------
        columns : list
            A list of columns. Each column should be represented
            by a string. The string must contain an integer or a range
            of integers separated by a colon.

        Returns
        -------
        indexes : list
            A list of columns. Each column is represented by a single
            integer and the numbers of columns are transformed into indexes
            (shifting the numbers by -1).
        """
        indexes = []

        for column in self.columns:
            arg_type = self.column_type(column)

            if arg_type == "number":
                indexes.append(int(column) - 1)
            elif arg_type == "range":
                n, m = self.split_range(column)
                self.validate_range(n, m)
                indexes.extend([i - 1 for i in range(n, m + 1)])

        return indexes

    def column_type(self, column):
        """
        Check a type of a column. It could be a single integer or a range
        of integers. Raise an exception if the type is improper.

        Parameters
        ----------
        column : str
            A string which contains an integer or a range of integers.

        Returns
        -------
        str
            A string which represents the type of the column. Possible
            values are: 'number' or 'range'.
        """
        if search('^[0-9]{1,}$', column):
            return "number"
        elif search('^[0-9]{1,}:[0-9]{1,}$', column):
            return "range"
        else:
            raise ValueError("Invalid column argument {}".format(column))

    @staticmethod
    def split_range(column):
        """
        Get minimum and maximum values of a range.

        Parameters
        ----------
        column : str
            A string which represents a range as two values separated
            by a colon.

        Returns
        -------
        tuple
            Minimum and maximum values of the range.
        """
        start, end = map(int, column.split(":"))
        return start, end

    def validate_range(self, start, end):
        """
        Check whether a range defined by two values is increasing.
        Raise an exception if not.
        """
        if start >= end:
            column = str(start) + ":" + str(end)
            raise ValueError("Invalid column argument {}".format(column))
