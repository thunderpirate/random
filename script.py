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
        'Moneca':['Brazil','Germany','France','Argentina']}
points_map = {'Qatar':65,'Ecuador':50,'Senegal':35,'Netherlands':14,'England':12,'Iran':65,
              'United States':35,'Wales':40,'Argentina':11, 'Saudi Arabia':120,'Mexico':35,
              'Poland':35, 'Denmark':20,'Tunisia':90,'France':11,'Australia':75,'Germany':13,
             'Japan':60,'Spain':12,'Costa Rica':120,'Morocco':60,'Croatia':25, 'Belgium':16,
             'Canada':17,'Switzerland':35,'Cameroon':75,'Brazil':10, 'Serbia':35,
             'Uruguay':25,'South Korea':60, 'Portugal':15, 'Ghana':65}
standings= {}

url= 'https://worldcupjson.net/teams'
r=requests.get(url)
data = r.json()
for player in teams:
    standings[player] = 0

master_data = []
for k,v in data.items():
    for x in v:
        for y in x['teams']:
            master_data.append(y)
df = pd.DataFrame(master_data)

for player in teams:
    for pick in teams[player]:
        standings[player]+=int(df.loc[df['name'] == pick, 'group_points'])*points_map[pick]
st.write((pd.DataFrame.from_dict(standings,orient='index',columns=['points']).sort_values(by=['points'],ascending=False))
