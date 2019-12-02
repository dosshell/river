import unittest
import pandas as pd
import numpy as np
import s2


class TestS2(unittest.TestCase):
    def test_cv_kf(self):
        N = 100
        t = pd.date_range('2018-01-01', periods=N, freq='D').values
        z = np.array(range(0, N))
        x_g00 = s2.cv_kf(t, z, 0.01)
        x_g10 = s2.cv_kf(t, z, 0.99)
        x_g05 = s2.cv_kf(t, z, 0.5)
        self.assertAlmostEqual(float(x_g00[-1, 1]), 1.0)
        self.assertAlmostEqual(float(x_g10[-1, 1]), 1.0)
        self.assertAlmostEqual(float(x_g05[-1, 1]), 1.0)

    def test_cv_kf_estimate(self):
        N = 100
        t = pd.date_range('2018-01-01', periods=N, freq='D').values
        z = np.array(range(0, N))
        z, x = s2.cv_kf_estimate(t, z, 0.5, np.timedelta64(1, 'D'))
        h = z - x
        rmse = np.sqrt((h**2).mean())
        self.assertAlmostEqual(float(rmse), 0.1264885296216132)
        self.assertEqual(float(h[0]), 1.0)
        self.assertEqual(float(h[50]), 0.0)
        self.assertAlmostEqual(float(h[-1]), 0.0)

    def test_interpolate(self):
        t1 = np.datetime64('2018-01-01', freq='D')
        t2 = np.datetime64('2018-01-03', freq='D')
        t_target = np.datetime64('2018-01-02', freq='D')
        y1 = 10
        y2 = 20
        y_target = s2.interpolate(t1, t2, y1, y2, t_target)
        self.assertAlmostEqual(y_target, 15)

    def test_globopt(self):
        def F1(x):
            return x**2 + 2 * x - 3
        minx11 = s2.globopt(F1, -5.0, 5.0, 11)
        self.assertAlmostEqual(minx11, -1.0)
        minx12 = s2.globopt(F1, 2, 10, 100)
        self.assertEqual(minx12, 2)

        def F2(x):
            return 1 / 7 * x**2 + 5 / 3 * x + 15 / 2
        minx21 = s2.globopt(F2, -10.0, 10.0, 1001)
        self.assertAlmostEqual(minx21, -5.84)

        minx22 = s2.globopt(F2, -10.0, 10.0, 11, 4)
        self.assertAlmostEqual(minx22, -5.84)

        minx23 = s2.globopt(F2, -10.0, 10.0, 11, 11)
        self.assertAlmostEqual(minx23, -35 / 6)

        minx24 = s2.globopt(F2, 10.0, 100.0, 11, 11)
        self.assertEqual(minx24, 10.0)

        minx25 = s2.globopt(F2, -100, -10, 11, 11)
        self.assertEqual(minx25, -10)
