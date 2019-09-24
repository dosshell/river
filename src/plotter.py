import io
import matplotlib.pyplot as plt


def example_plot(x, y):
    buf = io.BytesIO()

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='Time', ylabel='Percentage [%]', title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()
