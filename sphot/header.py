"""
The Header class transforms a list of columns to the list of labels.
"""
import pandas as pd
from itertools import product
from .columns import Columns


class Header(Columns):
    """Handle a header of a text file."""

    __suffixes = [
        "_ins",
        "_ierr",
        "_std",
        "_serr"
    ]

    def __init__(self, filename, columns):
        """
        Set a filename and a list of columns. Trigger internal helper
        methods to transform the list to labels from a header.

        Parameters
        ----------
        filename : str
            A name of the input text file.
        columns : list
            A list of columns. Each column should be represented
            by a string. The string must contain an integer or a range
            of integers. For example ['2', '4', '7:11', '15'].
        """
        super().__init__(columns)
        self.filename = filename
        self._check_column_numbers()
        self._read_header()
        self._get_passband_labels()
        self._get_passband_column_labels()

    def _check_column_numbers(self):
        """Check whether the number of column is proper."""
        n = len(self.__suffixes)
        total, rest = divmod(len(self.indexes), n)

        if (rest != 1) or not total:
            raise ValueError(
                "Number of columns must be equal ({}n + 1).".format(n))

    def _read_header(self):
        """Read a header file."""
        self.__header = pd.read_csv(
            self.filename, usecols=self.indexes, sep="\s+", nrows=0)

        return self.__header

    def _get_passband_labels(self):
        """Get unique passband labels from a file's header."""
        suff = self.__suffixes[0]
        self.__passband_labels = [
            name[:-len(suff)] for name in
            self.__header.filter(regex=suff).columns.to_list()
        ]

        return self.__passband_labels

    def _get_passband_column_labels(self):
        """Get all labels which represent passbands columns."""
        self.__column_labels = []

        for column_name in product(self.__passband_labels, self.__suffixes):
            column_name = "".join(column_name)

            if column_name not in self.__header.columns:
                raise ValueError(
                    "There is no '{}' in the file header.".format(column_name))

            self.__column_labels.append(column_name)

        self.__column_labels.insert(
            0, self._get_identifier_column_label(self.__column_labels))

        return self.__column_labels

    def _get_identifier_column_label(self, passband_column_names):
        """Get a label which represent a column with identifiers."""
        self.__identifier_label = (
            set(self.__header.columns) - set(passband_column_names))
        self.__identifier_label = str(*self.__identifier_label)

        return self.__identifier_label

    @property
    def labels(self):
        """
        Get labels of columns keeping the proper order of them.

        Returns
        -------
        list
            A list of labels. Each label is represented by a string.
        """
        return self.__column_labels

    @property
    def identifier(self):
        """
        Get a label of the column with the identifier.

        Returns
        -------
        str
            A string label.
        """
        return self.__identifier_label
