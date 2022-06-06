import os
from sqlalchemy import create_engine
from CompanySort import *
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from Lists import *
import statistics as stat
import seaborn as sns
import numpy as np

connection = create_engine(os.environ["DB_STRING"]).connect()

df_conv = pd.read_sql_table("Conversations", connection)
df_conv_numpy = df_conv.to_numpy()


6
