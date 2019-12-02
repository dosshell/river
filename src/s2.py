import numpy as np
from numpy.linalg import inv
from typing import Callable


def cv_kf(t: np.ndarray, z: np.ndarray, gain: float):
    """
    t: np.ndarray[np.datetime64[us]]
    z: np.ndarray[float64]
    gain: (1-0)
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

    return x


def cv_kf_estimate(t, z, gain, step):
    """
    t: np.ndarray[np.datetime64[us]]
    z: np.ndarray[float64]
    gain: (1-0)
    step: numpy.timedelta64
    """
    res = np.timedelta64(1, 'D')
    f_step = step.astype('timedelta64[s]') / res
    x = cv_kf(t, z, gain)
    F = np.array([[1, f_step], [0, 1]])

    last_valid_date = (t - step)[-1]
    to_index = closest_index_before_or_equal(t, last_valid_date)
    if to_index is None:
        raise ValueError("Whoppsan hoppsan där! Har du för konstig data under fötterna?")

    x0_hat = np.zeros(to_index + 1)
    z_target = np.zeros(to_index + 1)
    for k in range(0, to_index + 1):
        x_hat = F @ x[k]
        x0_hat[k] = float(x_hat[0])

        # find stepped z value by interpolation
        target_date = t[k] + step
        t1_index = closest_index_before_or_equal(t, target_date)
        if t[t1_index] == target_date:
            z_target[k] = z[t1_index]
        else:
            z_target[k] = interpolate(t[t1_index], t[t1_index + 1], z[t1_index], z[t1_index + 1], target_date)

    return z_target, x0_hat


def closest_index_before_or_equal(t, target):
    """
    t: numpy.DatetimeIndex
    target: numpy.Datetime
    """
    # assume last index
    i = None
    for n in range(0, len(t)):
        if t[n] <= target:
            i = n
    return i


def interpolate(t1, t2, y1, y2, t_target):
    res = np.timedelta64(1, 'D')
    dt = (t2 - t1).astype('timedelta64[s]') / res
    k = (y2 - y1) / dt
    g = (t_target - t1).astype('timedelta64[s]') / res
    y_target = y1 + g * k
    return y_target


def globopt(F: Callable[[float], float], start: float, stop: float, steps: int, iterations: int = 1):
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
