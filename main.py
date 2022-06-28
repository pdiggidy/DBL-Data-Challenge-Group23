from Boxplot import *
from heatmap import *
from Categories_sentiment import *
from BarCharts import *
from Superplot import *
import datetime as dt

running = True


def runplots(month:int):
    if month == "end":
        global running
        running = False
        return None
    #month = int(month)
    heatmap(month)
    box_plots(month)
    plot_categories_sentiment(month)
    plot_superplot_heatmap_in_plot(month)
    BarChart(month)


while running:
    runplots(input("Which Month Would You Like? "))