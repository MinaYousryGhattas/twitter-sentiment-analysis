# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd


# Data
def plot_address_ratio(q, categorey_analysis):
    r = ["{}({})".format(i, categorey_analysis[i][0]+categorey_analysis[i][1]+categorey_analysis[i][2]
    ) if i is not None
         else "{}({})".format('Unknown',categorey_analysis[i][0]+categorey_analysis[i][1]+categorey_analysis[i][2]
    ) for i in categorey_analysis.keys()]
    greenBars = [i[0] for i in categorey_analysis.values()]
    redBars = [i[1] for i in categorey_analysis.values()]
    orangeBars = [i[2] for i in categorey_analysis.values()]
    total_green_bars = sum(greenBars)
    total_red_bars = sum(redBars)
    total_orange_bars = sum(orangeBars)
    greenBars += [total_green_bars]
    redBars += [total_red_bars]
    orangeBars += [total_orange_bars]
    r += ["{}({})".format('All', total_green_bars+total_orange_bars+total_red_bars)]

    raw_data = {'greenBars': greenBars, 'orangeBars': orangeBars, 'redBars': redBars}
    df = pd.DataFrame(raw_data)

    # From raw value to percentage
    totals = [i + j + k for i, j, k in zip(df['greenBars'], df['orangeBars'], df['redBars'])]
    greenBars = [i / j * 100 for i, j in zip(df['greenBars'], totals)]
    orangeBars = [i / j * 100 for i, j in zip(df['orangeBars'], totals)]
    redBars = [i / j * 100 for i, j in zip(df['redBars'], totals)]

    # plot
    barWidth = 0.50
    names = tuple(r)
    # Create green Bars
    plt.bar(r, greenBars, color='#008000', edgecolor='white', width=barWidth, label="POSITIVE")
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='#FF8C00', edgecolor='white', width=barWidth, label="NEUTRAL")
    # Create blue Bars
    plt.bar(r, redBars, bottom=[i + j for i, j in zip(greenBars, orangeBars)], color='#ff0000', edgecolor='white',
            width=barWidth, label="NEGATIVE")

    # Custom x axis
    plt.xticks(r, names, rotation=90)
    plt.xlabel("Countries")
    plt.title(q)
    # Show graphic
    plt.show()
