# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 08:05:08 2019

@author: jgalef
"""



import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
import mytools
import os
from mytools import getStandardsDetailed


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 5)

standards = {1:12.5, 2:8, 3:8, 4:11, 5:11, 6:'No Standard', 7:'No Standard', 8:'No Standard', 9:'No Standard', 10:19, 11:15.5, 12:15.5}  

standardsEastern, normalStandardsWestern, deficiencyStandardsWestern = getStandardsDetailed()

#Change these if the boxes and title do not align properly.
titleDiv = 0.26
boxDiv = 9.25


def placementGrid(ax,x0,xL,y0,yL):
    """This adds percentage labels to the x and y axes.  It is used to position items on the map,
    such as arrows, boxes, and labels."""
    import matplotlib.ticker as ticker
    ax.axis('on')  
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(4000))
    vals = ax.get_yticks()    
    ax.set_yticklabels(['{:,.2}'.format((y-y0)/(yL-y0)) for y in vals])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5000))
    vals = ax.get_xticks()    
    ax.set_xticklabels(['{:,.2}'.format((x-x0)/(xL-x0)) for x in vals])  



def addTitle(ax, endDate, deficiencyPeriod):   
    """Adds a title to the Monthly Average chart."""
    
  
    #Get the standard for the previous month.   
    ESstandard = standardsEastern[endDate.month]     
    
    if deficiencyPeriod==True:
        WSstandard = deficiencyStandardsWestern[endDate.month]
    else:
        WSstandard = normalStandardsWestern[endDate.month]

    #Add the standard to the figure.    
    if np.isnan(ESstandard): 
        ESstandardStatement = f"No Salinity Standard for {endDate:%B}"        
    else:
        ESstandardStatement = f"Eastern Stations Standard = {ESstandard} mS/cm" 

    if np.isnan(WSstandard): 
        WSstandardStatement = f"No Salinity Standard for {endDate:%B}"      
    else:
        WSstandardStatement = f"Western Stations Standard = {WSstandard} mS/cm" 


    #Set the margins and add the title to the map.    
    leftTitleMargin=-0.1
    topTitleMargin=1.01
    lineSpace=0.035
          
    ax.text(leftTitleMargin,topTitleMargin,"Delta Tributary ", fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes) 
    ax.text(leftTitleMargin + titleDiv,topTitleMargin,"Monthly Average", fontsize=20,fontfamily='calibri',weight='bold',ha='left',va='top',transform=ax.transAxes)     
    ax.text(leftTitleMargin,topTitleMargin-lineSpace,"Flows & Suisun Marsh Monthly", fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes) 
    ax.text(leftTitleMargin,topTitleMargin-2*lineSpace,"Mean High Tide Salinities as of", fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)
    ax.text(leftTitleMargin,topTitleMargin-3*lineSpace,endDate.strftime('%B %Y'), weight='bold', style='italic',fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     
    ax.text(leftTitleMargin,topTitleMargin-6*lineSpace,"(Flows in CFS)",fontsize=14,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     
    if 'No' in ESstandardStatement:
        ax.text(leftTitleMargin,.001,ESstandardStatement, weight='bold', style='italic',fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     
    else:
        ax.text(leftTitleMargin,.01,ESstandardStatement+'\n'+WSstandardStatement, weight='bold', style='italic',fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     

def addTitle2(ax,yesterday):   
    """Adds a title to the Daily Average chart."""
    
    #Get the standard for the previous month.   
    ESstandard = standardsEastern[yesterday.month]     
    
    if deficiencyPeriod==True:
        WSstandard = deficiencyStandardsWestern[yesterday.month]
    else:
        WSstandard = normalStandardsWestern[yesterday.month]

    #Add the standard to the figure.    
    if np.isnan(ESstandard): 
        ESstandardStatement = f"No Salinity Standard for {yesterday:%B}"        
    else:
        ESstandardStatement = f"Eastern Stations Standard = {ESstandard} mS/cm" 

    if np.isnan(WSstandard): 
        WSstandardStatement = f"No Salinity Standard for {yesterday:%B}"      
    else:
        WSstandardStatement = f"Western Stations Standard = {WSstandard} mS/cm"
 
    leftTitleMargin=-0.1
    topTitleMargin=1.01
    lineSpace=0.035
          
    #Set the margins and add the title to the map. 
    ax.text(leftTitleMargin,topTitleMargin,"Delta Tributary ", fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     
    ax.text(leftTitleMargin + titleDiv,topTitleMargin,"Daily Average", fontsize=20,fontfamily='calibri',weight='bold',ha='left',va='top',transform=ax.transAxes)     
    ax.text(leftTitleMargin,topTitleMargin-lineSpace,"Flows & Suisun Marsh Daily", fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes) 
    ax.text(leftTitleMargin,topTitleMargin-2*lineSpace,"Mean High Tide Salinities as of", fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)
    ax.text(leftTitleMargin,topTitleMargin-3*lineSpace,yesterday.strftime('%B %#d, %Y'), weight='bold', style='italic',fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes) 
    # ax.text(leftTitleMargin,topTitleMargin-4*lineSpace,standardStatement, weight='bold', style='italic',fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     
    ax.text(leftTitleMargin,topTitleMargin-6*lineSpace,"(Flows in CFS)",fontsize=14,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes) 
    if 'No' in ESstandardStatement:
        ax.text(leftTitleMargin,.001,ESstandardStatement, weight='bold', style='italic',fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     
    else:
        ax.text(leftTitleMargin,.01,ESstandardStatement+'\n'+WSstandardStatement, weight='bold', style='italic',fontsize=20,fontfamily='calibri',ha='left',va='top',transform=ax.transAxes)     


def createBackground(ax):
    """Creates the background, including the Delta and Suiusn Marsh, and the flow labels."""
    
    #Set the bounding box coordinates.  
    x0, xL = 576400, 655000
    y0, yL = 4171000, 4274000
    
    #Use Geopandas to read the hydrography shapefile.
    mapDF = gpd.read_file(r'data_GIS\delta_marsh_remove100m.shp')

    #Use a query to remove distracting water bodies.
    mapDF= mapDF.query("HNAME not in 'SOUTH FORK PUTAH CREEK' and HNAME not in 'PUTAH CREEK'" 
                       "and HNAME not in 'LAKE BERRYESSA' and HNAME not in 'LOS VAQUEROS RESERVOIR'")                 

    #Plot the shapefile.
    mapDF.plot(color=('lightsteelblue'), edgecolor='lightsteelblue', ax=ax, zorder=0)

    #Use Geopandas to read the stations shapefile.
    stationsDF = gpd.read_file(r'data_GIS\stations.shp')

    #Use a query to separate the compliance from the monitoring stations for colorizing.    
    stationsCompliance = stationsDF.query("type == 'compliance'")

    stationsCompliance.plot(color='lightcoral', edgecolor='black',ax=ax)
    
    stationsMonitoring = stationsDF.query("type == 'monitoring'")
    
    stationsMonitoring.plot(color='lightgreen',edgecolor='black',ax=ax)

    #Assign the bounding box coordinates to the axes limits.
    ax.set_xlim([x0,xL])
    ax.set_ylim([y0,yL])

    #Add the Flow labels and arrows to the map.
    arrowColor = 'steelblue'
    
    #Sacramento River label and arrow.
    ax.text(x=0.71,y=0.9,s='        ',transform=ax.transAxes,ha='center',rotation=90,
                bbox=dict(boxstyle='larrow,pad=0.01', facecolor=arrowColor,edgecolor='black'))    
    ax.text(x=0.805,y=0.9,s='Sacramento\nRiver',transform=ax.transAxes,ha='center')

    #Yolo Bypass label and arrow.
    ax.text(x=0.48,y=0.77,s='        ',transform=ax.transAxes,ha='center',rotation=90,
                bbox=dict(boxstyle='larrow,pad=0.01', facecolor=arrowColor,edgecolor='black'))    
    ax.text(x=0.48,y=0.83,s='Yolo\nBypass',transform=ax.transAxes,ha='center')


    #Eastside Streams label and arrow.
    ax.text(x=0.84,y=0.53,s='        ',transform=ax.transAxes,ha='center',rotation=0,
                bbox=dict(boxstyle='larrow,pad=0.01', facecolor=arrowColor,edgecolor='black'))    
    ax.text(x=0.81,y=0.56,s='Eastside Streams',transform=ax.transAxes,ha='left')

    #San Joaquin River label and arrow.
    ax.text(x=1.03,y=-0.0,s='        ',transform=ax.transAxes,ha='center',rotation=-55,
                bbox=dict(boxstyle='larrow,pad=0.01', facecolor=arrowColor,edgecolor='black'))    
    ax.text(x=1.03,y=0.06,s='San\nJoaquin\nRiver',transform=ax.transAxes,ha='center')
    
    
    #SWP and CVP labels and arrow.
    ax.text(x=0.52,y=0.13,s='        ',transform=ax.transAxes,ha='center',rotation=90,
                bbox=dict(boxstyle='larrow,pad=0.01', facecolor=arrowColor,edgecolor='black'))    
    ax.text(x=0.07,y=0.13,s='SWP Exports',transform=ax.transAxes,ha='left')
    ax.text(x=0.32,y=0.13,s='CVP Exports',transform=ax.transAxes,ha='left')    
    

    #Delta Outflow label and arrow.
    ax.text(x=0.5,y=0.24,s='        ',transform=ax.transAxes,ha='center',rotation=0,
                bbox=dict(boxstyle='larrow,pad=0.01', facecolor=arrowColor,edgecolor='black'))    
    ax.text(x=0.50,y=0.27,s='Delta\nOutflow',ha='center',transform=ax.transAxes)



def createFlowBox(ax,x,y,flow,diff):
    """Create a two-column box for the current flow and the change."""
    
    
    box = ax.text(x=x,y=y,s='Current:\n{:,.0f}'.format(flow),transform=ax.transAxes,
                  ha='center',linespacing=2,fontsize=10,bbox=dict(edgecolor='black',fc='None',pad=5,linewidth=1.4))    
    boxWidth = box.get_bbox_patch().get_width()/boxDiv
    ax.text(x=x+boxWidth,y=y,s='Change:\n{:,.0f}'.format(diff),transform=ax.transAxes,
            ha='center',linespacing=2,fontsize=10,bbox=dict(edgecolor='black',fc='None',pad=5,linewidth=1.4))     


def getFlows(symbol, sensorNumber, startDate, endDate):
    """Enter a CDEC symbol and its sensor number, and get back the previous month's daily
    flow average, and the change from two months ago."""

    #Read the flow data from CDEC from the first of the month two months ago, through the end of last month.   
    df = mytools.getCDECseries(symbol, sensorNumber, 'D', startDate, endDate)
    
    #Calculate the monthly means.
    means = df.resample('M').mean()
    


    #Return the mean from the previous month.
    lastMonthMean = means.iloc[1]
    
    #Take the difference between previous month's mean, and the mean of two month's ago.
    monthlyDiff = means.iloc[1] - means.iloc[0]
   
    #If all NULL "---" values, replace the values with 0 for computational purposes.
    if np.isnan(lastMonthMean): lastMonthMean=0
    if np.isnan(monthlyDiff): monthlyDiff=0    

    return lastMonthMean, monthlyDiff



def getFlows2(symbol, sensorNumber, yesterday, startDate, endDate):
    """Gets yesterday's average flow, and the difference between it and the average of the previous month."""

    #Read the flow data from CDEC for the previous month, from day 1 through the end.
    df = pd.read_csv(r'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?'
                     'Stations={}&SensorNums={}&dur_code=D&Start={}&End={}'.format(symbol,sensorNumber,str(startDate),
                      str(endDate)),na_values='---')   

    #Convert the date string to datetime format.     
    df['DATE TIME'] = pd.to_datetime(df['DATE TIME'])

    #Set the datetime as the index.      
    df.set_index(['DATE TIME'],inplace=True)    
    
    

    #Return the mean from the previous month.    
    lastMonthMean = df['VALUE'].mean()
    
    #If all NULL "---" values, replace the values with 0 for computational purposes.    
    if np.isnan(lastMonthMean): lastMonthMean=0    
       
    #Read the flow data from CDEC for yesterday.
    df = pd.read_csv(r'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?'
                     'Stations={}&SensorNums={}&dur_code=D&Start={}&End={}'.format(symbol,sensorNumber,str(yesterday),
                      str(yesterday)),na_values='---')   
               
    #Assign value from dataframe to variable.
    yesterFlow = df['VALUE'].iloc[0]
    
    #If NULL "---" value, replace the value with 0 for computational purposes.
    if np.isnan(yesterFlow): yesterFlow=0    
    
    #Compute the difference between yesterday's flow and the average of the previous month.
    flowDiff = yesterFlow - lastMonthMean
    
    return yesterFlow, flowDiff
    
    

def getSacFlows(startDate, endDate):
    """Compute the last month's average, plus difference with the month prior for the Sac River.  
    This is the sum of the Sac River at Freeport, plus effluent from the Sac Regional WWTP."""
    
    #Calculate monthly average of daily flow data, and change from previous month for Sacramento River.
    lastMonthMeanFPT, monthlyDiffFPT = getFlows('FPT', '20', startDate, endDate)  

    #Get data from the Sac Regional WWTP, which only gives monthly values.
    df = pd.read_csv(r'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?'
                     'Stations=SPE&SensorNums=20&dur_code=M&Start={}&End={}'.format(str(startDate),
                      str(endDate)),na_values='---')

    #Get last month's flow average, and compute its difference with the month before that.
    lastMonthSPE, monthlyDiffSPE = df['VALUE'].iloc[1], df['VALUE'].iloc[1]-df['VALUE'].iloc[0]

    #Add the data for FPT and SPE
    lastMonthMean = lastMonthMeanFPT + lastMonthSPE
    monthlyDiff = monthlyDiffFPT + monthlyDiffSPE

    return lastMonthMean, monthlyDiff
       


def getSacFlows2(yesterday, startDate, endDate):
    """Get yesterday's flow, plus the difference with the month prior for the Sac River.  
    This is the sum of the Sac River at Freeport, plus effluent from the Sac Regional WWTP."""
        
    #Calculate daily flow average, and change from previous month for Sacramento River.
    yesterFlowFPT, flowDiffFPT = getFlows2('FPT','20', yesterday, startDate, endDate)  
    
    #Get values for FPT.
    url = r'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=SPE&SensorNums=20&dur_code=M&Start={}&End={}'\
    .format(str(startDate),str(endDate))
    
    df = pd.read_csv(url,na_values='---')    
    
    #Get values for SPE.
    url = r'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=SPE&SensorNums=20&dur_code=M&Start={}&End={}'\
    .format(str(endDate),str(yesterday))   

    df2 = pd.read_csv(url,na_values='---')   
    
    #Calculate daily flow average, and change from previous month for SPE.
    yesterFlowSPE, flowDiffSPE = df2['VALUE'].iloc[0], df2['VALUE'].iloc[0]-df['VALUE'].iloc[0]

    #Sum the FPT and SPE values.
    yesterFlow = yesterFlowFPT + yesterFlowSPE
    flowDiff = flowDiffFPT + flowDiffSPE

    return yesterFlow, flowDiff


def getYoloFlows(startDate, endDate):
    """Compute last month's average, plus the difference with the month prior for the Yolo Bypass.  
    This is the sum of the Yolo Bypass at Rumsey Bridge, plus any flow over the Fremont Weir."""
    
    lastMonthMeanRUM, monthlyDiffRUM = getFlows('RUM', '41', startDate, endDate) 
    lastMonthMeanFRE, monthlyDiffFRE = getFlows('FRE', '41', startDate, endDate)     

    lastMonthMean=lastMonthMeanRUM+lastMonthMeanFRE
    monthlyDiff = monthlyDiffRUM+monthlyDiffFRE
    
    return lastMonthMean, monthlyDiff   



def getYoloFlows2(yesterday, startDate, endDate):
    """Compute last month's average, plus the difference with the month day for the Yolo Bypass.  
    This is the sum of the Yolo Bypass at Rumsey Bridge, plus any flow over the Fremont Weir."""
    
    yesterFlowRUM, flowDiffRUM = getFlows2('RUM', '41', yesterday, startDate, endDate) 
    yesterFlowFRE, flowDiffFRE = getFlows2('FRE', '41', yesterday, startDate, endDate)     

    yesterFlow=yesterFlowRUM+yesterFlowFRE
    flowDiff = flowDiffRUM+flowDiffFRE
    
    return yesterFlow, flowDiff 





def getESSflows(startDate, endDate):
    """Compute last month's average, plus the difference with the month prior for the Eastside Streams.  
    This is the sum of the Cosumnes River at Michigan Bar, the Mokulmne River at Woodbridge, and releases
    from New Hogan Dam into the Calaveras River."""    
    
    
    #For Cosumnes River at Michigan Bar.
    lastMonthMeanMHB, monthlyDiffMHB = getFlows('MHB', '41', startDate, endDate) 
    
    #For reservoir releases from New Hogan Lake into the Calaveras River.
    lastMonthMeanNHG, monthlyDiffNHG = getFlows('NHG', '23', startDate, endDate)    
    
    #WBR isn't on CDEC, so these data come from a CSV file made from another script.
    path=r'Mokelumne at Woodbridge Flow Data.csv'
    df = pd.read_csv(path)
    
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df.set_index(['Date'], inplace=True)
    
    means = df[startDate : endDate]['Flow'].groupby(by=[pd.Grouper(freq='M')]).mean()
    

    lastMonthMeanWBR, monthlyDiffWBR = means.iloc[1], means.iloc[1]-means.iloc[0]
    
    lastMonthMean = lastMonthMeanMHB + lastMonthMeanNHG + lastMonthMeanWBR
    
    monthlyDiff = monthlyDiffMHB + monthlyDiffNHG + monthlyDiffWBR
    
    return lastMonthMean, monthlyDiff    



def getESSflows2(yesterday, startDate, endDate):
    """Compute last month's average, plus the difference with yesterday for the Eastside Streams.  
    This is the sum of the Cosumnes River at Michigan Bar, the Mokulmne River at Woodbridge, and releases
    from New Hogan Dam into the Calaveras River."""   

    
    #For Cosumnes River at Michigan Bar.
    yesterFlowMHB, flowDiffMHB = getFlows2('MHB', '41', yesterday, startDate, endDate) 
    
    #For reservoir releases from New Hogan Lake into the Calaveras River.
    yesterFlowNHG, flowDiffNHG = getFlows2('NHG', '23', yesterday, startDate, endDate)    
    
    df = pd.read_csv(r'Mokelumne at Woodbridge Flow Data.csv')
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df.set_index(['Date'], inplace=True)
       
    
    means = df[startDate : yesterday]['Flow'].groupby(by=[pd.Grouper(freq='M')]).mean()
    

    yesterFlowWBR, flowDiffWBR = df['Flow'].iloc[-1], df['Flow'].iloc[-1]-means.iloc[0]
    
    yesterFlow = yesterFlowMHB + yesterFlowNHG + yesterFlowWBR
    
    flowDiff = flowDiffMHB + flowDiffNHG + flowDiffWBR
       

    return yesterFlow, flowDiff 






def getPDM(station):
    """Gets the PDM for a station from the end of the previous month."""
    from numpy import nan
  
    startDate = pd.Timestamp.today() - pd.offsets.MonthBegin(2)
       
    dfPDMgood = pd.read_csv(r'PRIVATE API URL' \
                          .format(station, str(startDate.year)  , str(startDate.month)))

    dfPDMgood.replace(0,np.nan,inplace=True)


    dfPDMunchecked= pd.read_csv(r'PRIVATE API URL' \
                          .format(station, str(startDate.year)  , str(startDate.month)))

    dfPDM = dfPDMgood.combine_first(dfPDMunchecked)
    
    dfPDM.replace(0.00,nan,inplace=True)
    
    return dfPDM['Progressive Daily Mean'].iloc[-1]/1000.0


def getDM(station, yesterday):
    """Gets the Daily Mean for a station from yesterday."""    
    from numpy import nan
  
    # startDate = mytools.firstDateOfMonthsAgo(0)
    
    startDate = pd.Timestamp.today() - pd.offsets.MonthBegin()
       
    dfDMgood = pd.read_csv(r'PRIVATE API URL' \
                          .format(station, str(startDate.year)  , str(startDate.month)))

    dfDMgood.replace(0,np.nan,inplace=True)


    dfDMunchecked= pd.read_csv(r'PRIVATE API URL' \
                          .format(station, str(startDate.year)  , str(startDate.month)))

    dfDM = dfDMgood.combine_first(dfDMunchecked)
    
    dfDM.replace(0.00,nan,inplace=True)
    

    string = yesterday.strftime('%Y/%m/%d')+" 00:00:00"
      
    dailyMean = dfDM[dfDM['StartDateTime']==string].iloc[0]['DailyMean']
      
    
    return dailyMean/1000.0





def createFigure1(newDirPath,deficiencyPeriod):
    """Creates a map of the Monthly Average Flows for the previous month, and differences 
    from the month before that, along with the PDM for the previous month."""
    
    fig = plt.figure(figsize = (8.5,11))  
    ax = fig.add_axes([0.05,0.15,.9,.8])    

    createBackground(ax)
        
    startDate = (pd.Timestamp.today() - pd.offsets.MonthBegin(3)).date()
    endDate = (startDate + pd.offsets.MonthEnd(2)).date()
       
    
    #Get Sacramento River and Sac Regional WWTP flow values, and add boxes to figure.
    lastMonthMean,monthlyDiff = getSacFlows(startDate, endDate)
    createFlowBox(ax,0.77,0.82,lastMonthMean,monthlyDiff)
   
    #Get Yolo Bypass at Rumsey Bridge and Fremont Weir flow values, and add boxes to figure.
    lastMonthMean,monthlyDiff = getYoloFlows(startDate, endDate)    
    createFlowBox(ax,0.26,0.77,lastMonthMean,monthlyDiff)    

    #Get East Side Streams flow values, and add boxes to figure.    
    lastMonthMean,monthlyDiff = getESSflows(startDate, endDate)
    createFlowBox(ax,0.89,0.45,lastMonthMean,monthlyDiff)    
    
    #Get San Joaquin flow values, and add boxes to figure.  
    lastMonthMean, monthlyDiff = getFlows('VNS', '41', startDate, endDate)     
    createFlowBox(ax,0.96,-0.07,lastMonthMean,monthlyDiff)     
    
    #Get Tracy Pumping Plant flow values, and add boxes to figure.      
    lastMonthMean, monthlyDiff = getFlows('TRP', '70', startDate, endDate)     
    createFlowBox(ax,.34,0.05,lastMonthMean,monthlyDiff)      

    #Get Harvey O. Banks Pumping Plant flow values, and add boxes to figure.      
    lastMonthMean, monthlyDiff = getFlows('HRO', '70', startDate, endDate)     
    createFlowBox(ax,.07,0.05,lastMonthMean,monthlyDiff) 
    
     #Get Delta Outflow values, and add boxes to figure.      
    lastMonthMean, monthlyDiff = getFlows('DTO', '23', startDate, endDate)     
    createFlowBox(ax,.27,0.25,lastMonthMean,monthlyDiff)      
    
    pdm = getPDM("2")
    if np.isnan(pdm):    
        ax.text(x=0.41,y=0.36,s='*No data\nCollinsville\n(C-2)',ha='center', weight='bold',transform=ax.transAxes)
    else:    
        ax.text(x=0.41,y=0.36,s=f'{pdm:.2f} mS/cm\nCollinsville\n(C-2)',ha='center', weight='bold',transform=ax.transAxes)
        
    pdm = getPDM("64")
    if np.isnan(pdm):                   
        ax.text(x=0.37,y=0.45,s='*No Data\nNational Steel\n(S-64)',ha='center', weight='bold',transform=ax.transAxes)  
    else:
        ax.text(x=0.37,y=0.45,s=f'{pdm:.2f} mS/cm\nNational Steel\n(S-64)',ha='center', weight='bold',transform=ax.transAxes)

    pdm = getPDM("49")
    if np.isnan(pdm):
       ax.text(x=0.31,y=0.53,s='*No Data\nBeldon\'s Landing\n(S-49)',ha='center', weight='bold',transform=ax.transAxes)         
    else:
        ax.text(x=0.31,y=0.53,s=f'{pdm:.2f} mS/cm\nBeldon\'s Landing\n(S-49)',ha='center', weight='bold',transform=ax.transAxes)

    pdm = getPDM("42")
    if np.isnan(pdm):
       ax.annotate(text='*No Data\nVolanti\n(S-42)', xy=(0.1,0.54),
       xycoords='axes fraction',xytext=(0.2,0.6),arrowprops=dict(arrowstyle='-',relpos=(0.2,0)),ha='center', weight='bold')     
    else:
       ax.annotate(text=f'{pdm:.2f} mS/cm\nVolanti\n(S-42)', xy=(0.1,0.54),
       xycoords='axes fraction',xytext=(0.2,0.6),arrowprops=dict(arrowstyle='-',relpos=(0.2,0)),ha='center', weight='bold')  

    pdm = getPDM("21")
    if np.isnan(pdm):
       ax.annotate(text='*No Data\nSunrise\n(S-21)', xy=(0.051,0.545),
       xycoords='axes fraction',xytext=(0.01,0.60),arrowprops=dict(arrowstyle='-',relpos=(0.7,0.0)),ha='center', weight='bold')       
    else:
       ax.annotate(text=f'{getPDM("21"):.2f} mS/cm\nSunrise\n(S-21)', xy=(0.051,0.545),
       xycoords='axes fraction',xytext=(0.01,0.60),arrowprops=dict(arrowstyle='-',relpos=(0.7,0.0)),ha='center', weight='bold')
        
    pdm = getPDM("97")
    if np.isnan(pdm):
       ax.text(x=-0.05,y=0.5,s='*No Data\nIbis\n(S-97)',ha='center', weight='bold',transform=ax.transAxes)
    else:       
       ax.text(x=-0.05,y=0.5,s=f'{pdm:.2f} mS/cm\nIbis\n(S-97)',ha='center', weight='bold',transform=ax.transAxes)

    
    pdm = getPDM("35")
    if np.isnan(pdm):
       ax.text(x=-0.045,y=0.41,s='*No Data\nGoodyear\n(S-35)',ha='center', weight='bold',transform=ax.transAxes)  
    else:
       ax.text(x=-0.045,y=0.41,s=f'{pdm:.2f} mS/cm\nGoodyear\n(S-35)',ha='center', weight='bold',transform=ax.transAxes)    
    
    addTitle(ax, endDate, deficiencyPeriod)   
    ax.axis('off')     
  
    fig.savefig(os.path.join(newDirPath,'Figure 1.pdf'), dpi=300) 
   

def createFigure2(newDirPath,deficiencyPeriod):
    """Creates a map of the Monthly Average Flows for the previous month, and differences 
    it and the Monday before the meeting, along with the Daily for that day.""" 
    
    fig = plt.figure(figsize = (8.5,11))  
    ax = fig.add_axes([0.05,0.15,.9,.8])    
    
    createBackground(ax)    
    

    
    yesterday = (pd.Timestamp.today() - pd.DateOffset(days=1)).date()
    startDate = (pd.Timestamp.today() - pd.offsets.MonthBegin(2)).date()
    endDate = (startDate + pd.offsets.MonthEnd()).date()
    

    
    
    #Get Sacramento River and Sac Regional WWTP flow values, and add boxes to figure.
    yesterFlow, flowDiff = getSacFlows2(yesterday, startDate, endDate)
    createFlowBox(ax,0.77,0.82,yesterFlow, flowDiff)    

   
    #Get Yolo Bypass at Rumsey Bridge and Fremont Weir flow values, and add boxes to figure.
    yesterFlow, flowDiff = getYoloFlows2(yesterday, startDate, endDate)
    createFlowBox(ax,0.26,0.77,yesterFlow, flowDiff)        
    
    
    #Get East Side Streams flow values, and add boxes to figure.  
    yesterFlow, flowDiff = getESSflows2(yesterday, startDate, endDate)
    createFlowBox(ax,0.89,0.45,yesterFlow, flowDiff) 
    
      
    #Get San Joaquin flow values, and add boxes to figure.  
    yesterFlow, flowDiff = getFlows2('VNS', '41', yesterday, startDate, endDate)     
    createFlowBox(ax,0.96,-0.07,yesterFlow, flowDiff)  
    
    #Get Tracy Pumping Plant flow values, and add boxes to figure.      
    yesterFlow, flowDiff = getFlows2('TRP', '70', yesterday, startDate, endDate)     
    createFlowBox(ax,.34,0.05, yesterFlow, flowDiff)        
    
    #Get Harvey O. Banks Pumping Plant flow values, and add boxes to figure.      
    yesterFlow, flowDiff = getFlows2('HRO', '70', yesterday, startDate, endDate)     
    createFlowBox(ax,.07,0.05,yesterFlow, flowDiff)    
    

     #Get Delta Outflow values, and add boxes to figure.      
    yesterFlow, flowDiff = getFlows2('DTO', '23', yesterday, startDate, endDate)     
    createFlowBox(ax,.27,0.25,yesterFlow, flowDiff)  

  
    dm = getDM("22",yesterday)
    if np.isnan(dm):    
        ax.text(x=0.41,y=0.36,s='*No data\nCollinsville\n(C-2)',ha='center', weight='bold',transform=ax.transAxes)
    else:    
        ax.text(x=0.41,y=0.36,s=f'{dm:.2f} mS/cm\nCollinsville\n(C-2)',ha='center', weight='bold',transform=ax.transAxes)
        
    dm = getDM("64",yesterday)
    if np.isnan(dm):    
        ax.text(x=0.37,y=0.45,s='*No Data\nNational Steel\n(S-64)',ha='center', weight='bold',transform=ax.transAxes)
    else:          
        ax.text(x=0.37,y=0.45,s='{:.2f} mS/cm\nNational Steel\n(S-64)'.format(getDM('64',yesterday)),ha='center', weight='bold',transform=ax.transAxes)

    dm = getDM("49",yesterday)
    if np.isnan(dm):
       ax.text(x=0.31,y=0.53,s='*No Data\nBeldon\'s Landing\n(S-49)',ha='center', weight='bold',transform=ax.transAxes)         
    else:
        ax.text(x=0.31,y=0.53,s=f'{dm:.2f} mS/cm\nBeldon\'s Landing\n(S-49)',ha='center', weight='bold',transform=ax.transAxes)

    dm = getDM("42",yesterday)
    if np.isnan(dm):
       ax.annotate(text='*No Data\nVolanti\n(S-42)', xy=(0.1,0.54),
       xycoords='axes fraction',xytext=(0.2,0.6),arrowprops=dict(arrowstyle='-',relpos=(0.2,0)),ha='center', weight='bold')     
    else:
       ax.annotate(text=f'{dm:.2f} mS/cm\nVolanti\n(S-42)', xy=(0.1,0.54),
       xycoords='axes fraction',xytext=(0.2,0.6),arrowprops=dict(arrowstyle='-',relpos=(0.2,0)),ha='center', weight='bold')  

    dm = getDM("21",yesterday)
    if np.isnan(dm):
       ax.annotate(text='*No Data\nSunrise\n(S-21)', xy=(0.051,0.545),
       xycoords='axes fraction',xytext=(0.01,0.60),arrowprops=dict(arrowstyle='-',relpos=(0.7,0.0)),ha='center', weight='bold')       
    else:
       ax.annotate(text=f'{dm:.2f} mS/cm\nSunrise\n(S-21)', xy=(0.051,0.545),
       xycoords='axes fraction',xytext=(0.01,0.60),arrowprops=dict(arrowstyle='-',relpos=(0.7,0.0)),ha='center', weight='bold')
        
    dm = getDM("97",yesterday)
    if np.isnan(dm):
       ax.text(x=-0.05,y=0.5,s='*No Data\nIbis\n(S-97)',ha='center', weight='bold',transform=ax.transAxes)
    else:       
       ax.text(x=-0.05,y=0.5,s=f'{dm:.2f} mS/cm\nIbis\n(S-97)',ha='center', weight='bold',transform=ax.transAxes)

    
    dm = getDM("35",yesterday)
    if np.isnan(dm):
       ax.text(x=-0.045,y=0.41,s='*No Data\nGoodyear\n(S-35)',ha='center', weight='bold',transform=ax.transAxes)  
    else:
       ax.text(x=-0.045,y=0.41,s=f'{dm:.2f} mS/cm\nGoodyear\n(S-35)',ha='center', weight='bold',transform=ax.transAxes)     
       
       
    addTitle2(ax,yesterday)     
    
    # ax.text(x=1.1,y=-0.15,s='4',ha='right',transform=ax.transAxes,fontsize='x-large') 
    
    ax.axis('off')      

    fig.savefig(os.path.join(newDirPath,'Figure 2.pdf'), dpi=300) 
    

def createDir():
    """Create a new directory for the new month of the report."""
    
    today = pd.Timestamp.today()
    newDir = f'{today:%Y_%m}' 
    newDirPath = os.path.join(rootDir,newDir)

    if not os.path.exists(newDirPath):
        print(f'Creating new directory, {newDirPath}')
        os.mkdir(newDirPath)

        
    return newDirPath        



def downloadFigs(overwriteCDECs):
    
    """Downloads figures from CDEC, including Reservoirs, Northern Sierra Basin 
    Precipitation and San Joaquin Basin Precipitation.  Set overwriteCDECs=True
    if existings charts should be overwritten with new charts."""
    
    import requests
    
    #Create a list to hold the URLs.
    urls = []
    
    #Create a list to hold the full paths of the output files.
    outFiles = []
      
    urls.append('https://cdec.water.ca.gov/reportapp/javareports?name=rescond.pdf')
    outFiles.append(f'{newDirPath}/Reservoirs_{period}.pdf')
   
    
    urls.append('https://cdec.water.ca.gov/reportapp/javareports?name=PLOT_ESI.pdf')
    outFiles.append(f'{newDirPath}/N_Sierras_{period}.pdf')
    
    
    urls.append('https://cdec.water.ca.gov/reportapp/javareports?name=PLOT_FSI.pdf')
    outFiles.append(f'{newDirPath}/San_Joaquin_{period}.pdf')    
    
    #Loop through urls and outFiles, and if the files haven't been downloaded, or
    #overwriteFigs=True, then download from CDEC.
    for url,outFile in zip(urls, outFiles):
                
        if not os.path.exists(outFile) or overwriteCDECs==True:
            
                print(f'Downloading {os.path.split(outFile)[-1]}')

                r = requests.get(url)
                
                with open(outFile,'wb') as file:
                    
                    file.write(r.content)  
    
def latex():
    
    """Creates the LaTeX file."""
    
    #Determine second Wednesday of the month.
    secWed = pd.Timestamp.today() - pd.offsets.MonthBegin(1) + pd.offsets.WeekOfMonth(week=1,weekday=2)
          
    #Full path of the current Reservoirs figure.
    resPath = f'{rootDir}/{period}/Reservoirs_{period}.pdf'
    
    #Full paths of the Northern Sierra and San Joaquin figures.
    northSierrasPath = f'{rootDir}/{period}/N_Sierras_{period}.pdf'
    sanJoaquinPath = f'{rootDir}/{period}/San_Joaquin_{period}.pdf'
       
    #Timestamp of the previous month.
    prevTS = pd.Timestamp.today()-pd.DateOffset(months=1)
    
    #Period from the previous month, e.g., 2020_12.
    prevPeriod = f'{prevTS:%Y_%m}'
    
    #Full path of the root dir of the previous period.
    prevRootDir = f'{rootDir}/{prevPeriod}'
    
    #Full paths of Figures 1 and 2.
    fig1Path = f'{rootDir}/{period}/Figure 1.pdf'
    fig2Path = f'{rootDir}/{period}/Figure 2.pdf'
    
    #Full path of the reservoir figure from the previous period.
    prevResPath = f'{prevRootDir}/Reservoirs_{prevPeriod}.pdf'

    #Full path of the tex file.
    texPath = os.path.join(newDirPath,period+'.tex')
    
    file = open(texPath,'w')
    
    #Get dictionary of facilities updates.
    mapLog = readLog()

    #Boilerplate first string.
    s = r"""\documentclass[12 pt]{article}
        \usepackage{helvet}
        \usepackage{graphicx}
        \usepackage[top=0.5in,bottom=0.7in,left=0.5in,right=0.5in]{geometry}
        \usepackage{array}
        \usepackage{fancyhdr}
        \usepackage{setspace}
        
        \fancyhf{}
        \renewcommand{\headrulewidth}{0pt}
        \pagestyle{fancy}
        \fancyfoot[R]{\thepage}
        \renewcommand{\familydefault}{\sfdefault}
        \doublespacing
        
        \begin{document}
        \begin{center}
        \begin{Large}
        \begin{singlespace}
        \textbf{DEPARTMENT OF WATER RESOURCES \\
        BRIEFING PACKET}  \\[10 pt]
        \textbf{SUISUN RESOURCE CONSERVATION DISTRICT\\
        BOARD OF DIRECTORS MEETING} \\[12 pt]
        \end{singlespace}
        \end{Large}"""'\n'.replace('    ','')
    file.write(s)
    file.write(f'{secWed:%B %d, %Y}'r' \\[5pt]''\n')
    file.write(r'2 PM \\[5 pt]''\n')
    file.write(r'Solano County Board of Supervisors Chambers, Fairfield, CA \\[10 pt]''\n\n')
    file.write(r'\makebox[\textwidth][c]{\includegraphics[width=1.2\textwidth]{' \
               f'{salinityMapPath}''}}\n\n')
    file.write(r'\pagebreak''\n\n')
    
    
    
    file.write(r'{\Large \textbf{Facilities Update}}  \\[30pt]''\n')
    file.write(r'\end{center}''\n')
    file.write(r'\begin{flushleft}''\n')
    file.write(r'{\Large \emph{' f'{mapLog["rrds"][0]}' '}}\n')
    file.write(r'\begin{itemize}''\n')
    for item in mapLog['rrds'][1:]:
        file.write(item+'\n')
    file.write(r'\end{itemize}''\n')
    
    file.write(r'\end{flushleft}''\n') 
    file.write(r'\pagebreak''\n')
    file.write(r'\begin{center}''\n')
    file.write(r'{\Large \textbf{Facilities Update}}  \\[30pt]''\n')
    file.write(r'\end{center}  ''\n')  
    
    file.write(r'\begin{flushleft}''\n')       
    file.write(r'\bigskip \bigskip {\Large \emph{' f'{mapLog["mids"][0]}' '}}\n')
    file.write(r'\begin{itemize}''\n')
    for item in mapLog['mids'][1:]:
        file.write(item+'\n')
    file.write(r'\end{itemize}''\n')    
   
    file.write(r'\end{flushleft}''\n')
    file.write(r'\pagebreak''\n')
    
    file.write(r'\begin{center}''\n')
    file.write(r'{\Large \textbf{Facilities Update}}  \\[30pt]''\n')    
    file.write(r'\end{center}''\n')
    file.write(r'\begin{flushleft}''\n')
    file.write(r'{\Large \emph{' f'{mapLog["gyso"][0]}' '}}\n')
    file.write(r'\begin{itemize}''\n')
    for item in mapLog['gyso'][1:]:
        file.write(item+'\n')
    file.write(r'\end{itemize}''\n') 
    
    
    file.write(r'\end{flushleft}''\n')     
    file.write(r'\pagebreak''\n')
    file.write(r'\begin{center}''\n')
    file.write(r'{\Large \textbf{Facilities Update}}  \\[30pt]''\n')
    file.write(r'\end{center}  ''\n')      
    
    file.write(r'\begin{flushleft}''\n')
    file.write(r'\bigskip \bigskip {\Large \emph{' f'{mapLog["smscg"][0]}' '}}\n')
    file.write(r'\begin{itemize}''\n')  
    for item in mapLog['smscg'][1:]:
        file.write(item+'\n')
    file.write(r'\end{itemize}''\n')     
    file.write(r'\end{flushleft}''\n')    
           
    file.write(r'\pagebreak''\n')    

  #Include when lanugage on a Deficiency Period is desired.    
    # file.write(r'\begin{center}''\n')
    # file.write(r'{\Large \textbf{Deficiency Period}}  \\[20pt]''\n')
    # file.write(r'\end{center}''\n')      
    
    # file.write(r'\begin{flushleft}''\n')

    # file.write(r'{\Large \emph{Conditions:} }''\n')       
    # file.write(r'\begin{enumerate}')
    # file.write(r' \item \emph{Critical Year} following a \emph{Dry} or \emph{Critical Year}.''\n')       
    # file.write(r' \item \emph{Dry Year} following a year where the Sacramento Valley Water Year Sum was less than 11.35 MAF.''\n')
    
    # file.write(r' \item The second consecutive \emph{Dry Year} following a \emph{Critical Year}.''\n')
    # file.write(r'\end{enumerate}''\n')   

    # file.write(r'\vspace{0.2 in} {\Large \emph{Determination of a new Deficiency Period:} }''\n')
    # file.write(r'\begin{itemize}''\n')       
    
    # file.write(r' \item The determination is made using the prior water ' 
    #            "year's final Water Year Type and a Forecast of the Current Water Year Type.\n")
        
    # file.write(r' \item The Forecast of the Current Water Year Type is a preliminary determination'  
    #            r'made by DWR on the first of each February, March, April, and May. It is published in '  
    #            r'DWR Bulletin 120, which comes out the second week of each February, March, April, and May.  '  
    #            "It is also posted on DWR's Water Supply Index webpage.\n")
       
    # file.write(r' \item During a Deficiency Period, the salinity standards in the Western Marsh Stations ' \
    #            r'(S-21 and S-42) are higher than during normal circumstances.''\n')
    # file.write(r'\end{itemize}''\n')
    # file.write(r'\medskip \qquad  \enspace \includegraphics{StandardsTable.jpg}\n')
    # file.write(r'\pagebreak''\n') 
    # file.write(r'\begin{center}''\n')
    # file.write(r"{\Large \textbf{Deficiency Period (cont'd)}}  \\[20pt]"'\n')
    
    # file.write(r'\vspace{0.2 in} {\Large \emph{Criterion for Ending a Deficiency Period:} }''\n')
    # file.write(r'\end{center}''\n')  
    # file.write(r'\begin{itemize}''\n')   
    # file.write(r' \item Once in effect, a Deficiency Period will remain in effect until the \underline{subsequent} '
    #            r'water year is classified as either \textit{Wet, Above Normal} or \textit{Below Normal}.''\n')
    # file.write(r' \item The final classification is based on the May-1 50\%-Exceedance Value, typically finalized by the following spring.''\n')
    # file.write(r'\end{itemize}''\n')
        
    # file.write(r'\begin{center}''\n')
    # file.write(r'\vspace{0.4 in} {\Large \textbf{Deficiency Period 2021} }''\n')
    # file.write(r'\end{center}''\n')    
     
    # file.write(r'\begin{itemize}''\n')
    # file.write(r' \item The preliminary WY 2020 (October 2019 to September 2020) Type is classified as \textit{Dry}.''\n')   
    # file.write(r' \item The February 1st Forecast for WY 2021 (October 2020 to September 2021) is \textit{Critical}.''\n')
    # file.write(r' \item Based on these factors, we are now in a Deficiency Period.''\n')
    # file.write(r' \item The earliest the Deficiency Period could end is Spring of 2023.  For this to occur, WY 2022 '
    #            r'(October 2021 to September 2022) would have to be classified as \textit{Wet, Above Normal, or Below Normal}.''\n')
    # file.write(r'\end{itemize}  ''\n')
    
    # file.write(r'\pagebreak''\n')
     
    # file.write(r'\begin{center}''\n')  
    # file.write(r'{\Large \textbf{Drought Response Fund (DRF)}}  \\[20pt]''\n')
    # file.write(r'\end{center}   ''\n')   
    
    # file.write(r'\vspace{0.4 in} {\Large \textit{Conditions triggering the DRF:} }''\n')
    # file.write(r'\begin{enumerate} ''\n')
    
    # file.write(r' \item Deficiency Period is in effect and Trigger Values of Table 2 of the SMPA are exceeded at Control Stations S-35 or S-97, during any two or more of the following months: October, February, March, April, or May. \medskip''\n')
    # file.write(r' \item Deficiency Period has been in effect for more than one year, and Trigger Values of Table 2 of the SMPA '
    #            r'are exceeded at any Compliance Station, C-2, S-21, S-42, S-49, or S-64, during any two or more of the following months: October, February, March, '               
    #            r'April, or May. \medskip   ''\n')
    # file.write(r'\item If the Standards are not met for more than two months at one or more of the Eastern Stations, C-2, S-49, or S-64.  \\[20pt]''\n\n')
    # file.write(r'\end{enumerate}''\n')  
    
    file.write(r'\begin{center}''\n')
    file.write(r'{\Large   \textbf{DRF 2021}}  \\[20pt]''\n')
    file.write(r'\end{center}  ''\n')
    
    file.write(r'\begin{flushleft} ''\n')
    file.write(r'\begin{itemize}''\n')
#Add monthly DRF updates here.    
    file.write(r' \item The PDMs at the Control and Compliance Stations did not exceed the trigger value of 20.0 mS/cm at the end of October.''\n')
    # file.write(r' \item The PDMs at the Control Stations exceeded the trigger value of 9.0 mS/cm at the end of February.''\n')
    # file.write(r' \item The PDMs at the Control Stations exceeded the trigger value of 9.0 mS/cm at the end of March.''\n')
    # file.write(r' \item The PDMs at the Control Stations were below the trigger value of 12.0 mS/cm at the end of April.''\n')
    file.write(r'\end{itemize}''\n')


    
    file.write('%GRAPHICS START HERE**************************************************************************\n\n')
    
    file.write(r'\newgeometry{left=0.2in,top=0.2in,bottom=0.2in,right=0.2in}''\n\n')   
    
    file.write(r'\includegraphics[scale=0.9]{' f'{fig1Path}' '}\n')
    file.write(r'\makebox[\textwidth][r]{\thepage}''\n\n')
    
    file.write(r'\pagebreak''\n\n')
    
    file.write(r'\includegraphics[scale=0.9]{' f'{fig2Path}' '}\n')
    file.write(r'\makebox[\textwidth][r]{\thepage}''\n\n')
    file.write(r'\pagebreak''\n\n')
       
    file.write(r'\begin{tabular}{m{4in}m{3in}}''\n')
    file.write(r'\includegraphics[trim=10 45 35 110,clip,height=0.46\paperheight]{' f'{resPath}' r'} &  \qquad Current Month: ' f'{pd.Timestamp.now():%B %Y} '   r'\\''\n')  
    file.write(r'\includegraphics[trim=10 45 35 110,clip,height=0.46\paperheight]{' f'{prevResPath}' r'} &  \qquad Previous Month: ' f'{prevTS:%B %Y} '   r'\\''\n')
    file.write(r'\end{tabular}''\n\n')

    file.write(r'\makebox[\textwidth][r]{\thepage}''\n\n')
    
    file.write(r'\includegraphics[trim=30 25 20 20,clip,height=0.44\paperheight]{' f'{northSierrasPath}'   r'}  \\[10 pt]''\n')
    file.write(r'\includegraphics[trim=30 25 20 20,clip,height=0.44\paperheight]{' f'{sanJoaquinPath}'   r'} \\''\n')
    
    file.write(r'\end{flushleft}''\n')       
    file.write(r'\makebox[\textwidth][r]{\thepage}''\n\n')
    
    file.write(r'\restoregeometry''\n')
    file.write(r'\end{document}''\n')

    file.close()

    
def getLines(lines, idx):
    
     """Return a list of facilities updates for a given facility given the full list of lines
     read from log file, and the index location for a given facility, idx."""

     lst=[]
     
     #Set the index equal to the given idx.
     i=idx
     #Add lines to list until hitting '\n' or 'END'.
     while not (lines[i]=='\n' or lines[i]=='END'):
         #Strip off the trailing '\n'
         lst.append(lines[i].strip("\n"))
         i+=1
     return lst
     
    
def readLog():
    
    """Reads the log file of facilities updates and returns a dictionary of a list of updates with 
    the name of the facility as the key."""

    file = open(logPath,'r')
    
    lines = file.readlines()
    
    file.close()    
    
    mapLog={}    
    
    mapLog['rrds'] = getLines(lines, lines.index('Roaring River Distribution System (RRDS)\n'))
    mapLog['mids'] = getLines(lines, lines.index('Morrow Island Distribution System (MIDS)\n'))
    mapLog['gyso'] = getLines(lines, lines.index('Goodyear Slough Outfall (GYSO)\n'))
    mapLog['smscg'] = getLines(lines, lines.index('Suisun Marsh Salinity Control Gates (SMSCG)\n'))
        
    return mapLog
    

def report(overwriteFigs, overwriteCDECs):
    
    """Creates the full report, including:
        1) Creates new directory, if necessary.
        2) Downloads graphics from CDEC, if necesary.
        3) Creates Figures 1 and 2, if necessary.
        4) Buids the LaTeX file.
        5) Compiles LaTeX file to PDF.
    """
    
    #GET THE PATH OF THE DIRECTORY FOR THE NEW REPORT AND CREATE IF NECESSARY.
    newDirPath = createDir()      

    #Create Figures 1 and 2, if necessary.
    if not (os.path.exists(os.path.join(newDirPath,'Figure 1.pdf'))) or overwriteFigs==True:
        print('Creating Figure 1')
        createFigure1(newDirPath,deficiencyPeriod)
    if not (os.path.exists(os.path.join(newDirPath,'Figure 2.pdf'))) or overwriteFigs==True:
        print('Creating Figure 2')
        createFigure2(newDirPath,deficiencyPeriod)   
        
    #Download figures from CDEC.
    downloadFigs(overwriteCDECs=True)    
    
    print('Creating LaTeX file')
    latex()
    
    print('Compiling TeX file into PDF')
    os.system(f'pdflatex -output-directory "{newDirPath}" "{os.path.join(newDirPath,period)}.tex"')





if __name__=="__main__":
    
    """This script creates monthly SRCD Board Report.  Run report() to:
        1) Create new directory with createDir(), if necessary.
        2) Download graphics from CDEC with downloadFigs(), if necesary.
        3) Create Figures 1 and 2 with createFigure1 and createFigure2, if necessary.
        4) Buid the LaTeX file with latex().
        5) Compile LaTeX file to PDF.
    
    Run any of the above listed functions to carry out each operation, independently.
    
    State below whether we are in a Deficiency Period.
    
    Run PDMmap(controlStations=False, deficiencyPeriod) from SalinityTrackers script first to generate the PDM map.
    
    """
    
    #STATE IF WE'RE IN A DEFICIENCY PERIOD.
    deficiencyPeriod = True

    #SET THE FULL PATH OF THE PROGRESSIVE DAILY MEAN SALINITIES MAP.
    #Run PDMmap(controlStations=False, deficiencyPeriod) from SalinityTrackers script first to generate the PDM map.
    salinityMapPath = 'SalinityTrackers/Progressive Daily Mean Salinities Map.pdf'
    
    #SET THE PATH OF THE LOG TEXT FILE OF FACILITY UPDATES.
    logPath = r'SRCD_Board_Report\log.txt'
    
    #SET THE ROOT DIR OF THE SRCD BOARD REPORT.
    rootDir = r'SRCD Board Report'

    #GET THE PATH OF THE DIRECTORY FOR THE NEW REPORT AND CREATE IF NECESSARY.
    newDirPath = createDir()    

    #Get the year_month period.  E.g. 2021_01.
    period = newDirPath.split('\\')[-1]  

    #Download figures from CDEC.
    # downloadFigs(overwriteFigs=True)
    
    #Create Figures 1 and 2.
    # createFigure1(newDirPath,deficiencyPeriod)
    # createFigure2(newDirPath,deficiencyPeriod)     
    
    #Creat the LaTeX file:
    # latex()
    
    #Create the full report.    
    # report(overwriteFigs = True, overwriteCDECs=True)
    report(overwriteFigs = False, overwriteCDECs=False)
    



    

    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    