import unittest
import pandas as pd
import numpy as np
import s2


class TestS2(unittest.TestCase):
    def test_cv_kf(self):
        N = 100
        t = pd.date_range('2018-01-01', periods=N, freq='D')
        v = np.array(range(0, N))
        x_g00 = s2.cv_kf(t.values, v, 0.01)
        x_g10 = s2.cv_kf(t.values, v, 0.99)
        x_g05 = s2.cv_kf(t.values, v, 0.5)
        self.assertAlmostEqual(float(x_g00[-1, 1]), 1.0)
        self.assertAlmostEqual(float(x_g10[-1, 1]), 1.0)
        self.assertAlmostEqual(float(x_g05[-1, 1]), 1.0)
