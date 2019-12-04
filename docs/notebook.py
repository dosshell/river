# flake8: noqa
# %% paths
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent) + '/src')
print(sys.path)

# %% in
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import s2

# %% create some data
N = 100
t = pd.date_range('2018-01-01', periods=N, freq='D').values
y = np.power(1.05, range(len(t)))

v = 1 + np.random.normal(0, 0.03, 100)
z = np.multiply(y, v)

px.line(x=t, y=z)
px.line(x=t, y=z, log_y=True)

# %% Kalman

x = s2.cv_kf(t, z, 0.005)
x0 = x[:, 0, 0]

fig = go.Figure()

fig.add_trace(go.Scatter(x=t, y=z, mode='lines'))
fig.add_trace(go.Scatter(x=t, y=x0, mode='lines'))
fig.update_layout(yaxis_type="log")
fig.show()

# %% Estimate Error

t_bar, z_hat, z_bar = s2.cv_kf_estimate(t, z, 0.1, np.timedelta64(21, 'D'))

e = (z_hat - z_bar) / z[range(len(z_hat))]

fig = go.Figure()
fig.add_trace(go.Scatter(x=t_bar, y=z_bar, mode='lines'))
fig.add_trace(go.Scatter(x=t_bar, y=z_hat, mode='lines'))
fig.update_layout(yaxis_type="log")
fig.show()

px.line(y=e)

# %%
