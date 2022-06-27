#from Boxplot import *
from heatmap import *
import datetime as dt

running = True


def runplots(month:int):
    if month == "end":
        global running
        running = False
        return None
    heatmap(int(month))


while running:
    runplots(input("Which Month Would You Like? "))