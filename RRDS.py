# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:34:15 2019

@author: jgalef
"""


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
import mytools 


pd.set_option('float_format','{:,.2f}'.format)

#Fish screen velocities for normal and variance periods.
varVelMax = 0.7
normalVelMax = 0.2


#Stage bounds for normal and increased periods.
increasedStageMin = 1.6
increasedStageMax = 2.1
normalStageMin = 1.6
normalStageMax = 1.9
floodStage = 2.6
drainStage = 2.3

#Enter starting and ending dates for Variance.
varStart = pd.Timestamp('9-14-2021')
varEnd = pd.Timestamp('10-21-2021')

#Enter starting and ending dates for stage increase.
stageStart = pd.Timestamp('8-17-2021')
stageEnd = pd.Timestamp('10-20-2021')

start = pd.Timestamp.now()-pd.DateOffset(days=7)
end = pd.Timestamp.now()


def getWQP(start,end):
       
    """Returns a dataframe of stage and operational data from WQP.  Only is called
    when data is to be retrieved from WQP.  This function does NOT use asycio, since
    it causes Spyder to lock up.  Discontinue use if Spyder ever fixes the problem."""
    
    #Specify columns to be returned when reading WQP Detailed Results table.    
    usecols = ['result_id','station_id','station_name','analyte_name','interval_name'] 
    
    #Read in WQP Detailed Results table.
    #Cannot share API from work.
    results = pd.read_csv(
        'API URL',
        sep='|',usecols=usecols)

    #Make a list of analytes to be fetched for the RRDS station.
    analytes=[f'Gate Position {i}' for i in range(1,9)]
    analytes.append('Stage Difference: Montezuma / Fishscreen')
    analytes.append('Velocity At Fish Screens')
    
    #Use analytes list to make a query to be used to retrieve all analytes for the RRDS station.
    query = "(station_id==RRDS & interval_name=='15 min' & (" + \
    ' | '.join([f"analyte_name=='{analyte}'" for analyte in analytes])+'))'
    
    #Add to the query information for retrieving stage data from MSL, ROR, and PEL.
    for station in [1171,1172,11120]:
        query = query + f"| (station_id=={station} & interval_name=='15 min' & analyte_name=='Stage')"
        
    #Use query to retrieve a list of Result IDs (rids) to be used for querying the data.
    rids = results.query(query)['result_id'].to_list()
    
    #Create an empty of list of URLs that will be used to retrieve the data.
    urls=[]

    #Using Result IDs in rids, build the URLs and append them to the urls list.
    #Cannot share API from work.
    for rid in rids:          
        url = 'API URL'\
        f'&resultid={rid}&start={start:%Y-%m-%d:%H:%M:%S}&end={end:%Y-%m-%d:%H:%M:%S}&version=1'     
        urls.append(url)
        
    #Create an empty list to hold the dataframes created from the responses.
    dfs=[]
    
    #Don't use the final 3 URLs because they're placeholders for when the stage data at ROR, PEL, and MSL
    #get transferred to the new RIDS.  Remember to ditch the first 3 URLS when this happens.
    for url in urls[:-3]:
        
        df = pd.read_csv(url,sep='|',index_col='time',parse_dates=['time'],na_values='null',usecols=['time','value'])
        dfs.append(df)
        
    df = pd.concat(dfs, axis=1)
    
    colNames = ['MSL','ROR', 'PEL', 'Gate1', 'Gate2', 'Gate3', 'Gate4', 'Gate5', 'Gate6', 'Gate7', 'Gate8', 
                'StageDiff', 'Velocity']
    
    
    df.columns = colNames
    
    df.loc[:,['MSL','ROR','PEL']] = df.loc[:,['MSL','ROR','PEL']] - 2.49

 
    #Create a column for the mean of the 8 Gate Positions.       
    df['GatesMean'] = df.loc[:,[f'Gate{i}' for i in range(1,9)]].mean(axis=1,skipna=True)    
    
    
    return df    


def getWQP_async(start,end):
    
    """Returns a dataframe of stage and operational data from WQP.  Only is called
    when data are to be retrieved from WQP.  This function USES asycio, but is on hold since
    it causes Spyder to lock up.  Use again if Spyder ever solves the issue.  It is quite
    a bit faster than getWQP()."""
    
    from io import StringIO
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    
    
    """Returns a dataframe of stage and operational data from WQP.  Only is called
    when data is to be retrieved from WQP."""
    
    #Specify columns to be returned when reading WQP Detailed Results table.    
    usecols = ['result_id','station_id','station_name','analyte_name','interval_name'] 
    
    #Read in WQP Detailed Results table.
    #Cannot share API from work.
    results = pd.read_csv('API URL',sep='|',usecols=usecols)

    #Make a list of analytes to be fetched for the RRDS station.
    analytes=[f'Gate Position {i}' for i in range(1,9)]
    analytes.append('Stage Difference: Montezuma / Fishscreen')
    analytes.append('Velocity At Fish Screens')
    
    #Use analytes list to make a query to be used to retrieve all analytes for the RRDS station.
    query = "(station_id==RRDS & interval_name=='15 min' & (" + \
    ' | '.join([f"analyte_name=='{analyte}'" for analyte in analytes])+'))'
    
    #Add to the query information for retrieving stage data from MSL, ROR, and PEL.
    for station in [1171,1172,11120]:
       query = query + f"| (station_id=={station} & interval_name=='15 min' & analyte_name=='Stage')"
        
    #Use query to retrieve a list of Result IDs (rids) to be used for querying the data.
    rids = results.query(query)['result_id'].to_list()
    
    #Create an empty of list of URLs that will be sent to the asyncio/aioattp API retrieval function.
    urls=[]

    #Using Result IDs in rids, build the URLs and append them to the urls list.
    #Cannot share API from work.
    for rid in rids:          
        url = 'API URL'\
        f'&resultid={rid}&start={start:%Y-%m-%d:%H:%M:%S}&end={end:%Y-%m-%d:%H:%M:%S}&version=1'     
        urls.append(url)

    #Send over URLs list to the fech_all function in mytools, and retrieve the text responses.
    #I eliminated the final 3 because they are empty Stage data holders for when Michael K. combines all
    #sensor data in one Result ID for each station/analyte.   
    
    #CHANGE THIS CODE BY ELIMINATING THE [:-3] PORTION WHEN MICHAEL K. SAYS THE WORK IS DONE.
    resps = asyncio.run(mytools.fetch_all(urls[:-3]))    

    #Create an empty list to hold the dataframes created from the responses.
    dfs=[]
        
    #First, loop through the stage data responses, since they were the first 3 Result IDs.
    cdecs=['MSL','ROR','PEL']       
    for resp,cdec in zip(resps[:3],cdecs):
       
       #Use StringIO to covert the text responses into a format that pd.read_csv() can use.
       df = pd.read_csv(StringIO(resp),sep='|',index_col='time',parse_dates=['time'],na_values='null',usecols=['time','value'])

       #Subtract off 2.49 to switch from NAVD88 to NGVD29.
       df['value'] = df['value']-2.49
       
       #Rename the columns from 'value' to the CDEC name of the station.
       df.rename(columns={'value':cdec},inplace=True)
       
       dfs.append(df)      
    
    #Second, loop through the remaining operational data from the RRDS station.
    for resp,analyte in zip(resps[3:],analytes):
       df = pd.read_csv(StringIO(resp),sep='|',index_col='time',parse_dates=['time'],na_values='null',usecols=['time','value'])
       df.rename(columns={'value':analyte},inplace=True)
       dfs.append(df)
       
    #Concatenate all the dataframes columnwise.
    df = pd.concat(dfs,axis=1)
    
    #Rename the Stage Differentential and Gate Opening columns to be shorter.
    df.rename(columns={'Velocity At Fish Screens':'Velocity','Stage Difference: Montezuma / Fishscreen':'StageDiff'},inplace=True)
    df.rename(columns=dict(zip([f'Gate Position {i}' for i in range(1,9)],[f'Gate{i}' for i in range(1,9)])),inplace=True)
 
    #Create a column for the mean of the 8 Gate Positions.       
    df['GatesMean'] = df.loc[:,[f'Gate{i}' for i in range(1,9)]].mean(axis=1,skipna=True)    
    
    return df    


def getWW_async(opsData):
    """Returns a dataframe of stage and operational data from CDEC and a Wonderware CSV file, respectively.  Only is 
    called when a CSV file is passed to createCharts1(opsData=path)."""    
    
    import asyncio
    from io import StringIO
    
    #Retrieve ops data from the Wonderware CSV file.
    df = mytools.getWonderwareData(opsData)
    
    #Round each datetime index element down to the closest 15-minute mark to sync with CDEC data.
    df.index = df.index.round('-15T')
    
    #Use the index of the dataframe to get teh start and end datetimes.
    start = df.index[0]
    end = df.index[-1]
    
    #Create an empty URL list and append on URLs to be used to retrieve stage data from CDEC.
    urls=[]
    
    urls.append(f'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=MSL&SensorNums=1&dur_code=E'\
            f'&Start={start:%Y-%m-%dT%H}''%3A'f'{start:%M}&End={end:%Y-%m-%dT%H}''%3A'f'{end:%M}')
                
    urls.append(f'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=ROR&SensorNums=6&dur_code=E'\
            f'&Start={start:%Y-%m-%dT%H}''%3A'f'{start:%M}&End={end:%Y-%m-%dT%H}''%3A'f'{end:%M}')      
        
    urls.append(f'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=PEL&SensorNums=1&dur_code=E'\
        f'&Start={start:%Y-%m-%dT%H}''%3A'f'{start:%M}&End={end:%Y-%m-%dT%H}''%3A'f'{end:%M}')        
        
    #Send URLs list to fetch_tools to retrieve the text responses.
    resps = asyncio.run(mytools.fetch_all(urls))
    
    #Create an empty list to hold dataframes created from the responses.
    cdfs=[]
    
    #Loop through the responses to create the dataframes and append them to cdfs.    
    for resp,cdec in zip(resps,['MSL','ROR','PEL']):
        
        #Use StringIO to covert the text responses into a format that pd.read_csv() can use.
        cdf = pd.read_csv(StringIO(resp),na_values='---',parse_dates=['DATE TIME'],
                          index_col='DATE TIME',usecols=['DATE TIME','VALUE'])
        
        #Subtract off 2.49 to switch from NAVD88 to NGVD29.
        cdf['VALUE'] = cdf['VALUE'] - 2.49
        
        #Rename the columns from 'VALUE' to the CDEC name of the station.
        cdf.rename(columns={'VALUE':cdec},inplace=True)
        
        #Rename index to match the name of the index from WQP.
        cdf.index.rename('time',inplace=True)
        
        cdfs.append(cdf)
    
    #Concatenate all the dataframes columnwise.  
    cdf = pd.concat(cdfs,axis=1)
    
    #Concatenate the Wonderware and CDEC dataframes.
    df = pd.concat([df,cdf],axis=1)
        
    return df


def getWW(opsData):
    """Returns a dataframe of stage and operational data from CDEC and a Wonderware CSV file, respectively.  Only is 
    called when a CSV file is passed to createCharts1(opsData=path)."""    
       
    #Retrieve ops data from the Wonderware CSV file.
    ww = mytools.getWonderwareData(opsData)
    
    #Round each datetime index element down to the closest 15-minute mark to sync with CDEC data.
    ww.index = ww.index.round('-15T')
    
    #Use the index of the dataframe to get the start and end datetimes.
    start = ww.index[0]
    end = ww.index[-1]
    
    msl = mytools.getCDECseries('MSL','1','E',start,end)-2.49
    ror = mytools.getCDECseries('ROR','6','E',start,end)-2.49
    pel = mytools.getCDECseries('PEL','1','E',start,end)-2.49
    
    # #Concatenate all the dataframes columnwise.  
    df = pd.concat([ww,msl,ror,pel],axis=1)
    
    df.dropna(inplace=True)
         
    return df
    
    

def createCharts1(opsData='WQP', start=start, end=end, outFile1='Flood Up 1.pdf', 
                  charts2=False, outFile2='Flood Up 2.pdf',predictions=False):
    
    """Creates the 4 charts used to monitor the performance of the RRDS.  The
    4 charts include the maximum and minimum stage targets, and the 15-minute
    stages at Montezuma Slough, Hammond Pond, and Pelican Point.   The stage
    data are retrieved from CDEC with the following respecitve station symbols:
    MSL, ROR, and PEL.   
    
    By default, the ops data are retrieved from WQP, but
    the user has the option of providing a CSV file retrieved from Wonderware.
    To use the CSV fucntionality, pass the full file path to the function
    with the 'opsData' argument.   
    
    The default time period is the last 7 days.  Enter specific start and 
    end dates if a different time range is desired.
    
    Charts2 is not created by default.  
    Pass in the argument, charts2=True, if the second chart is desired.
    """

    #Set font sizes
    yAxisLabelSizeStages = 9
    yAxisLabelSizeOthers = 8     
    yAxisTitleSizeStages = 10
    yAxisTitleSizeOthers = 8   
    legendLabelSize = 8  
    dataLabelSize = 8  

    #Get ops data from either WQP or CDEC/Wonderware.
    if opsData=='WQP':
        # df = getWQP_async(pd.Timestamp(start),pd.Timestamp(end))
        df = getWQP(pd.Timestamp(start),pd.Timestamp(end))
    else:
        df = getWW(opsData)        

    #Create columns for the Max Velocities and the Min and Max stage ranges.
    df['MaxVelocity'] = df.index.map(lambda x: varVelMax if x>=varStart and x<=varEnd else normalVelMax)
    
    df['MaxStage'] = df.index.map(lambda x: increasedStageMax if x>=stageStart and x<=stageEnd else normalStageMax)
    
    df['MinStage'] = df.index.map(lambda x: increasedStageMin if x>=stageStart and x<=stageEnd else normalStageMin)
    
    df['FloodStage'] = floodStage
    
    df['DrainStage'] = drainStage
    
    #Create the figure and two axes for the mins and average gate opening charts.
    fig1, (axStages,axVels,axGates,axDiff) = plt.subplots(4,1,sharex=True,
              figsize=(11,8.5), gridspec_kw={'height_ratios': [4, 1, 1, 1]})

    #Plot the timeseries data.
    axStages.plot(df['FloodStage'], label='Flood Stage', color='lightsteelblue')
    if not (pd.Timestamp.today() >= stageStart and pd.Timestamp.today() <= stageEnd):
        axStages.plot(df['DrainStage'], label='Drain Stage', color='plum')    
    axStages.plot(df['MaxStage'], label='Maximum Stage', color='red')
    axStages.plot(df['MinStage'], label='Minimum Stage',color='purple')
    axStages.plot(df['MSL'],label='Montezuma Slough',color='olivedrab')
    axStages.plot(df['ROR'],label='Hammond Pond',color='steelblue')
    axStages.plot(df['PEL'],label='Pelican Point',color='goldenrod')
    axDiff.plot(df['StageDiff'],label='MSL and Fish Screen Pond',color='purple')
    axVels.plot(df['Velocity'], color='slateblue', lw=1.5)    
    axVels.plot(df['MaxVelocity'],color='red',lw=1.5)    
    axGates.plot(df['GatesMean'], color='forestgreen',lw=1.5)    
        
    #Create the Stages legend.
    axStages.legend(frameon=True, loc="lower left",fontsize=legendLabelSize)
   
  #Add gridlines.
    lw=0.35
    axStages.grid(b=True, which='major', color='grey', linestyle='-', linewidth=lw)
    axDiff.grid(b=True, which='major', color='grey', linestyle='-', linewidth=lw)
    axVels.grid(b=True, which='major', color='grey', linestyle='-', linewidth=lw)
    axGates.grid(b=True, which='major', color='grey', linestyle='-', linewidth=lw)
 
  #Set the y-axis paramenters (if needed): labels, ranges, major locators, tick formatters, and tick sizes.

    axStages.set_ylabel('Stage (ft, NGVD29)',fontsize=yAxisTitleSizeStages)
    axStages.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    axStages.yaxis.set_tick_params(labelsize=yAxisLabelSizeStages)    
       
    axDiff.set_ylabel('Stage\nDifferential\n(ft)',labelpad=5, fontsize=yAxisTitleSizeOthers) 
    axDiff.set_ylim([-0.5,4])
    axDiff.yaxis.set_major_formatter(FormatStrFormatter('%.0f')) 
    axDiff.yaxis.set_major_locator(plt.AutoLocator()) 
    axDiff.yaxis.set_tick_params(labelsize=yAxisLabelSizeOthers)  

    axVels.set_ylabel('Velocity at the\nfish screens (fps)',labelpad=5, fontsize=yAxisTitleSizeOthers)
    axVels.set_ylim([-.05,0.8])
    axVels.yaxis.set_major_locator(plt.MaxNLocator(nbins=4, prune ='upper'))         
    axVels.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) 
    axVels.yaxis.set_tick_params(labelsize=yAxisLabelSizeOthers)  

    axGates.set_ylabel('Average gate\n opening (ft)',labelpad=5, fontsize=yAxisTitleSizeOthers)
    axGates.set_ylim([-.8,5.8])
    axGates.yaxis.set_major_locator(plt.MaxNLocator(7, prune='both'))
    axGates.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))        
    axGates.yaxis.set_tick_params(labelsize=yAxisLabelSizeOthers)    

  #Format the dates for x-axis.
    axDiff.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))   
    
    #Add in text labels for the final data point.
    axStages.text(df.index[0], df['MinStage'].iloc[0],f'{df["MinStage"].iloc[0]}  ', 
                  fontsize=dataLabelSize, verticalalignment='center', horizontalalignment='right')    
    
    axStages.text(df.index[0], df['MaxStage'].iloc[0],f'{df["MaxStage"].iloc[0]}  ', 
                  fontsize=dataLabelSize, verticalalignment='center', horizontalalignment='right')

    axStages.text(df.index[0], df['FloodStage'].iloc[0],f'{df["FloodStage"].iloc[0]}  ', 
                  fontsize=dataLabelSize, verticalalignment='center', horizontalalignment='right')

    if not (pd.Timestamp.today() >= stageStart and pd.Timestamp.today() <= stageEnd):
        axStages.text(df.index[0], df['DrainStage'].iloc[0],f'{df["DrainStage"].iloc[0]}  ', 
                      fontsize=dataLabelSize, verticalalignment='center', horizontalalignment='right')

    axStages.text(df['MSL'].dropna().index[-1], df['MSL'].dropna().iloc[-1],f'  {df["MSL"].dropna().iloc[-1]:.1f}', 
                  fontsize=dataLabelSize, verticalalignment='center', horizontalalignment='left',color='darkolivegreen')

    axStages.text(df['PEL'].dropna().index[-1], df['PEL'].dropna().iloc[-1],f'  {df["PEL"].dropna().iloc[-1]:.1f}', 
                  fontsize=dataLabelSize, verticalalignment='center', horizontalalignment='left',color='darkgoldenrod')

    axStages.text(df['ROR'].dropna().index[-1], df['ROR'].dropna().iloc[-1],f'  {df["ROR"].dropna().iloc[-1]:.1f}', 
                  fontsize=dataLabelSize, verticalalignment='center', horizontalalignment='left',color='royalblue')

    axDiff.text(df['StageDiff'].dropna().index[-1], df['StageDiff'].dropna().iloc[-1],
                f'  {df["StageDiff"].dropna().iloc[-1]:.1f}', fontsize=dataLabelSize, ha='left',verticalalignment='center')

    axGates.text(df['GatesMean'].dropna().index[-1], df['GatesMean'].dropna().iloc[-1],
                 f'  {df["GatesMean"].dropna().iloc[-1]:.1f}', fontsize=dataLabelSize, ha='left',verticalalignment='center')

    axVels.text(df['Velocity'].dropna().index[-1], df['Velocity'].dropna().iloc[-1],
                f'  {df["Velocity"].dropna().iloc[-1]:.2f}', fontsize=dataLabelSize, ha='left',verticalalignment='center')
 
    axVels.text(df.index[0],df['MaxVelocity'].iloc[0],f'{df["MaxVelocity"].iloc[0]}  ', fontsize=dataLabelSize, 
                verticalalignment='center', horizontalalignment='right')
    
    #Adjust the spacing between the subplots.
    fig1.subplots_adjust(hspace=0.07)

    #Save the figure.
    fig1.savefig(outFile1, dpi=200)

    if charts2: createCharts2(df,outFile2)
    
    if predictions: mytools.predictedTidesChart(29)


def createCharts2(df,outFile2):
    
    """Creates the second PDF showing stacked time-series plots of the 8 Gate Positions.
    To run this script, pass in the argument, charts2=True to the createCharts1() function."""
    
    #Set font sizes
    titleSize = 11
    xAxisLabelSize = 8.5
    yAxisLabelSize = 8
    legendLabelSize = 8.5
    dataLabelSize = 8
        
    #Create the 8 Gate Openings figure.
    fig2, axList = plt.subplots(8,1,sharex=True, sharey='col',figsize=(11,8.5))
          
    #Create gate labels for the legend.
    labels = ['Gate '+str(i) for i in range(1,9)]
    cols = ['Gate'+str(i) for i in range(1,9)]
    
    #Plot the timeseries data, add the legend, adjust the tick labels, add on the final data point label.
    for i in range(0,8):
        axList[i].plot(df[cols[i]], linewidth=1.65,label=labels[i], color='blue') 
        axList[i].legend(frameon=True,edgecolor='grey', facecolor='white', handlelength=0.5,loc='upper left',fontsize=legendLabelSize)
        axList[i].tick_params(axis='y', which='major', labelsize=yAxisLabelSize)   
        axList[i].grid(b=True, which='major', color='grey', linestyle='-', linewidth=0.20)
        axList[i].set_ylim([-.6,6])
        axList[i].yaxis.set_major_locator(plt.MaxNLocator(3))
        if (i<7): axList[i].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)  
        axList[i].text(df[cols[i]].dropna().index[-1], df[cols[i]].dropna().iloc[-1], 
                       f'   {df[cols[i]].dropna().iloc[-1]:.2f}', fontsize=dataLabelSize, ha='left', va='center')

    #Set the border line width for all charts.
    plt.rcParams['axes.linewidth'] = 1
       
    #Set the size of the x-axis date labels.    
    axList[-1].tick_params(axis='x', which='major', labelsize=xAxisLabelSize)
  
    #Change the format of the x-axis date labels.
    axList[-1].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))

    #Add the title.    
    axList[0].set_title('RRDS Gate Openings in feet\n',fontsize=titleSize)
     
    #Set the row space between the plots.
    fig2.subplots_adjust(hspace=0.2)

    fig2.savefig(outFile2, dpi=200)



def review(numWeeks, end=pd.Timestamp.now().normalize() ):
    """Creates a weekly chart1 going back from a specified date to the number 
    of weeks specified.  The default end date is today."""
    
    end = pd.Timestamp(end) 
    dates=[end]
    for i in range(1,numWeeks+1):
        dates.append(end - pd.DateOffset(weeks=i))
    dates.reverse()
    for i in range(len(dates)-1):
        createCharts1(start=dates[i],end=dates[i+1])    


def prepFiles():
    """Preps folder and files for following Flood Up Meeting.   
    1) Creates a new directory.
    2) Copies over packet and changes name to incorporate the new date.
    3) Copies over mintues and changes name to incorporate the new date.
    """
    
    import shutil, os
    
    rootDir = r'\Flood Up'
    
    lastWeek = f'{pd.Timestamp.today() - pd.offsets.Week(weekday=2):%Y_%m_%d}'
    
    thisWeek = f'{pd.Timestamp.today() + pd.offsets.Week(weekday=2):%Y_%m_%d}'
    
    lastWeekDir = os.path.join(rootDir, str(pd.Timestamp.today().year), lastWeek)
    
    thisWeekDir = os.path.join(rootDir, str(pd.Timestamp.today().year), thisWeek)
   
    if not os.path.exists(thisWeekDir):
        os.mkdir(thisWeekDir)
 
    lastWeekPacket = os.path.join(lastWeekDir,f'Floodup_{lastWeek}.docx')
     
    thisWeekPacket = os.path.join(thisWeekDir,f'Floodup_{thisWeek}.docx')

    if not os.path.exists(thisWeekPacket):
        shutil.copy(lastWeekPacket, thisWeekPacket)
    
    lastWeekMinutes = os.path.join(lastWeekDir,f'Floodup_{lastWeek} - minutes.docx')
    
    thisWeekMinutes = os.path.join(thisWeekDir,f'Floodup_{thisWeek} - minutes.docx')
    
    if not os.path.exists(thisWeekMinutes):
        shutil.copy(lastWeekMinutes, thisWeekMinutes)



if __name__=='__main__':
    
    """This script creates one or two PDFs for Flood Up.   The first PDF contains four stacked time-series charts.  
    The first chart shows the stages at MSL, ROR, and PEL, along with the minimum and maximum stage targets.   
    The second shows the estimated velocity at the fish screens.  The third is the average of the 8 gate openings.  
    The fourth plot shows the stage differential between MSL and the fish screen pond.        
    
    The second PDF shows eight stacked time-series charts of each of the gate openings.  If this plot is desired,
    pass charts2=True as an argument to createCharts1(charts2=True).
       
    The default setting plots the last 7 days.   If another time interival is desired, specify starting
    and ending dates, and pass them as follows, createCharts1(start='2020-12-1',end='2020-12-8').   This will
    only work when obtaining data from WQP.   
    
    If using data from a Wonderware CSV file, specify the full path of file with the opsData=<full path> arugment,
    and pass it to createCharts1(opsData).   No start and end dates are needed, as the CSV file will be used
    to determine start and end times.
    
    The default PDF locations will be in the root folder.  Pass in custom paths using the outFile1 and outFile2 
    arguments, such as charts1(outFile1=<full path>, outFile2=<full path>).
    
    Each year, change the global variables at the top that specify when the increased stages and
    increased fish screen velocities begin and end.
    
    To also generate a plot of Predicted Tides at Port Chicago, pass 'predictions=True':
    createCharts1(predictions=True)  
   
    """
    
    
    # Default is for Chart 1 only using the last 7 days using data from WQP:
    createCharts1()    
    
    #If using data directly from a Wonderware CSV file, enter the full path and pass it as an argument:
    opsData='opsdata.csv'
    # createCharts1(opsData)    
    # createCharts1(opsData,charts2=True)      
    
    
    #Prep folder and files for next week's meeting.
    # prepFiles()
    
    # To also plot Chart 2, pass in the argument, charts2=True:
    # createCharts1(charts2=True)         
    
    
    # To also generate a plot of Predicted Tides at Port Chicago, pass 'predictions=True.'
    # createCharts1(predictions=True)       
    
    #Just create the predictions chart.
    # mytools.predictedTidesChart(29)
    
    # Set a different time period using data from WQP here:       
    # createCharts1(start='2021-10-7',end='2021-10-20')     
        
        
    #Review backwards in weeks from a starting date. Returns a chart for each week.
    # review(3, '2021-10-20' )
    # review(2)
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
    
  