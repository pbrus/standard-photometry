import numpy as np
import numpy.ma as ma
from math import sqrt
from scipy import odr


class PointsRegression:

    def __init__(self, points):
        self.points = points
        self._mask = np.ones(len(self.points), dtype=bool)
        self._line_parameters = self._initial_regression_parameters()

    def _initial_regression_parameters(self):
        result = self._odr_wrapper([0, 0])
        result = self._odr_wrapper(result.beta)

        return result.beta

    def update_regression_parameters(self):
        result = self._odr_wrapper(self._line_parameters)
        self._line_parameters = result.beta

    def _odr_wrapper(self, beta):
        result = odr.ODR(
            odr.Data(
                self.points.iloc[:, 0][self._mask],
                self.points.iloc[:, 2][self._mask],
                1./(self.points.iloc[:, 1][self._mask] ** 2),
                1./(self.points.iloc[:, 3][self._mask] ** 2)),
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
                self._line_parameters, point) ** 2
            for point in zip(
                self.points.iloc[:, 0][self._mask],
                self.points.iloc[:, 2][self._mask])
            ]

        return square_distances


        return result

    def weight_errors(self, error):
        return 1./sqrt(error[0]**2 + error[1]**2)

    def rms(self):


    def amount(self):
        return self.mask.sum()
