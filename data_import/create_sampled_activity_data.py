# create activity data that is sampled monthly by chosen percentage
import pandas as pd

activity_filepath = input("enter activity file and folder path: ")
activity_filtered_filepath = input("enter activity filtered file and folder path: ")
activity_filtered_percentage = input("enter percentage of data to filter: ")
df = pd.read_csv(activity_filepath)
df.index = pd.to_datetime(df['started'], unit='s')
# df = df[(df.index >= '2014-1-1') & (df.index <= '2016-12-31')]
df.groupby([df.index.year, df.index.month]).sample(frac=int(activity_filtered_percentage), random_state=1).to_csv(
    activity_filtered_filepath, index=False)
