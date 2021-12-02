# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 12:57:23 2019

@author: jgalef
"""
"""The script websrcapes the daily flow rate for the EBMUD Mokelumne River at Woodbridge station.  It first 
checks the data file for the last date recorded.   If that date occurred before yesterday, 
the script goes to the EBMUD website, and grabs off the daily flow value in CFS for the Mokelumne River at 
Woodbridge station.   It  then opens a file and appends the value.  Script will do this for up to 7 days
of the latest data.  Website doesn't allow for more than 7 days."""


import pandas as pd
import datetime as dt
#import time

def updateFile():

    #Open the current data file. 
    file = open(r'Mokelumne at Woodbridge Flow Data.csv','r')
    
    #Get the last date of recorded data.
    lastDate = file.readlines()[-1].split(',')[0]
    
    #Close the file so that nothing gets overwritten.
    file.close()
    
    #Convert the last date to a date object.
    lastDate = dt.datetime.strptime(lastDate, '%m/%d/%Y').date()
    
    
    #Add 1 day to the last date, since that'll be the date to start getting new data.
    nextDate = lastDate + dt.timedelta(days=1)
    
    #Unfortunately, website only goes back 7 days, so set the lower bound of a loop.  This is in case there are missing dates.
    lastWeek = dt.date.today() - dt.timedelta(days=7)
    
    #If last date recorded is more than 7 days, make the date 7 days ago the lower bound.
    if nextDate < lastWeek: nextDate = lastWeek
    
    #Change for testing
    #nextDate = dt.date(2019,9,7)
    
    #Re-open the data file in append only mode.
    file = open(r'Mokelumne at Woodbridge Flow Data.csv','a')
    
    if (nextDate == dt.date.today()): print('\nFile is up to date as of {:%Y-%m-%d %H:%M:%S}.'.format(dt.datetime.now()))
    
    
    #Going back up to 7 days, increment daily to get the lastest data.
    while nextDate < dt.date.today():
           
        url = 'http://legacy.ebmud.com/if/daily-water-supply-report/WSE_DailyReport.asp?Date={}'.format(nextDate.strftime('%Y-%m-%d'))
    
        lst = pd.read_html(url)
    
        # succeeded=False
        # while not succeeded:
            
        #     try:
        #         lst = pd.read_html(url)
        #         succeeded=True
        #     except:
        #         print("Server temporarily down.  Sleeping for 2 hours and trying again.")
        #         time.sleep(7200)
                
                
        
        flow = lst[2][4][103].split(' ')[0]
        
        flow = flow.replace(',','')
        
        print('\n')
                                           
        if flow.isdigit(): 
            file.write(nextDate.strftime('%#m/%#d/%Y')+","+flow+'\n')
            print('The file was updated at {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        else:
            print('An attempt was unsuccessful at at {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
                                                 
        nextDate += dt.timedelta(days=1)
    
    file.close()


if __name__=="__main__":
    
    updateFile()
    
    # while True:
    #     updateFile()
        
    #     for i in range(86385):
    #         time.sleep(1)

