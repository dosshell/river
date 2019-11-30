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

    def test_estimate(self):
        N = 100
        t = pd.date_range('2018-01-01', periods=N, freq='D').values
        z = np.array(range(0, N))
        h = s2.estimate_error(t, z, 0.5, np.timedelta64(1, 'D'))
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
