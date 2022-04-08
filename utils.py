import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


class ExitCodeError(Exception):
    pass


def sh(x):
    if os.system(x):
        raise ExitCodeError()


def radar_chart_plot(df):

    fig = px.line_polar(df, r="scores", theta="labels", line_close=True)

    return fig


def bar_chart_plot(prediction_result):
    plt.plot()

    height = list(prediction_result.values())
    bars = list(prediction_result.keys())
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, bars, rotation="vertical")
