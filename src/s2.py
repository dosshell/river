import numpy as np
from numpy.linalg import inv


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
        dt = 1
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
