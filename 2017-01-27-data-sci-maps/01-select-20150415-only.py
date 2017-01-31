import pandas as pd
import datetime

df = pd.read_csv('data/yellow_tripdata_2015-04.csv')

df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])

len(df.index) #13,071,789

df['tpep_pickup_date'] = df['tpep_pickup_datetime'].map(lambda x: x.strftime('%Y-%m-%d'))


dfs = df[(df.tpep_pickup_date == '2015-04-15')]

len(dfs.index) #427,092

dfs.to_csv('data/yellow_tripdata_2015-04-15.csv',index=False)