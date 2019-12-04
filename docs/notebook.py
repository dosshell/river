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
N = 200
t = pd.date_range('2018-01-01', periods=N, freq='D').values
y = np.power(1.05, range(len(t)))

v = 1 + np.random.normal(0, 0.1, N)
z = np.multiply(y, v)

px.line(x=t, y=z, log_y=True).show()
step = np.timedelta64(7, 'D')

# %% Error over gain

def E(x):
    t_bar, z_hat, z_bar = s2.cv_kf_estimate(t, np.log(z), x, step)
    z_hat = np.exp(z_hat)
    z_bar = np.exp(z_bar)
    e = (z_hat - z_bar) / z_bar
    me = np.abs(e).mean()
    return me

gx = np.linspace(0.0001, 0.1, 9)
ey = np.zeros(9)
for i in range(len(gx)):
    ey[i] = E(gx[i])

f = px.line(x=gx, y=ey)
f.show()

# %% Best gain

min_g = s2.globopt(E, 0.0001, 0.9999, 10, 4)
print(min_g)

# %% Kalman

x = s2.cv_kf(t, np.log(z), min_g)
x0 = np.exp(x[:,0])

fig = go.Figure()

fig.add_trace(go.Scatter(x=t, y=z, mode='lines'))
fig.add_trace(go.Scatter(x=t, y=x0, mode='lines'))
fig.update_layout(yaxis_type="log")
fig.show()

# %% Estimate Error

t_bar, z_hat, z_bar = s2.cv_kf_estimate(t, np.log(z), min_g, step)
z_hat = np.exp(z_hat)
z_bar = np.exp(z_bar)
e = (z_hat - z_bar) / z_bar

fig = go.Figure()
fig.add_trace(go.Scatter(x=t_bar, y=z_bar, mode='lines'))
fig.add_trace(go.Scatter(x=t_bar, y=z_hat, mode='lines'))
fig.update_layout(yaxis_type="log")
fig.show()

px.line(y=e)

# %% Forecast error histogram

t_bar, z_hat, z_bar = s2.cv_kf_estimate(t, np.log(z), min_g, step)
z_hat = np.exp(z_hat)
z_bar = np.exp(z_bar)
e = (z_hat - z_bar) / z_bar

px.histogram(e, x=0, nbins=25).show()

# %%
