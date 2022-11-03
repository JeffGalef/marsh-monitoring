# -*- coding: utf-8 -*-
"""
Checks progress of USGS QC-ing their data.
Enter the Water Year below.

Estimated values are grouped into totals.  E.g., 'A:e', which stands for estimated approved,
has been lumped into Approved, 'A'.  

@author: jgalef
"""

from os.path import join
import mytools
import pandas as pd
from numpy import nan
# from io import StringIO
# import asyncio
# import nest_asyncio
# nest_asyncio.apply()

pd.set_option('float_format','{:,.0f}'.format)



def getInfo(wy):
    
    """Retrieves start and end datetimes, a list of Site Numbers,
    a dictionary linking Site Number to Station Name, and a dictionary
    linking Site Number to Parameter Number.
    
    Sample output for 3 stations:
        
        start: 2019-10-01 00:00:00 
        
        end:  2020-09-30 00:00:00 
        
        siteNumbers = ['11336600', '11325500', '11303500'] 
        
        numberMapName = {
                         '11336600': 'DELTA CROSS CHANNEL NR WALNUT GROVE', 
                         '11325500': 'MOKELUMNE R AT WOODBRIDGE', 
                         '11303500': 'SAN JOAQUIN R NR VERNALIS'
                        }
        
        numberMapParam = {
                          '11336600': '72137', 
                          '11325500': '00060', 
                          '11303500': '00060'
                          }

    """

    #Establish the start and end dates for desired Water Year.
    start = pd.Timestamp(year=wy-1, month=10, day=1)
    end = pd.Timestamp(year=wy, month=9, day=30)
    
    #List of official USGS station names.
    siteNames = ['DELTA CROSS CHANNEL NR WALNUT GROVE',
                    'MOKELUMNE R AT WOODBRIDGE',
                    'SAN JOAQUIN R NR VERNALIS',
                    'SACRAMENTO R AT FREEPORT',
                    'COSUMNES R AT MICHIGAN BAR',
                    'GEORGIANA SLOUGH NR SACRAMENTO R',
                    'YOLO BYPASS NR WOODLAND',
                    'THREEMILE SLOUGH NR RIO VISTA',
                    'DUTCH SLOUGH AT JERSEY ISLAND',
                    'SACRAMENTO R AT RIO VISTA',
                    'SAN JOAQUIN R AT JERSEY POINT']
    
    #List of USGS station numbers associated with list above.
    siteNumbers = '11336600,11325500,11303500,11447650,11335000,11447903,11453000,11337080,11313433,11455420,11337190'.split(',')      
    
    #List of USGS parameters to query.  
    #These will either be 00060 for flow in CFS,or 72137 for tidally-averaged flow in CFS.
    params = '72137,00060,00060,72137,00060,72137,00060,72137,72137,72137,72137'.split(',') 
    
    #Create dictionaries.
    numbersMapNames = dict(zip(siteNumbers, siteNames))
    numbersMapParams = dict(zip(siteNumbers, params))

    return(start,end,siteNumbers,siteNames,numbersMapNames,numbersMapParams)


    

def getDFs_async(wy):
    
    """This is the async version that I had to shelve because it causes Spyder to die.  I'll
    reinstate if Spyder fixes the problem.
    
    Retrieves a list of Data Frames of flow data from the USGS of stations used by Dayflow.
    
    Sample output for 2 stations:
        
                             site_no  SACRAMENTO R AT RIO VISTA Flag
        Date                                                
        2019-10-01  11455420                      9,360    A
        2019-10-02  11455420                      8,420    A
        2019-10-03  11455420                      8,890    A
        2019-10-04  11455420                     10,500    A
        2019-10-05  11455420                      9,650    A
        
                     site_no  SAN JOAQUIN R AT JERSEY POINT Flag
        Date                                                    
        2019-10-05  11337190                          3,900    A
        2019-10-06  11337190                          3,880    A
        2019-10-07  11337190                          1,080    A
        2019-10-08  11337190                         -2,420    A
        2019-10-09  11337190                          3,760    A
    
    """
    
    #Get global parameters.
    start,end,siteNumbers,siteNames,numbersMapNames,numbersMapParams = getInfo(wy)
    
    #Make an empty list to hold URLs.
    urls=[]
    
    #Loop through site numbers, create the URL, and append to list.
    for siteNumber in siteNumbers:
    
        url = f'https://waterdata.usgs.gov/nwis/dv?cb_{numbersMapParams[siteNumber]}='\
        f'on&format=rdb&site_no={siteNumber}&referred_module=' \
        f'sw&period=&begin_date={start:%Y-%m-%d}&end_date={end:%Y-%m-%d}'
        
        urls.append(url)
        
    #Retrieve the asynchronous responses.
    resps = asyncio.run(mytools.fetch_all(urls))
 
    #Make an empty list to hold dataframes.
    dfs = []    
    
    #Loop through responses and site names.
    for resp,siteName in zip(resps,siteNames):
        
        #Create the dataframe with response data.
        df = pd.read_csv(StringIO(resp),comment='#',sep='\t',header=1,
                     names=['USGS','site_no','Date',siteName,'Flag'],
                     usecols=['Date','site_no',siteName,'Flag'],parse_dates=['Date'],
                     index_col='Date')
        
        dfs.append(df)

    return dfs

def getDFs(wy):
    
    """Retrieves a list of Data Frames of flow data from the USGS of stations used by Dayflow.
    
    Sample output for 2 stations:
        
                             site_no  SACRAMENTO R AT RIO VISTA Flag
        Date                                                
        2019-10-01  11455420                      9,360    A
        2019-10-02  11455420                      8,420    A
        2019-10-03  11455420                      8,890    A
        2019-10-04  11455420                     10,500    A
        2019-10-05  11455420                      9,650    A
        
                     site_no  SAN JOAQUIN R AT JERSEY POINT Flag
        Date                                                    
        2019-10-05  11337190                          3,900    A
        2019-10-06  11337190                          3,880    A
        2019-10-07  11337190                          1,080    A
        2019-10-08  11337190                         -2,420    A
        2019-10-09  11337190                          3,760    A
    
    """
    
    #Get global parameters.
    start,end,siteNumbers,siteNames,numbersMapNames,numbersMapParams = getInfo(wy)
       

    
    #Make an empty list to hold URLs.
    dfs=[]
    
    #Loop through site numbers, create the URL, and append to list.
    for siteNumber in siteNumbers:
    
        url = f'https://waterdata.usgs.gov/nwis/dv?cb_{numbersMapParams[siteNumber]}='\
        f'on&format=rdb&site_no={siteNumber}&referred_module=' \
        f'sw&period=&begin_date={start:%Y-%m-%d}&end_date={end:%Y-%m-%d}'
        
        siteName = numbersMapNames[siteNumber]
    
        df = pd.read_csv(url,comment='#',sep='\t',header=1,
                     names=['USGS','site_no','Date',siteName,'Flag'],
                     usecols=['Date','site_no',siteName,'Flag'],parse_dates=['Date'],
                     index_col='Date')
        
        
        dfs.append(df)
        
        

    return dfs




def getData(wy,outFile):
    
    """Creates a CSV of the USGS flow data used in Dayflow.  Pass in the Water Year,
    and the full path of the output file."""
    
    # pd.set_option('display.precision',2)    
    
    #Get global parameters.
    start,end,siteNumbers,siteNames,numbersMapNames,numbersMapParams = getInfo(wy)
     
    #Retrieve the list of dataframes.
    dfs = getDFs(wy)
    
    
    for df in dfs:

        #Only retrieve flow data.
        if not df.empty:
            df = df.drop(columns=['site_no','Flag'],inplace=True)
   
    df = pd.concat(dfs,axis=1)
    
    if 'site_no' in df.columns:
        df.drop(columns=['site_no','Flag'],inplace=True)
    
    df.fillna(value=0.0,inplace=True)
           
    #Save to a user-specified CSV file.
    df.to_csv(outFile)
    

def checkProgress(wy):
    
    """Checks the QC progress of the USGS for stations used by Dayflow.  The results
    are printed to the screen.  Pass in the Water Year.
    
    Sample output:
        
        Flag                                  A   P   M
        DELTA CROSS CHANNEL NR WALNUT GROVE 153 209   4
        MOKELUMNE R AT WOODBRIDGE             0   0 366
        SAN JOAQUIN R NR VERNALIS           134 232   0
        SACRAMENTO R AT FREEPORT            135 231   0
        COSUMNES R AT MICHIGAN BAR            3 363   0
        GEORGIANA SLOUGH NR SACRAMENTO R    226 140   0
        YOLO BYPASS NR WOODLAND             366   0   0
        THREEMILE SLOUGH NR RIO VISTA       273  84   9
        DUTCH SLOUGH AT JERSEY ISLAND       179 108  79
        SACRAMENTO R AT RIO VISTA           203 148  15
        SAN JOAQUIN R AT JERSEY POINT       324  14  28
    
    """
    
    pd.set_option('display.precision',0) 
    
    #Get global parameters.
    start,end,siteNumbers,siteNames,numbersMapNames,numbersMapParams = getInfo(wy)    
    
    #Retrieve the dataframes.
    dfs = getDFs(wy)
    
    #Make an empty list to hold grouped-by dataframes.
    gs=[]
    
    #Loop through site numbers, retrieve data, groubpy the QC flags, and append to gs.
    for df in dfs:
        
        df.drop(columns=['site_no'],inplace=True)

        g = df.groupby(by='Flag').count()
        
        gs.append(g)    
        
    df = pd.concat(gs,axis=1)    
    
    #Transpose for ease of reading.
    df = df.transpose()
    
    #Replace nans so they can be added in the next step.
    df.replace(nan,0,inplace=True)
    
    #Combine normal and approved values.
    df['A'] = df['A'] + df['A:e']
    df['P'] = df['P'] + df['P:e']    
    
    #Drop the esimated columns.
    df.drop(['A:e','P:e'],axis=1,inplace=True)    
    
    #Create a column of missing values.
    df['M'] = (end - start).days+1 - df['A'] - df['P']
        
    #Print out results.
    print(df.sort_index())



def missingData():
    
    """Creates a text file of continuous blocks of missing USGS data.
    
    Sample output:
        
        Sacramento River At Rio Vista
        2019-10-15
        2019-10-25
        2020-09-05
        2020-09-08
                
        San Joaquin River at Jersey Point
        2019-10-01
        2019-10-04
        2019-11-13
        2019-11-19
        2019-12-01
        2019-12-11
        2020-07-16
        2020-07-21
    
    """
    
    dfs = getDFs(wy)
    
    
    start,end,siteNumbers,siteNames,numbersMapNames,numbersMapParams = getInfo(wy)  
    
    newCols = ['Delta Cross Channel near Walnut Grove', 'Mokelumne River At Woodbridge', 
               'San Joaquin River near Vernalis', 'Sacramento River At Freeport', 
               'Cosumnes River At Michigan Bar', 'Georgiana Slough near Sacramento River', 
               'Yolo Bypass near Woodland', 'Threemile Slough near Rio Vista', 
               'Dutch Slough at Jersey Island', 'Sacramento River At Rio Vista', 
               'San Joaquin River at Jersey Point']

    #Make a dictionary with more readable station names.
    mapNames = dict(zip(siteNames,newCols))
    

    #Open a text file for writing output.
    with open(missingFile,'w') as file:   
    
        #Loop through dataframes.
        for df in dfs:
            
            #Output the name of the station.
            file.write(mapNames[df.columns[1]]+'\n')
            
            #If no data, output start and end date of WY.
            if df.empty:
                file.write(f'{pd.Timestamp(wy-1,10,1):%m-%d-%Y}'+'\n')
                file.write(f'{pd.Timestamp(wy,9,30):%m-%d-%Y}'+'\n')        
    
            else:
                
                #Create an index of dates where there were nulls.
                idx = df[df['Flag'].isnull()].index   
                
                #Append on the final date of the WY to make things work properly.
                idx = idx.append(df['Flag'].index[-1:])
    
                #Loop through index to output start and end dates to null blocks.
                for i in range(len(idx)-1):
                    if idx[i+1]!=idx[i]+pd.DateOffset(days=1):
                        file.write(f'{idx[i]:%m-%d-%Y}'+'\n')
                    elif idx[i-1]!=idx[i]-pd.DateOffset(days=1):
                        file.write(f'{idx[i]:%m-%d-%Y}'+'\n')
            
            #Output newline for start of next station.
            file.write('\n')

        

# if __name__=='__main__':
    
    """Contains two scripts pertaining to USGS data used by Daflow. See individual
    docstrings for more information.
       
    *  getData(wy,outFile) retrieves USGS flow data and creates an output file.
    
    *  checkProgress(wy) checks the QC status of USGS flow data and prints a summary to the screen.
    
    SET THE NECESSARY USER-DEFINED ARGUMENTS BELOW.    
    
    """

#ENTER WATER YEAR HERE:
wy = 2021


#ENTER ROOT DIRECTORY FOR DAYFLOW:
rootDir = '//cnrastore-des/des001/DES_0340 - EP&I Branch/MARSH_WQ/Projects/DAYFLOW'


#CHANGE DEFAULT FILE PATH FOR USGS DATA IF DESIRED:
outFile = join(rootDir,f'WY{wy}/Input Data/USGS.csv')


#CHANGE DEFAULT FILE PATH FOR MISSING USGS DATA IF DESIRED:
missingFile = join(rootDir,f'WY{wy}/Input Data/USGSmissing.txt')


#Check the progress of the USGS on posting flow data:
# checkProgress(wy)


#Create a file of continous dates of missing flow data for each station:
missingData()    

#CREATE A CSV OF DATA READY TO ADD TO THE MAIN DAYFLOW INPUT FILE.
# getData(wy,outFile)

    
    
    
    
    
    
    
    
    
    