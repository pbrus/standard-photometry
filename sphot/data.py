import pandas as pd
from .header import Header


class Data(Header):

    __min_error = 0.0001

    def __init__(self, filename, columns, null_marker=99.9999):
        super().__init__(filename, columns)
        self.filename = filename
        self.__null_marker = null_marker
        self._read_data()
        self._handle_nulls()
        self._set_minimum_error()

    def _read_data(self):
        self.__dataframe = pd.read_csv(
            self.filename, sep="\s+", usecols=self.labels)
        return self.__dataframe

    def _handle_nulls(self):
        self.__dataframe.mask(
            self.__dataframe == self.__null_marker, inplace=True)

    def _set_minimum_error(self):
        self.__dataframe.mask(self.__dataframe < self.__min_error,
            self.__min_error, inplace=True)
