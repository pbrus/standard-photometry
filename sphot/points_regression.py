import numpy as np
import numpy.ma as ma
from math import sqrt
from scipy import odr


class PointsRegression:

    def __init__(self, points):
        self.__points = points
        self.__mask = np.ones(len(self.__points), dtype=bool)
        self.__line_parameters = self._initial_regression_parameters()
        self.__rms = self._calculate_rms()

    def _initial_regression_parameters(self):
        result = self._odr_wrapper([0, 0])
        result = self._odr_wrapper(result.beta)

        return result.beta

    def update_regression_parameters(self):
        result = self._odr_wrapper(self.__line_parameters)
        self.__line_parameters = result.beta

    def _odr_wrapper(self, beta):
        result = odr.ODR(
            odr.Data(
                self.__points.iloc[:, 0][self.__mask],
                self.__points.iloc[:, 2][self.__mask],
                1./(self.__points.iloc[:, 1][self.__mask] ** 2),
                1./(self.__points.iloc[:, 3][self.__mask] ** 2)),
            odr.Model(PointsRegression.regression_function),
            beta0=beta).run()

        return result

    @staticmethod
    def regression_function(points, x):
        return points[0]*x + points[1]

    @staticmethod
    def line_point_distance(line_parameters, point_coordinates):
        A, B = line_parameters
        x, y = point_coordinates

        return abs(A*x - y + B)/sqrt(A ** 2 + 1)

    def _calculate_square_distances(self):
        square_distances = [
            PointsRegression.line_point_distance(
                self.__line_parameters, point) ** 2
            for point in zip(
                self.__points.iloc[:, 0][self.__mask],
                self.__points.iloc[:, 2][self.__mask])
            ]

        return square_distances

    def _calculate_weights(self):
        return 1./np.sqrt(self.__points.iloc[:, 1][self.__mask] ** 2
                          + self.__points.iloc[:, 3][self.__mask] ** 2)

    def _calculate_rms(self):
        square_distances = self._calculate_square_distances()
        weights = self._calculate_weights()
        weighted_distances = weights*square_distances
        self.__rms = sqrt(weighted_distances.sum()/weights.sum())

        return self.__rms

    @property
    def rms(self):
        return self._rms

    def sigma_clipping(self, sigma_factor=3.):
        rms = self._rms
        distances = self._calculate_square_distances()
        distances = [sqrt(dist) for dist in distances]

        for row, distance in enumerate(distances):
            if distance > sigma_factor*rms:
                self.__mask[row] = False
            else:
                self.__mask[row] = True

    @property
    def amount(self):
        return self.__mask.sum()

