import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from numpy import argsort
from matplotlib.patches import Patch

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #######################################################################################
# 
# Description: This file calculates the average annual salary for each MLB team. It takes
# a list of player salaries for each team, sums up the player salaries during each year,
# and then calculates the average salary over a given year range.
#  
# NOTE: The year ranges do have some variation. Most teams have salary info from 1985-
# 2015, but some teams have differences. Here's the list...
# -- Miami Marlins (aka Florida Marlins): 1993-2015
# -- Colorado Rockies: 1993-2015
# -- Tampa Bay Rays: 1998-2015
# -- Arizona Diamondbacks: 1998-2015
# 
# #######################################################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Dictionary to convert 3-letter abbreviations into team names
all_teams = {
    'ANA': 'Anaheim Angels',                    # Existed from 1997-2004, became the Los Angeles Angels
    'ARI': 'Arizona Diamondbacks',
    'ATL': 'Atlanta Braves',
    'BAL': 'Baltimore Orioles',
    'BOS': 'Boston Red Sox',
    'CAL': 'California Angels',                 # Renamed several times; now Los Angeles Angels
    'CHA': 'Chicago White Sox',
    'CHN': 'Chicago Cubs',
    'CLE': 'Cleveland Guardians',               # Formerly Indians
    'CIN': 'Cincinnati Reds',
    'COL': 'Colorado Rockies',
    'DET': 'Detroit Tigers',
    'FLO': 'Florida Marlins',                   # Existed from 1993-2011, renamed Miami Marlins
    'HOU': 'Houston Astros',
    'KCA': 'Kansas City Royals',
    'LAA': 'Los Angeles Angels',
    'LAN': 'Los Angeles Dodgers',
    'ML4': 'Milwaukee Brewers (AL)',            # Milwaukee Brewers in the American League from 1970-1998
    'MIL': 'Milwaukee Brewers',                 # Milwaukee Brewers after they moved to the National League in 1998
    'MIN': 'Minnesota Twins',
    'MIA': 'Miami Marlins',
    'MON': 'Montreal Expos',                    # Moved to Washington Nationals
    'NYA': 'New York Yankees',
    'NYN': 'New York Mets',
    'OAK': 'Oakland Athletics',
    'PHI': 'Philadelphia Phillies',
    'PIT': 'Pittsburgh Pirates',
    'SDN': 'San Diego Padres',
    'SEA': 'Seattle Mariners',
    'SFN': 'San Francisco Giants',
    'SLN': 'St. Louis Cardinals',
    'TBA': 'Tampa Bay Rays',
    'TEX': 'Texas Rangers',
    'TOR': 'Toronto Blue Jays',
    'WAS': 'Washington Nationals'             
}

# Gathering salary data from CSV file
df_salaries = pd.read_csv("Salaries.csv")
# Creating set of abbreviations for each team
all_teams_list = set(list(df_salaries['teamID']))
# Some teams had two or more abbreviations
duplicate_teams = ["ML4", "MON", "CAL", "ANA", "FLO"]
# Remove teams from abbreviation list, will account for these teams' salaries later
for team in duplicate_teams:
    all_teams_list.remove(team)

# Dictionary for holding average annual salary for each team  
salary_by_team = {}

# -------------------------------------------------------------------
# Process and find the average annual salary for each team
# -------------------------------------------------------------------
for team in all_teams_list:

    # Handling data from teams that operated under two names (and have two abbreviations)
    if (team == "MIL"):
        # "Milwaukee Brewers" and "Milwaukee Brewers (AL)"
        # ----------------------------------------------------------------
        old_team_df = df_salaries[df_salaries['teamID'] == "ML4"]
        old_team_years = set(list(old_team_df['yearID']))

        new_team_df = df_salaries[df_salaries['teamID'] == team]
        new_team_years = set(list(new_team_df['yearID']))

        # Build dataframe for all salaries for the team
        team_df = pd.concat([old_team_df, new_team_df])
        # Build list of all years for the team
        years = old_team_years.union(new_team_years)
    elif (team == "WAS"):
        # "Washington Nationals" and "Montreal Expos"
        # ----------------------------------------------------------------
        old_team_df = df_salaries[df_salaries['teamID'] == "MON"]
        old_team_years = set(list(old_team_df['yearID']))

        new_team_df = df_salaries[df_salaries['teamID'] == team]
        new_team_years = set(list(new_team_df['yearID']))

        # Build dataframe for all salaries for the team
        team_df = pd.concat([old_team_df, new_team_df])
        # Build list of all years for the team
        years = old_team_years.union(new_team_years)
    elif (team == "LAA"):
        # "Los Angeles Angels", "Anaheim Angels", and "California Angels"
        # ----------------------------------------------------------------
        old_team_df_1 = df_salaries[df_salaries['teamID'] == "CAL"]
        old_team_years_1 = set(list(old_team_df_1['yearID']))
        old_team_df_2 = df_salaries[df_salaries['teamID'] == "ANA"]
        old_team_years_2 = set(list(old_team_df_2['yearID']))

        new_team_df = df_salaries[df_salaries['teamID'] == team]
        new_team_years = set(list(new_team_df['yearID']))

        # Build dataframe for all salaries for the team
        team_df = pd.concat([old_team_df_1, old_team_df_2, new_team_df])
        # Build list of all years for the team
        years = old_team_years_1.union(new_team_years)
        years.update(old_team_years_2)
    elif (team == "MIA"):
        # "Miami Marlins" and "Florida Marlins"
        # ----------------------------------------------------------------
        old_team_df = df_salaries[df_salaries['teamID'] == "FLO"]
        old_team_years = set(list(old_team_df['yearID']))

        new_team_df = df_salaries[df_salaries['teamID'] == team]
        new_team_years = set(list(new_team_df['yearID']))

        # Build dataframe for all salaries for the team
        team_df = pd.concat([old_team_df, new_team_df])
        # Build list of all years for the team
        years = old_team_years.union(new_team_years)
    else:
        # Build dataframe for all salaries for the team
        team_df = df_salaries[df_salaries['teamID'] == team]
        # Build list of all years for the team
        years = set(list(team_df['yearID']))

    # Building list of salary in each year 
    salary_by_year = []
    for year in years: 
        year_df = team_df[team_df['yearID'] == year]
        salary_by_year.append(year_df['salary'].mean())

    # Calculate average salary over length of years
    avg_team_salary = sum(salary_by_year)/len(years)

    # Save data to dictionary
    salary_by_team[team] = avg_team_salary
    
# ------------------------------------------------------------------------
# Sort dictionary of teams by salary (descending) 
# ------------------------------------------------------------------------
keys = list(salary_by_team.keys())
for k in keys:
    k = all_teams[k]
values = list(salary_by_team.values())
sorted_value_index = argsort(values)
sorted_salaries = {keys[i]: values[i] for i in sorted_value_index}

# Converting abbreviations to full team names
names = []
for key in sorted_salaries.keys(): 
    names.append(all_teams[key])

# ------------------------------------------------------------------------
# Plot results to horizontal bar chart
# ------------------------------------------------------------------------
plt.figure(figsize=(16,10))
color_map = {'MIA': 'tab:purple','COL': 'tab:purple', 'TBA': 'tab:pink', 'ARI': 'tab:pink'}
bar_colors = [color_map.get(team, 'tab:blue') for team in sorted_salaries.keys()] 

plt.barh(names, sorted_salaries.values(), height=0.5, align='center', color=bar_colors)
plt.title("AVERAGE SALARY BY TEAM")
plt.xlabel("Average salary per year \n(date ranges vary -- see color key)")
plt.ylabel("Team name")
plt.xticks([0, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000], ['0', '$500K', '$1M', '$1.5M', '$2M', '$2.5M', '$3M', '$3.5M', '$4M'])
plt.yticks(list(names))  # Ensure all keys are displayed on y-axis
handles = [
    Patch(facecolor='tab:blue', label='1985-2015'),
    Patch(facecolor='tab:purple', label='1993-2015'),
    Patch(facecolor='tab:pink', label='1998-2015')
]
plt.legend(handles=handles, loc="center right")
plt.savefig("salaries2.png")

# Generating simple webpage display using Streamlit
st.image("salaries2.png")
st.page_link("https://www.kaggle.com/datasets/open-source-sports/baseball-databank/data?select=Salaries.csv", label="**Source**: Baseball Databank \t :green-badge[Salaries.csv]")
st.title("Average Yearly Salary By MLB Team")

