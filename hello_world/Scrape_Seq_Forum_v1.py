'''
Created on Aug 15, 2018

@author: ubuntu
'''
import html5lib
import requests

#default 
#url = 'http://seqanswers.com/forums/forumdisplay.php?f=19'   
#Postings since last year (365 days), very few old postings in page 2.

url = 'http://seqanswers.com/forums/forumdisplay.php?s=&f=19&page=1&pp=30&sort=lastpost&order=desc&daysprune=365'
req = requests.get(url)
#req.text[:100]  #print first 100 chars

from bs4 import BeautifulSoup

#soup_l = BeautifulSoup(req.text, 'lxml')  # html.parser - python default parser
#Parser html5lib works better with forum data
soup = BeautifulSoup(req.text, 'html5lib')  
 
#Extract all "<TR>" tags below "<TBODY>" tage that has element "id = threadbits_forum_1"
trs_raw = soup.find('tbody', {'id': 'threadbits_forum_19'}).findAll("tr")
print(trs_raw)

def get_forum_data():
    
    forums = []
    trs = soup.find('tbody', {'id': 'threadbits_forum_19'}).findAll("tr")

    for i in trs:
        tds = i.findAll("td")
        forum_data = dict()
        forum_data['title'] = tds[2].text.strip()
        forum_data['date_time'] = tds[3].text.strip()
        forum_data['replies'] = tds[4].find('a').text.strip()
        forum_data['view'] = tds[5].text.strip()
        forums.append(forum_data)
        
    return forums

if __name__ == "__main__":
    print(get_forum_data())


# Convert raw list (uncleaned) to data
import pandas as pd

forums = get_forum_data()
forums_df = pd.DataFrame(forums).set_index('title')
print(forums_df)

#Cleaning data by removing/substituting the empty/new lines and tabs
#new_variable = re.sub('\n', '', old_variable)   # Remove the '\n' new-line
#new_variable = re.sub('\t', '', old_variable)   # Remove the '\t' tab

import re

def get_forums_data():
    
    forums = []
    trs = soup.find('tbody', {'id': 'threadbits_forum_19'}).findAll("tr")

    for i in trs:
        tds = i.findAll("td")
        forum_data = dict()
        
        #Fetch entire title
        title = tds[2].text.strip()
        title = re.sub('\t\t\t\t',' - ',title)
        title = re.sub('[\n,\t]','',title)
        forum_data['title'] = title
        
        #Fetch data from 3rd column contains date-time and user-name
        date_time = tds[3].text.strip()
        date_time = re.sub('\n\t\t\t',' - ',date_time)
        forum_data['date_time'] =  date_time
        
        #No of Replies
        forum_data['replies'] = tds[4].find('a').text.strip()
        
        # No of views
        view  = tds[5].text.strip()
        forum_data['view'] = view 
        
        forums.append(forum_data)
        
    return forums

if __name__ == "__main__":
    print(get_forums_data())
    

import pandas as pd

# construct a data from the list
forums = get_forums_data()


#Create CSV file.
import csv

with open('forum.csv', 'w+') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(('Title', 'Date_and_Time', 'Replies', 'Views'))
    for forum in forums:
        writer.writerow([forum['title'], forum['date_time'], forum['replies'], forum['view'] ])
        
# construct a data from from the cleaned list
forums = get_forums_data()
forums_df = pd.DataFrame(forums).set_index('title')
#forums_df = pd.DataFrame(forums).set_index('date_time')
print(forums_df)

#####################
# Plotting the data #
#####################

