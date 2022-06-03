import os
from sqlalchemy import create_engine
import pandas as pd

connection = create_engine(os.environ["DB_STRING"]).connect()

df = pd.read_sql_table('AirFrance', connection)
print(df.head(20))
