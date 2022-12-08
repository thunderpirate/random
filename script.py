# Load packages
import streamlit as st
# Load packages
import pandas as pd
import requests

teams = {'Liam':['Brazil','France','Argentina','Senegal'], 
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

#url= 'https://worldcupjson.net/teams'
#r=requests.get(url)
#data = r.json()

#master_data = []
#for k,v in data.items():
#    for x in v:
#        for y in x['teams']:
#            master_data.append(y)
#df = pd.DataFrame(master_data)

#standings={}
#for player in teams:
#    standings[player] = 0
    
#games_played={}
#for player in teams:
#    games_played[player] = 0


#for player in teams:
#    for pick in teams[player]:
#        standings[player]+=int(df.loc[df['name'] == pick, 'group_points'])*points_map[pick]
#        games_played[player]+=int(df.loc[df['name'] == pick, 'games_played'])
        
#my_df = pd.DataFrame.from_dict(standings,orient='index',columns=['points']).sort_values(by=['points'],ascending=False)
to_publish = pd.DataFrame(teams).T
#games_played_df=pd.DataFrame.from_dict(games_played,orient='index',columns=['games played outta 12'])
#to_publish = my_df.join(games_played_df).join(teams_df)
#to_publish['ppg']=to_publish['points']/to_publish['games played outta 12']
to_publish.rename(columns = {0:'Team 1',1:'Team 2',2:'Team 3',3:'Team 4'}, inplace = True)
#to_publish=to_publish[['group game points','played','ppg','Team 1','Team 2','Team 3','Team 4']]

'''#updating for group and runners up - unusable now due to KO rounds being classified as group games
temp_df = df.sort_values(by=['group_letter','group_points','goal_differential','goals_for','goals_against'],ascending=False).reset_index()
groupwinners = temp_df.iloc[::4,:].loc[temp_df['games_played']>2]['name'].to_list()
group_runnersup= temp_df.iloc[1: , :].iloc[::4,:].loc[temp_df['games_played']>2]['name'].to_list()'''

def get_fixtures():
    link = 'https://worldcupjson.net/matches'
    request = requests.get(link)
    data = request.json()
    fixtures_df = pd.DataFrame.from_dict(data)
    return fixtures_df

fixtures_df = get_fixtures()
home_team_detail = fixtures_df.home_team.apply(pd.Series)
home_team_detail=home_team_detail.drop(['penalties','country'],axis=1)
home_team_detail.rename(columns = {'name':'home_name','goals':'home_goals'}, inplace = True)
away_team_detail = fixtures_df.away_team.apply(pd.Series)
away_team_detail=away_team_detail.drop(['penalties','country'],axis=1)
away_team_detail.rename(columns = {'name':'away_name','goals':'away_goals'}, inplace = True)
fixtures_df = fixtures_df.join(home_team_detail).join(away_team_detail)

for i in points_map.keys():
    group_points_base[i]=0
for i, j in fixtures_df.iterrows():
    if j['stage_name']=='First stage':
        if j.winner == 'Draw':
            if j.home_name in group_points_base.keys():    
                group_points_base[j.home_name]+=1
            else:
                group_points_base[j.home_name]=1
            if j.away_name in group_points_base.keys():    
                group_points_base[j.away_name]+=1
            else:
                group_points_base[j.away_name]=1
        else:
            if j.winner in group_points_base.keys():    
                group_points_base[j.winner]+=3
            else:
                group_points_base[j.winner]=3


groupwinners = ['Netherlands', 'England', 'Argentina', 'France', 'Japan', 'Morocco', 'Brazil', 'Portugal']
group_runnersup = ['Senegal', 'USA', 'Poland', 'Australia', 'Spain', 'Croatia', 'Switzerland', 'Korea Republic']

def get_group_game_points(my_list):
    group_game_points=0
    for team in my_list:
        group_game_points += group_points_base[team]*points_map[team]
    return group_game_points

def get_group_success_points(my_list):
    group_success_points=0
    for team in my_list:
        if team in group_runnersup:
            group_success_points += 3*points_map[team]
        if team in groupwinners:
            group_success_points += 5*points_map[team]
    return group_success_points

def get_last16_points(my_list):
    last_16_points=0
    for team in my_list:
        if team in r16_winners:
            last_16_points += 10*points_map[team]
    return last_16_points

def get_quarter_final_points(my_list):
    quarter_final_points=0
    for team in my_list:
        if team in q_final_winners:
            quarter_final_points += 12*points_map[team]
    return quarter_final_points

def get_semi_final_points(my_list):
    semi_final_points=0
    for team in my_list:
        if team in s_final_winners:
            semi_final_points += 15*points_map[team]
    return semi_final_points

def get_final_points(my_list):
    final_points=0
    for team in my_list:
        if team in final_winner:
            final_points += 25*points_map[team]
    return final_points

def get_third_place_points(my_list):
    third_place_points=0
    for team in my_list:
        if team in third_place:
            semi_final_points += 10*points_map[team]
    return third_place_points

to_publish['group game points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_group_game_points, axis=1)
to_publish['group qual. points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_group_success_points, axis=1)
to_publish['last 16 points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_last16_points, axis=1)
to_publish['quarter-final points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_quarter_final_points, axis=1)
to_publish['semi-final points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_semi_final_points, axis=1)
to_publish['3rd place points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_third_place_points, axis=1)
to_publish['Champion points']=to_publish[['Team 1','Team 2','Team 3','Team 4']].apply(get_final_points, axis=1)
to_publish['Total Points']=to_publish['Champion points']+to_publish['3rd place points']+to_publish['semi-final points']+to_publish['quarter-final points']+to_publish['last 16 points']+to_publish['group qual. points']+to_publish['group game points']
to_publish=to_publish[['Total Points','Champion points','3rd place points','semi-final points','quarter-final points','last 16 points','group qual. points','group game points','Team 1','Team 2','Team 3','Team 4']]
to_publish=to_publish.sort_values(by=['Total Points'],ascending=False)

st.set_page_config(layout="wide")
st.dataframe(data=to_publish, height=my_df.shape[0]*50, width=20000, use_container_width=True)
