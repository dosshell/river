import io
import matplotlib.pyplot as plt
from pandas.core.series import Series
from pandas.plotting import register_matplotlib_converters


def example_plot(x: Series, y: Series):
    buf = io.BytesIO()
    register_matplotlib_converters()
    fig, ax = plt.subplots()

    ax.plot(x, y)

    ax.set(xlabel='Time', ylabel='Percentage [%]', title='Half of writing history is hiding the truth')
    ax.grid()

    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()
