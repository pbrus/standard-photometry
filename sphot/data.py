"""
The Data class reads columns from a text file. Each column is represented
by brightness in a specific passband. The class calculates differences
of consecutive passbands (colors) and filters such data.
"""
import numpy as np
import pandas as pd

from sphot.header import Header


class Data(Header):

    __min_error = 0.0001

    def __init__(self, filename, columns, null_marker=99.9999):
        """
        Set parameters to get data from a text file.

        Parameters
        ----------
        filename : str
            A name of the input text file.
        columns : list
            A list of columns. Each column should be represented
            by a string. The string must contain an integer or a range
            of integers. For example ['2', '4', '7:11', '15'].
        null_marker : float, int, NaN
            A value indicating that there is no measurement
            in the input file.
        """
        super().__init__(filename, columns)
        self.filename = filename
        self.__null_marker = null_marker
        self._read_data()
        self._handle_nulls()
        self._set_minimum_error()
        self._calculate_sets()

    def _read_data(self):
        """Read data from a file."""
        self.__dataframe = pd.read_csv(
            self.filename, sep=r'\s+', usecols=self.labels)

        return self.__dataframe

    def _handle_nulls(self):
        """Replace null markers by default NaN value."""
        self.__dataframe.mask(
            self.__dataframe == self.__null_marker, inplace=True)

    def _set_minimum_error(self):
        """Set a minimum value for errors to prevent division by zero."""
        self.__dataframe.mask(self.__dataframe < self.__min_error,
                              self.__min_error, inplace=True)

    def _xy_labels(self, standard, instrumental):
        """Generator for sets of column's labels."""
        for labels in zip(standard, instrumental, instrumental[1:]):
            yield labels

        yield standard[-1], instrumental[-2], instrumental[-1]

    def _column_name_generator(self, first_label, second_label):
        """Wrapper for column labels generator."""
        first_column_labels = self._get_specific_labels(first_label)
        second_column_labels = self._get_specific_labels(second_label)

        return self._xy_labels(first_column_labels, second_column_labels)

    def _calculate_sets(self):
        """Transform columns with passbands to proper sets."""
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
        """
        Get sets of data for each panel, i.e. differences of magnitudes
        on the X and Y axes.

        Returns
        -------
        list
            A list which contains DataFrame objects. Each object
            represents four columns:
            - instrumental_magnitude_i - instrumental_magnitude_j
            - errors of above difference
            - standard_magnitude_i - instrumental_magnitude_i
            - errors of above difference

            i and j are indexes. These objects don't contain rows with
            null_marker - see the __init__ method.
        """
        return self.__sets
