from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

x = [1,2,3,4,5,6,7,8,9]
y = [1,1,
     2,2,2,2,2,2,
     3,3,3,3,3,
     4,4,4,
     5,
     6,6,
     7,7,7,
     ]
y_series = pd.Series(y)
print(y_series.mean())