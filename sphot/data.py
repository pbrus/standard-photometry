import pandas as pd
import numpy as np
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
        self._calculate_sets()

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

    def _xy_labels(self, standard, instrumental):
        for labels in zip(standard, instrumental, instrumental[1:]):
            yield labels

        yield standard[-1], instrumental[-2], instrumental[-1]

    def _column_name_generator(self, first_label, second_label):
        first_column_labels = self._get_specific_labels(first_label)
        second_column_labels = self._get_specific_labels(second_label)

        return self._xy_labels(first_column_labels, second_column_labels)

    def _calculate_sets(self):
        self.__sets = []
        passbands_generator = self._column_name_generator("_std", "_ins")
        errors_generator = self._column_name_generator("_serr", "_ierr")

        for passbands, errors in zip(passbands_generator, errors_generator):
            i_std, i_ins, j_ins = passbands
            i_serr, i_ierr, j_ierr = errors

            dataframe = pd.DataFrame(
                data=[
                    self.__dataframe[i_ins] - self.__dataframe[j_ins],
                    np.sqrt(np.square(self.__dataframe[i_ierr])
                            + np.square(self.__dataframe[j_ierr])),
                    self.__dataframe[i_std] - self.__dataframe[i_ins],
                    np.sqrt(np.square(self.__dataframe[i_serr])
                            + np.square(self.__dataframe[i_ierr]))
                ],
                index=[
                    i_ins + " - " + j_ins,
                    i_ierr + " + " + j_ierr,
                    i_std + " - " + i_ins,
                    i_serr + " + " + i_ierr
                ]
            )
            self.__sets.append(dataframe.T.dropna())

    @property
    def sets(self):
        return self.__sets
