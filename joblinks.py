# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:25:17 2016

@author: Gerru.Kloppers
"""
import urllib
from bs4 import BeautifulSoup
import re
from time import gmtime, strftime
import sqlite3
import csv

date = strftime("%Y-%m-%d", gmtime())
print(date)

with open('jobsites.csv') as f:
    d = dict(filter(None, csv.reader(f)))


conn = sqlite3.connect('jobs.sqlite')
cur = conn.cursor()

# Setting up the tables, only done for 1st time
#cur.execute('''
#CREATE TABLE Joblinks (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
#new INTEGER, date TEXT, site TEXT, linktext TEXT, link TEXT)''')

new = 1

for website in d:    

    url = d[website]
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    
    print("!!!!!!!" + d[website] + "!!!!!!!!!!!!!")
    for tag in soup.find_all('a', href=True):
        link = tag.get('href')
        if link:
            #if re.match('.*www.*', link) or re.match('.*http.*', link):                        
            linktext = unicode(tag.contents[0])
                                 
            print(link)
            print(linktext)
            print("======") 

            cur.execute('SELECT link, date FROM Joblinks WHERE link = ? ', (link, ))
            row = cur.fetchone()
            if row is None:
                               
                cur.execute('''INSERT INTO Joblinks (date, new, site, linktext, link) 
                            VALUES ( ?, ?, ?, ?, ? )''', ( date, new, website, linktext, link ) )
            
            else:
                if row[1] != date:
                    cur.execute('''UPDATE Joblinks SET new = 0 WHERE link = ?''', (link, ))
            
    conn.commit()  

cur.close()