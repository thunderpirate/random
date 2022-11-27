# Load packages
import streamlit as st
import pandas as pd
import requests

teams = {'Liam':['Brazil','France','Senegal','Argentina'], 
         'Andrew':['France','Switzerland','Morocco','Uruguay'],
        'Amanda':['England','Canada','Belgium','Brazil'],
        'Anna':['Germany','England','Ecuador','Uruguay'],
        'Ashley':['Netherlands','Argentina','Brazil','Spain'],
        'Carla':['Netherlands','Germany','Denmark','Switzerland'],
        'Charles':['Germany','Wales','Mexico','Uruguay'],
         'Chirag':['Brazil','Argentina','France','Belgium'],
        'Dennis':['Argentina','Brazil','Germany','France'],
        'Dylan':['Ecuador','Wales','Croatia','Ghana'],
        'Esther':['Brazil','Argentina','Mexico','Denmark'],
        'Kyle':['Netherlands','United States','Denmark','Canada'],
        'Lori':['Germany','Portugal','Brazil','Cameroon'],
        'Moneca':['Brazil','Germany','France','Argentina'],
         'Nelson':['Ecuador','Denmark','Germany','Brazil'],
        'Nick':['Netherlands','England','France','Brazil']}
points_map = {'Qatar':65,'Ecuador':50,'Senegal':35,'Netherlands':14,'England':12,'Iran':65,
              'United States':35,'Wales':40,'Argentina':11, 'Saudi Arabia':120,'Mexico':35,
              'Poland':35, 'Denmark':20,'Tunisia':90,'France':11,'Australia':75,'Germany':13,
             'Japan':60,'Spain':12,'Costa Rica':120,'Morocco':60,'Croatia':25, 'Belgium':16,
             'Canada':17,'Switzerland':35,'Cameroon':75,'Brazil':10, 'Serbia':35,
             'Uruguay':25,'South Korea':60, 'Portugal':15, 'Ghana':65}

url= 'https://worldcupjson.net/teams'
r=requests.get(url)
data = r.json()

master_data = []
for k,v in data.items():
    for x in v:
        for y in x['teams']:
            master_data.append(y)
df = pd.DataFrame(master_data)

standings={}
for player in teams:
    standings[player] = 0
    
games_played={}
for player in teams:
    games_played[player] = 0


for player in teams:
    for pick in teams[player]:
        standings[player]+=int(df.loc[df['name'] == pick, 'group_points'])*points_map[pick]
        games_played[player]+=int(df.loc[df['name'] == pick, 'games_played'])
        
my_df = pd.DataFrame.from_dict(standings,orient='index',columns=['points']).sort_values(by=['points'],ascending=False)
teams_df = pd.DataFrame(teams).T
games_played_df=pd.DataFrame.from_dict(games_played,orient='index',columns=['games played outta 12'])
to_publish = my_df.join(games_played_df).join(teams_df)
to_publish['ppg']=to_publish['points']/to_publish['games played outta 12']
st.dataframe(data=to_publish, height=my_df.shape[0]*50, use_container_width=True)
