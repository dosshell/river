import numpy as np
from numpy.linalg import inv
from typing import Callable
from typing import NamedTuple


def cv_kf(t: 'np.ndarray[np.datetime64]', z: 'np.ndarray[np.float64]', gain: float) -> 'np.ndarray[np.float64]':
    """
    :param t: timestamps
    :param z: measurements
    :param gain: gain value between (1-0)
    """
    if t.ndim != 1 or z.ndim != 1:
        raise ValueError("Dimensions of t and v is wrong")
    if len(t) != len(z):
        raise ValueError("t and v has to be of the same length")
    if gain <= 0 or gain >= 1:
        raise ValueError("gain has to be in the interval of (0-1)")

    def Qm(dt):
        return np.array([[1 / 4 * dt**4, 1 / 2 * dt**3], [1 / 2 * dt**3, dt**2]])

    res = np.timedelta64(1, 'D')

    x = np.zeros((len(t), 2, 1))
    y = np.zeros((len(t), 1, 1))
    P = np.zeros((len(t), 2, 2))
    Q_var = gain
    Z_var = 1 - gain
    x[0] = np.array([[z[0]], [0]])

    dt_init = 1.0
    P[0] = Qm(dt_init) * Q_var

    H = np.array([[1, 0]])
    R = np.array([[Z_var]])

    for k in range(1, len(t)):
        dt = (t[k] - t[k - 1]).astype('timedelta64[s]') / res
        F = np.array([[1, dt], [0, 1]])
        Q = Qm(dt) * Q_var

        x[k] = F @ x[k - 1]
        P[k] = F @ P[k - 1] @ F.transpose() + Q

        if not np.isnan(y[k]):
            y[k] = z[k] - H @ x[k]
            S = H @ P[k] @ H.transpose() + R
            K = P[k] @ H.transpose() @ inv(S)
            x[k] = x[k] + K @ y[k]
            P[k] = (np.eye(2) - K @ H) @ P[k]

    return x[:, :, 0]


class Estimation(NamedTuple):
    t_bar: 'np.ndarray[np.datetime64]'  # timestamp of made target pridection
    z_har: 'np.ndarray[np.float64]'  # predicted z measurement
    z_bar: 'np.ndarray[np.float64]'  # interpolated z measurement


def cv_kf_estimate(t: 'np.ndarray[np.datetime64]', z: 'np.ndarray[np.float64]', gain: float,
                   step: np.timedelta64) -> Estimation:
    """
    Make historical estimations

    :param t: timestamps
    :param z: measurements
    :param gain: value ebtween (0 - 1)
    :param step: timestep into the future to predict
    :return: Estimation class
    """
    res = np.timedelta64(1, 'D')
    f_step = step.astype('timedelta64[s]') / res
    x = cv_kf(t, z, gain)
    F = np.array([[1, f_step], [0, 1]])

    last_valid_date = (t - step)[-1]
    to_index = closest_index_before_or_equal(t, last_valid_date)
    if to_index is None:
        raise ValueError("Whoppsan hoppsan där! Har du för konstig data under fötterna?")

    t_bar = np.zeros(to_index + 1, dtype='datetime64[D]')
    z_hat = np.zeros(to_index + 1)
    z_bar = np.zeros(to_index + 1)

    for k in range(0, to_index + 1):
        # predict with cvkf model
        x_hat = F @ x[k]
        z_hat[k] = float(x_hat[0])

        target_date = t[k] + step
        t_bar[k] = target_date

        # find stepped z value by interpolation
        t1_index = closest_index_before_or_equal(t, target_date)
        if t[t1_index] == target_date:
            z_bar[k] = z[t1_index]
        else:
            z_bar[k] = interpolate(t[t1_index], t[t1_index + 1], z[t1_index], z[t1_index + 1], target_date)

    return Estimation(t_bar, z_hat, z_bar)


def closest_index_before_or_equal(t: 'np.ndarray[np.datetime64]', target: 'np.ndarray[np.datetime64]') -> int:
    '''
    returns -1 if target is before all values in t
    '''
    i = -1
    for n in range(0, len(t)):
        if t[n] <= target:
            i = n
    return i


def interpolate(t1: np.datetime64, t2: np.datetime64, y1: float, y2: float, t_target: np.datetime64) -> float:
    res = np.timedelta64(1, 'D')
    dt = (t2 - t1).astype('timedelta64[s]') / res
    k = (y2 - y1) / dt
    g = (t_target - t1).astype('timedelta64[s]') / res
    y_target = y1 + g * k
    return y_target


def globopt(F: Callable[[float], float], start: float, stop: float, steps: int, iterations: int = 1) -> float:
    x = np.linspace(start, stop, steps)
    y = np.zeros(steps)
    for i in range(steps):
        y[i] = F(x[i])
    im = np.argmin(y)
    if iterations == 1:
        return x[im]
    else:
        x1 = x[max(im - 1, 0)]
        x2 = x[min(im + 1, steps - 1)]
        return globopt(F, x1, x2, steps, iterations - 1)


class Tuning(NamedTuple):
    tuned_value: float
    errors: 'np.ndarray[np.float64]'


def cv_kf_tune_log(t: 'np.ndarray[np.datetime64]', z: 'np.ndarray[np.float64]', step: np.timedelta64) -> Tuning:
    def E(x):
        t_bar, z_hat, z_bar = cv_kf_estimate(t, np.log(z), x, step)
        z_hat = np.exp(z_hat)
        z_bar = np.exp(z_bar)
        e = (z_hat - z_bar) / z_bar
        me = np.abs(e).mean()
        return me

    min_g = globopt(E, 0.001, 0.999, 10, 4)
    t_bar, z_hat, z_bar = cv_kf_estimate(t, np.log(z), min_g, step)
    z_hat = np.exp(z_hat)
    z_bar = np.exp(z_bar)
    e = (z_hat - z_bar) / z_bar
    return Tuning(min_g, e)


class Prediction(NamedTuple):
    predicted_value: float
    historic_errors: 'np.ndarray[np.float64]'
