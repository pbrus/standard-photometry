"""
The Columns class handles a list of integers. These numbers
are pointers to indexes of columns of a text file.
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
        self.__columns = columns
        self._indexes()

    def _indexes(self):
        """
        Transform a list of columns to another form. For example:
        ['2', '4', '7:11', '15'] -> [1, 3, 6, 7, 8, 9, 10, 14]
        """
        self.__indexes = []

        for column in self.__columns:
            arg_type = self._column_type(column)

            if arg_type == "number":
                self.__indexes.append(int(column) - 1)
            elif arg_type == "range":
                n, m = self.split_range(column)
                self._validate_range(n, m)
                self.__indexes.extend([i - 1 for i in range(n, m + 1)])

        return self.__indexes

    def _column_type(self, column):
        """
        Check a type of a column. It could be a single integer or a range
        of integers. Raise an exception if the type is improper.
        """
        if search('^[0-9]{1,}$', column):
            return "number"
        elif search('^[0-9]{1,}:[0-9]{1,}$', column):
            return "range"
        else:
            raise ValueError(f'Invalid column argument {column}')

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

    def _validate_range(self, start, end):
        """
        Check whether a range defined by two values is increasing.
        Raise an exception if not.
        """
        if start >= end:
            column = str(start) + ":" + str(end)
            raise ValueError(f'Invalid column argument {column}')

    @property
    def indexes(self):
        """
        Get a list of indexes.

        Returns
        -------
        list
            A list of indexes represented by integers.
        """
        return self.__indexes
