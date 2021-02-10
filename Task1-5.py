# Importing all the libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import re
import matplotlib.pyplot as plt
from urllib.parse import urljoin
import json
import nltk
from numpy import arange

# TASK 1

# Finding the first link

base_url = 'http://comp20008-jh.eng.unimelb.edu.au:9889/main/'
page = requests.get(base_url)
soup = BeautifulSoup(page.text, 'html.parser')
links = soup.findAll('a')

# Creating a list of all the links 

link_list= []

# Joining the first hyperlink

for link in links:
    new_link = urljoin( base_url, link['href'])
    link_list.append(new_link)
 

# Forming a loop to find the rest of the links 

for lin in link_list:
    pages = requests.get(lin) 
    soups = BeautifulSoup(pages.text, 'html.parser')
    new_links = soups.findAll('a')
    
    for new_lin in new_links:
        joined = urljoin(base_url, new_lin['href'])
        if joined not in link_list:
            link_list.append(joined)
            
# Getting the titles            
titles = [] 

# Traversing through each link to get the title
for l in link_list:
    p = requests.get(l)
    s = BeautifulSoup(p.text, 'html.parser')
    title = s.findAll('h1')
    titl = title[0].text
    titles.append(titl)
    
# Contructing a table for urls and titles

link_list_series = pd.Series(link_list)
titles_series = pd.Series(titles)
links_frame = pd.DataFrame({'url': link_list_series, 'headline': titles_series})

# Producing a csv file for TASK 1
links_frame.to_csv('task1.csv', index = False)


# TASK 2

# Opening the json file and getting the team names into a list 
with open('rugby.json') as f:
    data = json.load(f)
    
values = list(data.values())
for dicts in values[0]:
    items = dicts.items()
    
teams = []

# Putting the team named which match with those in thr json file in a list
for dicts in values[0]:
    teams.append(list(dicts.values())[0])
     

# Creating empty lists to store the urls, titles, scores and team  names
# Creating empty dictionaries to store the game differences and article frequency
all_teams = []
all_links = []
all_scores = []
all_titles = []
game_diff = {}
article_freq = {}

# Traversing through every link to extract the article details 

for links in link_list:

    data = ''
    pages = requests.get(links) 
    soups = BeautifulSoup(pages.text, 'html.parser')
    para = soups.findAll('p')
   
    # Converting the article to a suitable form
    for lines in para:
        team = unicodedata.normalize("NFKD", lines.text.strip())
        data = data + team
        
    
    # Splitting the data on the basis of sentences to find the first team name
    
    split = data.split('.')
    word_found_list = []
    
    for line in split:
        for country in teams:
            word = re.findall(country, line)
            if len(word)!=0:
                word_found_list.append(word)
                
    # If a team name similar to that in the json file is found, find if the article has valid scores
    if len(word_found_list)!=0:
        
        patterns = re.findall(r'(\d+\-\d+)', data)
        
        # If valid score found, find the highest score in the article
        
        if len(patterns)!=0:
            sums = {}
            for score in patterns:
                split_score = score.split('-')
                if len(split_score[0])<=2 and len(split_score[1])<=2:
                    sum_score = int(split_score[0])+int(split_score[1])
                    sums[sum_score] = score
                    
            if len(sums)!=0:    
                max_score = sums[max(sums)]
                
                # Find the game difference for the max score 
                max_score_split = max_score.split('-')
                diff = abs(int(max_score_split[0])-int(max_score_split[1]))
                team = word_found_list[0][0]
                
                # Save the game difference along with the team in a dictionary
                if team in game_diff:
                    game_diff[team].append(diff)
                else:
                    game_diff[team] = [diff]
                
                # Save the max score, team name, url if a valid team name and valid score is found
                all_scores.append(max_score)
                all_teams.append(word_found_list[0][0])
                all_links.append(links)
                
                # Find the title of the article
                title = soups.findAll('h1')
                titl = title[0].text
                all_titles.append(titl)

# Find the article frequency

for team in all_teams:
    if team in article_freq:
        article_freq[team] +=1
    else:
        article_freq[team] = 1

# Find the average game difference for every team        
        
avg_game_difference = {}              
for team in game_diff:
    score_list = game_diff[team]
    avg = sum(score_list)/len(score_list)
    avg_game_difference[team] = avg    

# Separating the teams and their average game differences into lists
    
team_diff = [team for team in avg_game_difference]
avg_diff = [avg_game_difference[team] for team in avg_game_difference]


# Creating a dataframe for task 2

all_scores_series=pd.Series(all_scores)
all_teams_series=pd.Series(all_teams)
all_titles_series=pd.Series(all_titles)
all_links_series=pd.Series(all_links)
table=pd.DataFrame({'url': all_links_series,'headline': all_titles_series,'team': all_teams_series,'score': all_scores_series})
table.to_csv('task2.csv',index=False)   

# Creating a dataframe for task 3

team_diff_series = pd.Series(team_diff)
avg_diff_series = pd.Series(avg_diff)
table_2 = pd.DataFrame({'team':team_diff_series, 'avg_game_difference': avg_diff_series}) 
table_2.to_csv('task3.csv', index=False)

# Extracting the first five teams with the highest frequency of articles

article_teams = article_freq.items()
article_sorted = sorted(list(article_teams), key=lambda x:x[1], reverse=True)
first_five = article_sorted[:5]
team_list = [pair[0] for pair in first_five]
freq_list = [pair[1] for pair in first_five]

# Creating a bar graph for task 4

plt.bar(arange(len(freq_list)),freq_list)
plt.xticks( arange(len(team_list)),team_list, rotation=30)
plt.xlabel('Teams')
plt.ylabel('Article Frequency')
plt.title('Article Frequency of Teams')
plt.savefig('task4.png')
plt.show()


# Creating a bar graph for task 5

list_team = [team for team in article_freq]
avg_game = [avg_game_difference[team] for team in avg_game_difference]
article_list = [article_freq[team] for team in article_freq]

plt.bar(arange(len(avg_game))-0.4, avg_game, width=0.4, label = 'Average game difference')
plt.bar(arange(len(article_list)),article_list, width=0.4,color='r', label='No. of articles')
plt.xticks(arange(len(list_team)),list_team, rotation=30)
plt.xlabel('Teams')
plt.ylabel('Frequency')
plt.legend()
plt.title('Average game difference and Article frequency')
plt.savefig('task5.png')
plt.show()