# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:59:55 2019

@author: jgalef
"""

import pandas as pd
from math import log10
import os



pd.set_option('display.width',500)
pd.set_option('float_format','{:.0f}'.format)
pd.set_option('display.max_colwidth',500)
pd.set_option('expand_frame_repr',False)
pd.set_option('max_rows',500)



def dayflow():
    """Python implementation of Dayflow. Reads input file, calculates values,
    and outputs to file.  See Dayflow documentation for explanation of equations."""
    
    #Read input file.
    df = pd.read_csv(inputFile, parse_dates=['Date'], index_col="Date")
        
    df['QEAST'] = df[['San Joaquin River at Vernalis','Cosumnes River at Michigan Bar',
      'Mokelumne River at Woodbridbge', 
      'Calaveras River releases from New Hogan Reservoir',]].sum(axis=1)
    
    df['QYOLO'] = df[['Yolo Bypass at Woodland','Sacramento Weir',
      'Putah Creek releases from Lake Solano']].sum(axis=1)
    
    df['QTOT'] = df[['Sacramento River at Freeport','QEAST','QYOLO']].sum(axis=1)
    
    
   #Calculate QPREC.
   
    #Create a date range for the water year.
    dr = pd.date_range(start=df.index[0],end=df.index[-1]+pd.Timedelta('4 days'),freq='D')
    
    #Create a new series that starts off with zeros.
    runoff = pd.Series(index=dr, data=[0 for i in range(len(dr))])
    
    #Loop through Precip column, and replace the zeros if there is precipitation for a particular date.
    #The runoff will be spread over that day and the following 4.  The precip is converted to runoff
    #by multiplying the precip (inches/day) * the area of the Delta (682,230 ac) * (43,560 ft2/ac) *
    #(1 day/86,400 s) * (1 ft/12 in) / (5 days) = 5732.62708333.
    
    for i in range(len(df)):
        for j in range(5):
            runoff[i+j] = int(runoff[i+j]+df['Precipitation at Stockton Fire Station'][i]*5732.62708333)
    
    #Because going out 5 days goes beyond the WY, truncate the last 4 values, and assign the rest
    #to the QPREC column.
    df['QPREC']=runoff[:-4]
    
    
    #The estimated GCD values from the Dayflow documentation.
    QGCD = [2150,2100,2050,2050,2000,2000,1950,1950,1950,1900,1900,1900,1900,1850,1850,1850,1850,
          1800,1800,1800,1800,1800,1750,1750,1750,1750,1750,1750,1700,1700,1700,1700,1700,1700,1700,1700,1700,
          1700,1650,1650,1650,1650,1650,1650,1650,1700,1700,1700,1700,1700,1750,1750,1750,1750,1750,1800,1800,
          1850,1900,1900,1950,2000,2000,2000,2050,2100,2100,2150,2150,2150,2200,2200,2200,2200,2200,2200,2200,
          2200,2150,2150,2150,2100,2100,2050,2050,2000,2000,1950,1950,1900,1850,1800,1700,1650,1600,1550,1500,
          1450,1400,1400,1350,1300,1300,1250,1250,1200,1200,1150,1150,1100,1100,1100,1050,1050,1000,1000,1000,
          1000,950,950,950,950,900,900,900,900,900,900,900,900,900,900,850,850,850,850,850,850,850,850,850,850,
          850,900,900,900,900,900,900,900,900,950,1000,1000,1000,1050,1050,1050,1100,1100,1100,1150,1150,
          1200,1250,1250,1300,1350,1350,1400,1400,1450,1500,1500,1550,1550,1600,1600,1650,1650,1650,1700,1750,
          1750,1750,1800,1800,1800,1800,1850,1850,1850,1850,1850,1900,1900,1900,1900,1900,1900,1900,1900,1900,
          1900,1900,1950,1950,1950,1950,2000,2000,2000,2000,2000,2050,2100,2100,2100,2150,2150,2200,2200,2250,
          2300,2300,2350,2350,2400,2450,2450,2500,2550,2550,2600,2650,2700,2750,2750,2800,2850,2900,2950,3000,
          3050,3100,3150,3200,3250,3300,3350,3400,3450,3500,3550,3600,3650,3700,3750,3800,3850,3900,3950,4000,
          4050,4100,4100,4150,4200,4200,4250,4250,4300,4300,4300,4300,4350,4350,4400,4400,4400,4400,4400,4400,
          4400,4400,4400,4400,4400,4400,4400,4400,4400,4350,4350,4350,4350,4350,4300,4300,4300,4250,4250,4250,
          4200,4200,4200,4150,4150,4100,4100,4050,4050,4000,4000,3950,3950,3900,3850,3850,3800,3800,3750,3700,
          3700,3650,3600,3600,3550,3500,3450,3450,3400,3350,3300,3250,3200,3200,3150,3100,3050,3000,2950,2900,
          2900,2850,2800,2750,2700,2650,2600,2600,2550,2500,2450,2450,2400,2350,2350,2300,2250,2250,2200,2200,
          2150,2150]

    #If it is a leap-year, insert the QCD value for Feb. 29.
    if df.index[-1].is_leap_year: QGCD.insert(151,950)
    
    df['QGCD'] = QGCD
    
    df['QGCD'] = df['QGCD'] - df['Byron Bethany Irrigation District'] 
    
    df['QCD'] = df['QGCD'] + df['Miscellaneous Diversions'] - df['QPREC']
    
    df['QEXPORTS'] = df['Tracy Pumping Plant'] + df['Contra Costa Middle River Intake'] + df['Contra Costa Old River Intake'] + \
        df['Contra Costa Rock Slough Intake'] + df['Clifton Court Intake'] + df['Barker Slough Pumping Plant']
        
    df['CCC'] = df['Contra Costa Middle River Intake'] + df['Contra Costa Old River Intake'] + \
        df['Contra Costa Rock Slough Intake']

    df['QOUT'] = df['QTOT'] + df['QPREC'] - df['QGCD'] - df['QEXPORTS'] - df['Miscellaneous Diversions']

        
    df['EXPIN'] = (df['Tracy Pumping Plant'] + df['Clifton Court Intake'] - df['Byron Bethany Irrigation District'])/df['QTOT']


    df['QXGEO'] = df['Delta Cross Channel'] + df['Georgiana Slough near Sacramento River']
    
    df['QWEST'] = df['San Joaquin River at Vernalis'] + df['Cosumnes River at Michigan Bar'] + df['Mokelumne River at Woodbridbge'] + \
                  df['Calaveras River releases from New Hogan Reservoir'] + df['QXGEO'] - df['QEXPORTS'] - df['Miscellaneous Diversions'] - \
                  0.65 * (df['QGCD'] - df['QPREC'])
                  
    df['QRIO'] = df['Sacramento River at Freeport'] + df['QYOLO'] - df['QXGEO'] - 0.28 * (df['QGCD'] - df['QPREC'])
    
    df['QDIVER'] = ((df['QTOT'] - df['QOUT'])/df['QTOT']) * 100
    
    QSJ4SD = []
    
    for i in range(len(df.index)):
          
    
        if (df['San Joaquin River at Vernalis'][i] <= df['QEXPORTS'][i] + df['Miscellaneous Diversions'][i]  + 0.42 * df['QCD'][i]):
            
           QSJ4SD.append(df['San Joaquin River at Vernalis'][i])
           
        elif ((df['San Joaquin River at Vernalis'][i] > df['QEXPORTS'][i] + df['Miscellaneous Diversions'][i]  + 0.42 * df['QCD'][i]) and \
             (df['QEXPORTS'][i] + df['Miscellaneous Diversions'][i]  + 0.42 * df['QCD'][i] > 0.65 * df['San Joaquin River at Vernalis'][i] + \
              + 0.15 * df['QCD'][i])):
            
           QSJ4SD.append(0.65 * df['San Joaquin River at Vernalis'][i] + 0.15 * df['QCD'][i])
           
        elif ((df['San Joaquin River at Vernalis'][i] > df['QEXPORTS'][i] + df['Miscellaneous Diversions'][i]  + 0.42 * df['QCD'][i]) and \
             (df['QEXPORTS'][i] + df['Miscellaneous Diversions'][i]  + 0.42 * df['QCD'][i] <= 0.65 * df['San Joaquin River at Vernalis'][i] + \
              + 0.15 * df['QCD'][i])):    
            
            QSJ4SD.append(df['QEXPORTS'][i] + df['Miscellaneous Diversions'][i]  + 0.42 * df['QCD'][i])
            
    df['QSJ4SD'] = QSJ4SD         


    df['QEFFECT'] = df['QTOT'] - df['QSJ4SD']


    df['QEFFDIV'] = ((df['QEFFECT'] - df['QOUT']) / df['QEFFECT']) * 100
    
    df['QSWP'] = df['Clifton Court Intake']
    
    previousX2 = getX2()
    x2s = []
    for QOUT in df['QOUT']:
        previousX2 = 10.16 + 0.945*previousX2 - 1.487*log10(QOUT)
        x2s.append(previousX2)
        
  
    df['X2'] = x2s
    
    df.rename(columns={'Sacramento River at Freeport':'SAC', 'QYOLO':'YOLO', 'Cosumnes River at Michigan Bar':'CSMR', 
                       'Mokelumne River at Woodbridbge':'MOKE', 'Calaveras River releases from New Hogan Reservoir':'MISC', 
                       'San Joaquin River at Vernalis':'SJR', 'QEAST':'EAST', 'QTOT':'TOT', 'Clifton Court Intake':'SWP', 
                       'Tracy Pumping Plant':'CVP', 'Barker Slough Pumping Plant':'NBAQ', 'QEXPORTS':'EXPORTS', 'QCD':'CD', 
                       'QGCD':'GCD', 'QXGEO':'XGEO', 'QWEST':'WEST', 'QRIO':'RIO', 'QOUT':'OUT', 'QEXPIN':'EXPIN', 
                       'QDIVER':'DIVER', 'QEFFECT':'EFFEC', 'QEFFDIV':'EFFDIV', 'Miscellaneous Diversions':'MISDV','QPREC':'PREC'},inplace=True)
    
    df['Year'] = df.index.year
    
    df['Mo'] = df.index.month
    
    df['Date'] = df.index.date
      

    df = df[['Year','Mo','Date','SAC','YOLO','CSMR','MOKE','MISC','SJR','EAST','TOT','CCC','SWP','CVP','NBAQ','EXPORTS','GCD','PREC',
             'MISDV','CD','XGEO','WEST','RIO','OUT','EXPIN','DIVER','EFFEC','EFFDIV','X2']]
    
    
    df['YOLO'] = df['YOLO'].round(0).astype('int32')
    df['CSMR'] = df['CSMR'].round(0).astype('int32')
    df['MISC'] = df['MISC'].round(0).astype('int32')
    df['YOLO'] = df['YOLO'].round(0).astype('int32')
    df['EAST'] = df['EAST'].round(0).astype('int32')
    df['TOT'] = df['TOT'].round(0).astype('int32')
    df['YOLO'] = df['YOLO'].round(0).astype('int32')
    df['CCC'] = df['CCC'].round(0).astype('int32')
    df['SWP'] = df['SWP'].round(0).astype('int32')
    df['CVP'] = df['CVP'].round(0).astype('int32')
    df['NBAQ'] = df['NBAQ'].round(0).astype('int32')
    df['EXPORTS'] = df['EXPORTS'].round(0).astype('int32')
    df['GCD'] = df['GCD'].round(0).astype('int32')
    df['CD'] = df['CD'].round(0).astype('int32')
    df['WEST'] = df['WEST'].round(0).astype('int32')
    df['RIO'] = df['RIO'].round(0).astype('int32')
    df['OUT'] = df['OUT'].round(0).astype('int32')
    df['EXPIN'] = df['EXPIN'].round(2)
    df['DIVER'] = df['DIVER'].round(0).astype('int32')
    df['EFFEC'] = df['EFFEC'].round(0).astype('int32')
    df['EFFDIV'] = df['EFFDIV'].round(0).astype('int32')
    df['X2'] = df['X2'].round(2)
    
    outDir = os.path.join(rootDir,f'WY{wy}/Output')
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    
    df.to_csv(outputFile,index=False)
    
    #Run monthly totals function.
    monthlyTotals()


def monthlyTotals():
    
    """Creates a separate file of monthly totals of the daily values
    returned from the Dayflow output file."""
    
    pd.set_option('float_format','{:.0f}'.format)
    
    #Set the columns to be retrieved from the Dayflow output file.
    cols='Date,SAC,YOLO,CSMR,MOKE,MISC,SJR,EAST,TOT,CCC,SWP,CVP,NBAQ,EXPORTS,' \
    'GCD,PREC,MISDV,CD,XGEO,WEST,RIO,OUT,EFFEC'.split(',')

    df = pd.read_csv(outputFile,parse_dates=['Date'],index_col='Date',usecols=cols)
    
    #Convert from CFS to ac-ft.
    df = df * 86400/43560
       
    #Resample the daily flow data to monthly means.
    mt = df.resample(rule='M',axis=0).sum()
    
    #Create a new column of the month name, e.g. OCT.
    mt['Mo'] = mt.index.map(lambda x:f'{x:%b}'.upper())
    
    #Set this new column as the index and delete the old.
    mt.set_index(mt['Mo'],inplace=True)
    mt.drop(columns=['Mo'],inplace=True)
    
    #Open a new text file to write the results.
    with open(monthlyFile,'w') as outFile:
        
        #Write out the column titles.
        outFile.write('monthly totals, acre-ft\n')
        
    #Output the dataframe to the text file.
    mt.to_csv(monthlyFile,mode='a',index_label='Mo',float_format='%.0f')

   
def getX2():
    
     """Retrieve the Sept. 30 X2 value from last year's results."""
     
    #Set the file path of last year's output file.
     file = os.path.join(rootDir,
     f'WY{wy-1}/Output/dayflowCalculations{wy-1}.csv') 
     
     df = pd.read_csv(file,nrows=366)
     
     df.dropna(inplace=True)
     
     x2 = df.iloc[-1,-1]
     
     return(x2)
 
    
def plotQC(df,station):
    
    """Makes a times-eries plot of the observed vs. modeled values.
    Also includes a plot of the difference between the observed 
    and modeled values.  Output is written to a PDF."""
    
    import matplotlib.pyplot as plt    
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
    

    fig, (ax1, ax2) = plt.subplots(nrows=2,ncols=1,figsize=(11,8.5),sharex=True)
       
    ax1.plot(df.iloc[:,0],label='Observed',color='blue')
    ax1.plot(df.iloc[:,1],label='Modeled',color='red')
    ax2.bar(x=df.index,height=df.iloc[:,2],color='purple',width=0.3)
 
    
    ax1.legend()
    ax1.set_title(f'Observed vs. Modeled Comparison for {station}',pad=15)
    
    ax1.set_ylabel('Flow (CFS)', labelpad=5)
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    ax2.set_ylabel('Flow Difference (CFS)', labelpad=5)
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_minor_locator(mdates.DayLocator(15))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    ax1.grid(b=True, which='major', color='grey', linestyle='-', linewidth=0.25)
    ax2.grid(zorder=0,b=True, which='major', color='grey', linestyle='-', linewidth=0.25)

    
    ax2.text(x=1,y=-.25,s="*Gaps are a result of missing Observed data.", 
             transform=ax2.transAxes, ha='right')
    
    fig.subplots_adjust(hspace=0.07)    
    
    plt.savefig(os.path.join(metaFolder,f'{station}.pdf'),dpi=600,format='pdf')    

    

def QCresults():
    
    """QC analysis comparing observed vs. modeled results at three locations,
    namely: the Sacramento River at Rio Vista, the San Joaquin River at Vernalis,
    and the total Delta outflow at Chipps Island.  Since there is no flow meter 
    for the total Delta Outflow, a proxy is used consisting of the combined
    flows at the Sacramento River at Rio Vista, San Joaquin River at Vernalis,
    Dutch Slough at Jersey Island, and Threemile Slough near Rio Vista stations.
    PDF stacked time-series plots are created showing the observed vs. modeled values
    and the differences in flow."""
    
    #State the column names to be read from the USGS flow file.
    cols='Date,THREEMILE SLOUGH NR RIO VISTA,DUTCH SLOUGH AT JERSEY ISLAND,'\
    'SACRAMENTO R AT RIO VISTA,SAN JOAQUIN R AT JERSEY POINT'.split(',')
    
    #Set new, shorter columns names, where the O_ means 'observed.'
    names = ['Date','O_TMS','O_DS','O_SR','O_SJ']
    
    #Read results from USGS flow file.
    qc = pd.read_csv(usgsFile,parse_dates=['Date'],index_col='Date',
                     usecols=cols,na_values=0)
    
    #Rename columns to shorter names.
    qc.rename(columns=dict(zip(cols,names)),inplace=True)
    
    #Calculate the total outflow at Chipps Island proxy.
    qc['O_OUT'] = qc.loc[:,['O_TMS','O_DS','O_SR','O_SJ']].sum(axis=1,skipna=False)
    
    cols = ['Date','RIO','XGEO','WEST','OUT']
    
    
    df = pd.read_csv(outputFile,parse_dates=['Date'],index_col='Date',usecols=cols)
    
    
    df = df.join(qc)
    
    
    df['D_RIO'] = df['O_SR'] - df['RIO']
    
    df['D_WEST'] = df['O_SJ'] - df['WEST']
    
    df['D_OUT'] = df['O_OUT'] - df['OUT']
    
    
    
    if not os.path.exists(metaFolder):
        os.mkdir(metaFolder)
        
    plotQC(df.loc[:,['O_SR','RIO','D_RIO']],'Sacramento River at Rio Vista')
    
    plotQC(df.loc[:,['O_SJ','WEST','D_WEST']],'San Joaquin River at Jersey Point')    
    
    plotQC(df.loc[:,['O_OUT','OUT','D_OUT']],'Total Delta Outflow at Chipps Island')
    

    
# SET THE ROOT DIRECTORY:    
rootDir = '//cnrastore-des/des001/DES_0340 - EP&I Branch/MARSH_WQ/Projects/DAYFLOW'

# SET THE WATER YEAR:
wy=2021

# SET THE FULL PATH OF THE DAYFLOW INPUT FILE:
inputFile = os.path.join(rootDir,f'WY{wy}/Dayflow input {wy-1}-{wy}.csv')

# SET THE FULL PATH OF THE DAYFLOW OUTPUT FILE:
outputFile = os.path.join(rootDir,f'WY{wy}/Output/dayflowCalculations{wy}.csv') 

# SET THE FULL PATH OF THE DAYFLOW MONTHLY TOTALS FILE:
monthlyFile = os.path.join(rootDir,f'WY{wy}/Output/monthlyTotals{wy}.csv')

# SET THE FULL PATH OF THE USGS DATA FILE:
usgsFile = os.path.join(rootDir,f'WY{wy}/Input Data/USGS.csv')

# SET THE FULL PATH OF THE METADATA FILE:
metaFolder = os.path.join(rootDir,f'WY{wy}/Metadata')



# RUN DAYFLOW:
# dayflow()

# CREATE THE QC TIME-SERIES PLOT:
QCresults()  


# RUNNING DAYFLOW WILL ALSO CREATE THE MONTHLY TOTALS FILE,
# BUT RUN THIS TO DO SO SEPARATELY:
# monthlyTotals()    


  


    
    
    
    
    
    
    
    