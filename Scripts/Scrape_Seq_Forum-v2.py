'''
Web-scrape seqanswers forum and extract number of views, corresponding date, and replies.
Save data to a .csv file
url = 'http://seqanswers.com/forums/forumdisplay.php?f=19'   
Postings since last year (365 days)
'''
import requests
import csv
import re
import pandas as pd
from bs4 import BeautifulSoup

#Reading recent 30 postings posted in the past 365 days; very few old postings displayed in page 2.
url = 'http://seqanswers.com/forums/forumdisplay.php?s=&f=19&page=1&pp=30&sort=lastpost&order=desc&daysprune=365'
req = requests.get(url)                                                                        #fetch url
soup = BeautifulSoup(req.text, 'html5lib')                                                     #parser html5lib

'''
Funtion extracts body from forum
Cleaning data by removing/substituting the empty/new lines and tabs
new_variable = re.sub('\n', '', old_variable)   # Remove the '\n' new-line
new_variable = re.sub('\t', '', old_variable)   # Remove the '\t' tab
'''
def get_forum_data():
    
    forums = []                                                                       #instantiate an empty list
    trs = soup.find('tbody', {'id': 'threadbits_forum_19'}).findAll("tr")             #extract all "<TR>" tags below "<TBODY>" tage that has element "id = threadbits_forum_1"

    for i in trs:
        tds = i.findAll("td")                                                         #extract all cells in trs 
        forum_data = dict()                                                           #instantiate a dictionary
        
        #Fetch forum_id and create url link
        forum_id = tds[0].get('id')
        forum_id = re.sub('td_threadstatusicon_','',forum_id)
        forum_data['forum_id'] = forum_id
        forum_link="http://seqanswers.com/forums/showthread.php?t=" + forum_id
        forum_data['forum_link'] = forum_link

        #Fetch entire title
        title = tds[2].text.strip()
        title = re.sub('\t\t\t\t',' - ',title)                                         #remove the '\t' tab
        title = re.sub('[\n,\t]','',title)                                             #remove the [\n,\t] new-line with tab
        forum_data['title'] = title                                                    #replace old title with the new, cleaned title

        #Date and Time
        date_time = tds[3].text.strip()                                                #fetch data from 3rd column contains date-time and user-name
        date_time = re.sub('\n\t\t\t',' - ',date_time)                                 #remove the '\n' and '\t's
        forum_data['date_time'] =  date_time                                           #replace old date_time column with the new,cleaned date_time
        
        #No. of Replies
        forum_data['replies'] = tds[4].find('a').text.strip()                          #extract number of replies column
        
        #No. of Views
        view  = tds[5].text.strip()                                                    #extract number of views column
        forum_data['view'] = view                                                      #add the number of views column to dict  
        
        forums.append(forum_data)                                                      #append forum_data dict to list, forums
        
    return forums

#construct a data from from the cleaned list
forums = get_forum_data()
forums_df = pd.DataFrame(forums).set_index('title')                                    #sort data by title
print(forums_df)
forums_df.to_csv("forums_title_df.csv")                                                #write data frame to .csv file

df = pd.read_csv('forums_title_df.csv')                                                #read the .csv file for data visualization
print(df.head())

#Data visualization. Using matplotlib, create a WordCloud of Title words

import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

stopwords = set(STOPWORDS)                                                              #ignore stopwords (i.e "the”, “a”, “an”, “in”)
stopwords.add("Feb, 9th, 28th")                                                         #append dates to stopwords

data = pd.read_csv("C:/SEQ_Answers/forums_title_df.csv")                                #store results in .csv file into a varaiable

#create wordcloud object with customized settings
wordcloud = WordCloud(font_path ='c:/SEQ_Answers/fonts/SourceHanSerifK-Light.otf',
                      background_color='white',
                      stopwords=stopwords, max_words=350,
                      max_font_size=45, random_state=22
                     ).generate(str(data['title']))
 
#print(wordcloud)
fig = plt.figure(1)                                                                     #create figure using matplotlib
plt.imshow(wordcloud)                                                                   #display generated figure
plt.axis('off')                                                                         #turn off axis
#plt.show()
fig.savefig("C:/SEQ_Answers/forums_title_words.png", dpi=2400)                          #save the plotted figure as a .png file with a resolution of 2400

'''
References:
https://github.com/amueller/word_cloud/blob/master/examples/simple.py
https://stackoverflow.com/questions/44750574/creating-wordcloud-using-python
'''



