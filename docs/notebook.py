# %% in
import numpy as np
import plotly.express as px

# %% create some data
x = np.arange(0, 100)
y = np.power(1.05, x)

v = 1 + np.random.normal(0, 0.03, 100)
z = np.multiply(y, v)

fig = px.line(x=x, y=z)
fig.show()

# %% Log scale and plot

yl = np.log(z) / np.log(1.01)
fig = px.line(x=x, y=yl)
fig.show()

# %% Log plot

fig = px.line(x=x, y=z, log_y=True)
fig.show()

# %% Diff

d = np.diff(np.log(z))
fig = px.line(x=x[1:], y=d)
fig.show()

# %%
