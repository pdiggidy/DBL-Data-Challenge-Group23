import pandas as pd
import pymysql
from sqlalchemy import create_engine

db_con = ""

with open("pw.txt") as r:
    lines = r.readlines()
    db_con = lines[0]

engine = create_engine(db_con)

df=pd.read_sql("SELECT * FROM Test", engine)
print(df)