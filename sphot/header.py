import pandas as pd
from itertools import product
from .columns import Columns


class Header(Columns):

    __suffixes = [
        "_ins",
        "_ierr",
        "_std",
        "_serr"
    ]

    def __init__(self, filename, columns):
        super().__init__(columns)
        self.filename = filename
        self._check_column_numbers()
        self._read_header()
        self._get_passband_labels()
        self._get_passband_column_labels()

    def _check_column_numbers(self):
        n = len(self.__suffixes)
        total, rest = divmod(len(self.indexes), n)

        if (rest != 1) or not total:
            raise ValueError(
                "Number of columns must be equal ({}n + 1).".format(n))

    def _read_header(self):
        self.__header = pd.read_csv(
            self.filename, usecols=self.indexes, sep="\s+", nrows=0)

        return self.__header

    def _get_passband_labels(self):
        suff = self.__suffixes[0]
        self.__passband_labels = [
            name[:-len(suff)] for name in
            self.__header.filter(regex=suff).columns.to_list()
        ]

        return self.__passband_labels

    def _get_passband_column_labels(self):
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
        self.__identifier_label = (
            set(self.__header.columns) - set(passband_column_names))
        self.__identifier_label = str(*self.__identifier_label)

        return self.__identifier_label
