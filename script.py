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
        'Nick':['Netherlands','England','France','Brazil'],
        'Pele':['Senegal','France','Brazil','Argentina'],
        'Rafal':['Poland','Argentina','Netherlands','Brazil'],
        'Robin':['Netherlands','Denmark','Belgium','Portugal'],
         'Ruhi':['France','Belgium','Brazil','Argentina'],
        'Ruth':['Ghana','Senegal','France','Germany'],
        'Sarah':['Canada','Brazil','Netherlands','Ecuador'],
        'Steve':['Uruguay','Spain','Mexico','Netherlands'],
        'Stewart':['Brazil','United States','Portugal','Uruguay'],
        'TingYu':['Brazil','France','England','Poland'],
        'Brian':['Germany','France','Netherlands','Belgium']}
points_map = {'Qatar':65,'Ecuador':40,'Senegal':35,'Netherlands':14,'England':12,'Iran':65,
              'United States':35,'Wales':40,'Argentina':11, 'Saudi Arabia':120,'Mexico':35,
              'Poland':35, 'Denmark':20,'Tunisia':90,'France':11,'Australia':75,'Germany':13,
             'Japan':60,'Spain':12,'Costa Rica':120,'Morocco':60,'Croatia':25, 'Belgium':16,
             'Canada':70,'Switzerland':35,'Cameroon':75,'Brazil':10, 'Serbia':35,
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
to_publish.rename(columns = {'points':'group game points','games played outta 12':'group games played',0:'Team 1',1:'Team 2',2:'Team 3',3:'Team 4'}, inplace = True)
to_publish=to_publish[['group games points','group games played','ppg','Team 1','Team 2','Team 3','Team 4']]

#updating for group winners and runners up
temp_df = df.sort_values(by=['group_letter','group_points','goal_differential','goals_for','goals_against'],ascending=False).reset_index()
groupwinners = temp_df.iloc[::4,:].loc[temp_df['games_played']>2]['name'].to_list()
group_runnersup= temp_df.iloc[1: , :].iloc[::4,:].loc[temp_df['games_played']>2]['name'].to_list()

def get_success_points(my_list):
    group_success_points=0
    for team in my_list:
        if team in group_runnersup:
            group_success_points += 3*points_map[team]
        if team in groupwinners:
            group_success_points += 5*points_map[team]
    return group_success_points

to_publish['group success points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_success_points, axis=1)
to_publish['total tournament points']=to_publish['group success points']+to_publish['group game points']
to_publish.rename(columns = {'total tournament points':'Total points','group games played'}, inplace = True)
to_publish=to_publish[['Total points','group success points','group game points','played','ppg','Team 1','Team 2','Team 3','Team 4']]

st.dataframe(data=to_publish, height=my_df.shape[0]*50, use_container_width=True)
