import pandas as pd
from .header import Header


class Data(Header):

    def __init__(self, filename, columns, null_marker=99.9999):
        super().__init__(filename, columns)
        self.filename = filename
        self.__null_marker = null_marker

    def _read_data(self):
        self.__dataframe = pd.read_csv(
            self.filename, sep="\s+", usecols=self.labels)
        return self.__dataframe
