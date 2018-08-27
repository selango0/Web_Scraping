'''
Web-scrape seqanswers forum and extract number of views, corresponding date, and replies.
Save data to a .csv file
url = 'http://seqanswers.com/forums/forumdisplay.php?f=19'   
Postings since last year (365 days)
'''

import requests
import html5lib
from bs4 import BeautifulSoup


url = 'http://seqanswers.com/forums/forumdisplay.php?s=&f=19&page=1&pp=30&sort=lastpost&order=desc&daysprune=365'

req = requests.get(url)                                                                                  #req.text[:100]  #print first 100 chars
soup = BeautifulSoup(req.text, 'html5lib')                                                    #parser html5lib  
trs_raw = soup.find('tbody', {'id': 'threadbits_forum_19'}).findAll("tr")       #extract all "<TR>" tags below "<TBODY>" tage that has element "id = threadbits_forum_1"
print(trs_raw)

'''
Funtion extracts body from forum
'''
def get_forum_data():
    forums = []
    trs = soup.find('tbody', {'id': 'threadbits_forum_19'}).findAll("tr")          #extract all "<TR>" (rows) tags below "<TBODY>" tage that has element "id = threadbits_forum_19"

    for i in trs:
        tds = i.findAll("td")                                                                             #extract all cells in trs 
        forum_data = dict()                                                                             #instantiate a dictionary
        forum_data['title'] = tds[2].text.strip()                                                 #extract text from tds column 2 and store value for 'title' key
        forum_data['date_time'] = tds[3].text.strip()                                        #extract text from tds column 3 and store value for 'date_time' key
        forum_data['replies'] = tds[4].find('a').text.strip()                                #extract text from tds column 4 and store value for 'replies' key
        forum_data['view'] = tds[5].text.strip()                                                #extract text from tds column 5 and store value for 'view' key
        forums.append(forum_data)                                                               #append the forum_data dict to forums list
        
    return forums

if __name__ == "__main__":
    print(get_forum_data())


import pandas as pd

forums = get_forum_data()
forums_df = pd.DataFrame(forums).set_index('title')                                 #convert raw list to data
print(forums_df)


import re
'''

Cleaning data by removing/substituting the empty/new lines and tabs
new_variable = re.sub('\n', '', old_variable)   # Remove the '\n' new-line
new_variable = re.sub('\t', '', old_variable)   # Remove the '\t' tab

'''
def get_forum_data():
    
    forums = []
    trs = soup.find('tbody', {'id': 'threadbits_forum_19'}).findAll("tr")         #extract all "<TR>" (rows) tags below "<TBODY>" tage that has element "id = threadbits_forum_19"

    for i in trs:
        tds = i.findAll("td")                                                                            #extract all cells in trs 
        forum_data = dict()                                                                            #instantiate a dictionary
        
        
        title = tds[2].text.strip()                                                                       #fetch entire title
        title = re.sub('\t\t\t\t',' - ',title)                                                               #remove the '\t' tab 
        title = re.sub('[\n,\t]','',title)                                                                  #remove the [\n,\t] new-line with tab
        forum_data['title'] = title                                                                     #replace old title with the new, cleaned title
        
        
        date_time = tds[3].text.strip()                                                             #Fetch data from 3rd column contains date-time and user-name
        date_time = re.sub('\n\t\t\t',' - ',date_time)                                           #remove the '\n' and '\t's 
        forum_data['date_time'] =  date_time                                                 #replace old date_time column with the new,cleaned date_time
        
        
        forum_data['replies'] = tds[4].find('a').text.strip()                               #extract number of replies column
        
        
        view  = tds[5].text.strip()                                                                    #extract number of views column
        forum_data['view'] = view                                                                 #add the number of views column to dict 
        
        forums.append(forum_data)                                                              #append forum_data dict to list, forums
        
    return forums

if __name__ == "__main__":
    print(get_forum_data())
    

import pandas as pd


forums = get_forum_data()                                                                       #construct data from the list                   



import csv                                                                                                 #create CSV file.

with open('forum.csv', 'w+') as csvFile:                                                    #open and write onto a .csv file called forum
    writer = csv.writer(csvFile)
    writer.writerow(('Title', 'Date_and_Time', 'Replies', 'Views'))               #make a row of cells containing title, date_and_time, replies, and views
    for forum in forums:
        writer.writerow([forum['title'], forum['date_time'], forum['replies'], forum['view'] ])  #fill the rows with the values for title, date_and_time, replies, and views
        

forums = get_forum_data()                                                                      #construct data from from the cleaned list
forums_df = pd.DataFrame(forums).set_index('title')                               #convert list to data
print(forums_df)



