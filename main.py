#import libraries
import pandas as pd
import numpy as np
import plotly.graph_objs as go

#load data
matches_df = pd.read_csv('data/matches.csv')
deliveries_df = pd.read_csv('data/deliveries.csv')
#print (matches_df.head())
#print (deliveries_df.head())
#merge the two dataframs by match id
ipl = matches_df.merge(deliveries_df,left_on='id', right_on='match_id')
print (f"ipl.info:{ipl.info()}")
#umpire3 column is empty
print(f"missing data for umpire3 column:{ipl['umpire3'].isnull().sum()}")
#so drop the column
ipl.drop(['umpire3'], axis='columns', inplace=True)
print (f"after dropping umpire3 column, imp.info:{ipl.info()}")
#let's see all the columns name in the joint dataframe
print (ipl.columns)

# Problem :- We are going to draw a scatter plot between Batsman Avg(X axis) and
# Batsman Strike Rate(Y axis) of the top 50 batsman in IPL(All time)
#first, let's select the top 50 batsmen based on total runs scored
top_50_batsmen= ipl.groupby('batsman')['batsman_runs']\
                      .agg('sum')\
                      .reset_index()\
                      .sort_values('batsman_runs',ascending=False).head(50)
#now get relevent data for the top 50 players
#isin requires a list. Therefore, we have to convert the values from batsman column to list
top_50_data = ipl[ipl['batsman'].isin(top_50_batsmen['batsman'].values.tolist())]
#print(top_50_data.shape)
# Calculating SR
# SR=[(number of runs scored)/(number of balls played)]*100
#calculate total runs scored and number of balls played by a player
top_50_stat= top_50_data.groupby('batsman')['batsman_runs'].agg(['sum','count']).reset_index()
top_50_stat.rename(columns={'sum':'runs','count':'balls'},inplace=True)
top_50_stat['SR']=(top_50_stat['runs']/top_50_stat['balls'])*100
#print(f"top50:{top_50_stat.shape}")

#AVG= total run/number of outs

#Get the out information for the top 50 players
top_50_outs=top_50_data.groupby('batsman')['player_dismissed'].agg('count').reset_index()
print(f"group shape:{top_50_outs.shape}")
print(f"group columns: {top_50_outs.columns}")
print(top_50_outs.head())
 #merge top_50_out to top_50_stat
top_50=pd.merge(top_50_stat,top_50_outs)
#print(top_50.head())
top_50['Avg']= top_50['runs']/top_50['player_dismissed']
print(top_50.head())
