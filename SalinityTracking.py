# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:22:41 2019

@author: jgalef
"""

import matplotlib.pyplot as plt
import datetime as dt    
import geopandas as gp
import mytools


endDate = dt.date.today()-dt.timedelta(days=1)
startDate = endDate - dt.timedelta(days=30)

standards = mytools.getStandards()

SE, SW, SWDP = mytools.getStandardsDetailed()

df = mytools.getPDMs7(startDate, endDate, 'both', detailedStandards=True)

month = dt.date.today().month


def createTSplot(fig, extent, controlStations, deficiencyPeriod, color):
    """Creates a timeseries plot."""

    #Create the axes.    
    ax = fig.add_axes(extent[1])
    
    #Make the plot transparent.
    ax.patch.set_alpha(0)
    
    #Get rid of the x and y ticks.
    ax.set_xticks([])
    ax.set_yticks([])
    
    #Remove the top and right borders.
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #Plot the Daily Mean values.
    ax.plot(df[extent[0]],color=color)   
     
    station = extent[0].split(' ')[0]

    #Plot the Standard.  
    if station=='S-21' or station=='S-42': 
        if deficiencyPeriod==False:
            ax.step(df.index,df['Western Standards'],color='red') 
        elif deficiencyPeriod==True:
            ax.step(df.index,df['Western Deficiency Standards'],color='red') 
    elif station=='S-49' or station=='S-64' or station=='C-2': 
        ax.step(df.index,df['Eastern Standards'],color='red')
    
    if controlStations==True:
        
        if deficiencyPeriod==True:
            if station=='S-35' or station=='S-97': 
                ax.step(df.index,df['Western Deficiency Standards'],color='red')              
        else:    
            if station=='S-35' or station=='S-97': 
                ax.step(df.index,df['Western Standards'],color='red')         


    #Set the y-extent so that all plots are uniform.
    #Normally, the max is less than 20, so that is the default.
    #But, if it rises over 20, set limit 2 mS/cm over the max value.
    if df.max().max() < 20:
        ax.set_ylim([-0.5,20])
    else:
        ax.set_ylim([-0.5,df.max().max()+2])
    
    
    #Add a text data label to the final point.  
    ax.text(df.index.array[-1], df[extent[0]].iloc[-1], "  "+str(df[extent[0]].iloc[-1].round(1)), ha='left', va='center', fontsize=7)
    
    notna = df.loc[df[extent[0]].notna(),extent[0]]
    
    if not df[extent[0]].isna().all():
        ax.text(notna.index.array[-1], notna.iloc[-1], "  "+str(notna.iloc[-1].round(1)), ha='left', va='center', fontsize=7)
    

def createBackground(fig, ax):
    
    #Read in the hydrography shapefile.
    mapDf = gp.read_file(r'\\cnrastore\data_GIS\marsh.shp')
    
    #Plot all the channels.
    mapDf.plot(color=('lightsteelblue'), edgecolor='none', ax=ax, zorder=0, alpha=0.3)
    
    #Select only the relevant channels for bolding.
    mapDf = mapDf.query("HNAME == 'GRIZZLY BAY' or HNAME == 'MONTEZUMA SLOUGH' or HNAME == 'SACRAMENTO RIVER'\
                         or HNAME == 'BROAD SLOUGH' or HNAME == 'SUISUN SLOUGH' or HNAME == 'CORDELIA SLOUGH'\
                          or HNAME == 'GOODYEAR SLOUGH' or HNAME == 'CHADBOURNE SLOUGH' or HNAME == 'WELLS SLOUGH'\
                           or HNAME == 'VOLANTI SLOUGH'")
    
    #Plot the bolded channels.
    mapDf.plot(color=('lightblue'), edgecolor='lightblue', ax=ax, zorder=0, alpha=1)    
     
    #Use Geopandas to read the stations shapefile.
    stationsDF = gp.read_file(r'\\cnrastore\data_GIS\stations.shp')
    
    #Use a query to separate the compliance from the monitoring stations for colorizing.    
    stationsCompliance = stationsDF.query("type == 'compliance'")

    stationsCompliance.plot(color='lightcoral', edgecolor='black',ax=ax, zorder=0)
    
    stationsMonitoring = stationsDF.query("type == 'monitoring'")
    
    stationsMonitoring.plot(color='lightgreen',edgecolor='black',ax=ax)
    
    ax.patch.set_facecolor('whitesmoke')

    x0, xL = 572900, 603720
    y0 = 4211000 
    yL = (xL-x0)*(8.5/11)+y0

    ax.set_xlim([x0,xL])
    ax.set_ylim([y0,yL])
    
    ax.set_xticks([])
    ax.set_yticks([])

    ax.annotate(text='C-2\nSacramento River at\nCollinsville',xy=(600860,4214550),xytext=(599800,4216200),ha='right',va='center',fontsize=8,
                arrowprops=dict(arrowstyle='-', relpos=(1,0.5), connectionstyle='arc, angleA=0, angleB=45,armA=10,armB=1,rad=0'))    

    ax.annotate(text='S-64\nMontezuma Slough\nat National Steel',xy=(597380,4219880),xytext=(598500,4220850),ha='left',va='center',fontsize=8,
                arrowprops=dict(arrowstyle='-', relpos=(0,0.5), connectionstyle='arc, angleA=0, angleB=-45,armA=-10,armB=1,rad=0'))
    
    ax.annotate(text='S-49\nMontezuma Slough near\nBeldons Landing',xy=(590160,4227075),xytext=(596200,4227800),ha='left',va='center',fontsize=8,
                arrowprops=dict(arrowstyle='-', relpos=(0,0.5), connectionstyle='arc, angleA=0, angleB=-45,armA=-10,armB=1,rad=0'))
    
    ax.annotate(text='S-42\nSuisun Slough South of\nVolanti Slough',xy=(583500,4226230),xytext=(587100,4229000),ha='left',va='center',fontsize=8,
                arrowprops=dict(arrowstyle='-', relpos=(0,0.5), connectionstyle='arc, angleA=0, angleB=-45,armA=-10,armB=1,rad=0'))
   
    ax.annotate(text='S-21\nChadbourne Slough at\nSunrise Club',xy=(580330,4226380),xytext=(580000,4229612),ha='right',va='center',fontsize=8,
                arrowprops=dict(arrowstyle='-', relpos=(1,0.5), connectionstyle='arc, angleA=0, angleB=45,armA=10,armB=1,rad=0'))

    # ax.annotate(text='S-35\nGoodyear Slough at\nMorrow Island',xy=(579360,4219490),xytext=(578000,4215500),ha='right',va='center',fontsize=8,
    ax.annotate(text='S-35\nGoodyear Slough at\nMorrow Island',xy=(579360,4219490),xytext=(577500,4215800),ha='right',va='center',fontsize=8,
                arrowprops=dict(arrowstyle='-', relpos=(1,0.5), connectionstyle='arc, angleA=0, angleB=45,armA=10,armB=1,rad=0'))

    ax.annotate(text='S-97\nCordelia Slough at\nIbis Club',xy=(577730,4223700),xytext=(576900,4222400),ha='right',va='center',fontsize=8,
                arrowprops=dict(arrowstyle='-', relpos=(1,0.5), connectionstyle='arc, angleA=0, angleB=45,armA=10,armB=1,rad=0'))    


    #Add text showing the standard.
    if month >=6 and month <=9:
        fig.text(.5,.21,f"No PDM Standard for {dt.date.today():%B}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')
    elif month==10:
        fig.text(.5,.21,f"All Stations PDM Standard = {SE[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')
        fig.text(.5,.16,"Chart shows the last 30 days", fontfamily='calibri', color='darkslateblue', fontstyle='italic', ha='center', fontsize=16)        
    elif month == 11:
        fig.text(.5,.21,f"Eastern Stations PDM Standard = {SE[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')
        if deficiencyPeriod==False:
            fig.text(.5,.17,f"Western Stations PDM Standard = {SW[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')
        elif deficiencyPeriod==True:
            fig.text(.5,.21,f"Eastern Stations PDM Standard = {SE[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')           
            fig.text(.5,.17,f"Western Stations Deficiency Period PDM Standard = {SWDP[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')            
        fig.text(.5,.12,"Chart shows the last 30 days", fontfamily='calibri', color='darkslateblue', fontstyle='italic', ha='center', fontsize=16)
    else:
        if deficiencyPeriod==False:
            fig.text(.5,.21,f"All Stations PDM Standard = {SE[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')
            fig.text(.5,.16,"Chart shows the last 30 days", fontfamily='calibri', color='darkslateblue', fontstyle='italic', ha='center', fontsize=16)
        elif deficiencyPeriod==True:
            fig.text(.5,.21,f"Eastern Stations PDM Standard = {SE[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center')           
            fig.text(.5,.15,f"Western Stations Deficiency Period\nPDM Standard = {SWDP[month]:.1f}",color='red',fontsize=16,fontfamily='calibri',fontstyle='italic',ha='center') 
            fig.text(.5,.12,"Chart shows the last 30 days", fontfamily='calibri', color='darkslateblue', fontstyle='italic', ha='center', fontsize=16)

    #Add text showing the chart represents the last 30 days.
    # fig.text(.5,.16,"Chart shows the last 30 days", fontfamily='calibri', color='darkslateblue', fontstyle='italic', ha='center', fontsize=16)
    
    #Add labels for major water units.
    fig.text(.42,.38,"Grizzly Bay",color='royalblue',fontsize=12,fontfamily='calibri',fontstyle='italic',ha='center')
    fig.text(.51,.55,"Montezuma Slough",color='royalblue',fontsize=12,fontfamily='calibri',
             fontstyle='italic',ha='center',rotation=-2)


def DMmap(controlStations, deficiencyPeriod):
    """Creates a background map, and makes function calls to add the timeseries plots."""
 
    fig = plt.figure(figsize=(11,8.5))
    
    ax = fig.add_axes([0.1,0.1,.8,.8])

    createBackground(fig,ax)
   
#    #Set extents for each of the stations.  List values include percent of distance from origin of x and y, and width and height of plots.   
    extents = [('S-35 DM',[.12, .12, .12, .1]),('S-97 DM',[.11, .34, .12, .1]),('S-21 DM',[.165, .77, .12, .1]),('S-42 DM',[.46, .75, .12, .1]),('S-49 DM',[.7, .71, .12, .1])\
               ,('S-64 DM',[.74, .47, .12, .1]),('C-2 DM',[.69, .12, .12, .1])]    
   
#    #Create the timeseries plots.  
    for extent in extents: createTSplot(fig, extent, controlStations, deficiencyPeriod, color='blue')   
    
#    #Create the title.
    fig.text(x=.48,y=.25,s="Daily Mean Salinity Values in mS/cm\n as of {:%B %e, %Y}".format(dt.date.today()),\
             fontfamily='calibri',fontsize=18, fontstyle='italic',color='darkslateblue',linespacing=1.5, ha='center')
        
 
    fig.savefig('Daily Mean Salinities Map.pdf',dpi=100)
    
    

def PDMmap(controlStations, deficiencyPeriod):
    """Creates a background map, and makes function calls to add the timeseries plots."""
 
    fig = plt.figure(figsize=(11,8.5))
    
    ax = fig.add_axes([0.1,0.1,.8,.8])

    createBackground(fig,ax)
   
#    #Set extents for each of the stations.  List values include percent of distance from origin of x and y, and width and height of plots.   
    extents = [('S-35 PDM',[.12, .12, .12, .1]),('S-97 PDM',[.11, .34, .12, .1]),('S-21 PDM',[.165, .77, .12, .1]),('S-42 PDM',[.46, .75, .12, .1]),('S-49 PDM',[.7, .71, .12, .1])\
               ,('S-64 PDM',[.74, .47, .12, .1]),('C-2 PDM',[.69, .12, .12, .1])]    
   
#    #Create the timeseries plots.  
    for extent in extents: createTSplot(fig, extent, controlStations, deficiencyPeriod, color='green')   
    
#    #Create the title.
    fig.text(x=.48,y=.26,s="Progressive Daily Mean Salinity Values in mS/cm\n as of {:%B %e, %Y}".format(dt.date.today()),\
             fontfamily='calibri',fontsize=18, fontstyle='italic',color='darkslateblue',linespacing=1.5, ha='center')
    

    fig.savefig('Progressive Daily Mean Salinities Map.pdf',dpi=100)
    
    return fig

def DMchart(deficiencyPeriod):
    """Creates a time-series plot of the daily means."""
       
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
       
    fig = plt.figure(figsize=(11,8.5))
    
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    #Set marker size.       
    ms=1.5

    ax.plot(df['S-35 DM'],label='S-35',color='grey',ls='--',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(df['S-97 DM'],label='S-97',color='darkgoldenrod',ls='--',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)   
    ax.plot(df['S-49 DM'],label='S-49',color='purple',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)    
    ax.plot(df['S-42 DM'],label='S-42',color='firebrick',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)    
    ax.plot(df['S-21 DM'],label='S-21',color='forestgreen',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(df['S-64 DM'],label='S-64',color='mediumblue',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(df['C-2 DM'],label='C-2',color='goldenrod',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)

    if deficiencyPeriod==False:
        ax.step(df.index,df['Eastern Standards'],color='saddlebrown',label='Eastern\nStandard')
        ax.step(df.index,df['Western Standards'],color='red',label='Western\nStandard') 
    elif deficiencyPeriod==True:
        ax.step(df.index,df['Eastern Standards'],color='saddlebrown',label='Eastern\nStandard')
        ax.step(df.index,df['Western Deficiency Standards'],color='red',label='Western\nDeficiency\nStandard') 
  
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    
    ax.xaxis.set_tick_params(labelsize=10)
    
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    
    ax.grid(b=True, which='major',color='lightgrey',linewidth=0.2,linestyle='-')

    ax.legend(edgecolor='darkgrey', loc='upper left')
    
    #Set the y-extent so that all plots are uniform.
    #Normally, the max is less than 20, so that is the default.
    #But, if it rises over 20, set limit 1 mS/cm over the max value.
    if df[['C-2 DM','S-21 DM','S-42 DM','S-49 DM','S-64 DM','S-35 DM','S-97 DM']].max().max() < 20:
        ax.set_ylim(top=20)
    else:
        ax.set_ylim(top=df[['C-2 DM','S-21 DM','S-42 DM','S-49 DM','S-64 DM','S-35 DM','S-97 DM']].max().max()+1)  
        
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    ax.text(x=0.5,y=1.035,s='Daily Mean Specific Conductance (mS/cm) for Last 30 Days',transform=ax.transAxes,
            bbox=dict(facecolor='white',edgecolor='midnightblue',boxstyle='round',pad=.4),ha='center',fontsize='x-large')
    
    ax.tick_params(labelright=True)
        
    df.to_csv('dm.csv')

    fig.savefig('Daily Mean Specific Conductance for Last 30 Days.pdf',dpi=100)
    
    
    
def PDMchart(deficiencyPeriod):
    """Creates a time-series plot of the progressive daily means."""

    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
    
    fig = plt.figure(figsize=(11,8.5))
    
    ax = fig.add_axes([0.1,0.1,0.8,0.8])   
    
    #Set marker size.
    ms=1.5

    ax.plot(df['S-35 PDM'],label='S-35',color='grey',ls='--',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(df['S-97 PDM'],label='S-97',color='darkgoldenrod',ls='--',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)   
    ax.plot(df['S-49 PDM'],label='S-49',color='purple',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)    
    ax.plot(df['S-42 PDM'],label='S-42',color='firebrick',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)    
    ax.plot(df['S-21 PDM'],label='S-21',color='forestgreen',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(df['S-64 PDM'],label='S-64',color='mediumblue',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(df['C-2 PDM'],label='C-2',color='goldenrod',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)

    if deficiencyPeriod==False:
        ax.step(df.index,df['Eastern Standards'],color='saddlebrown',label='Eastern\nStandard')
        ax.step(df.index,df['Western Standards'],color='red',label='Western\nStandard') 
    elif deficiencyPeriod==True:
        ax.step(df.index,df['Eastern Standards'],color='saddlebrown',label='Eastern\nStandard')
        ax.step(df.index,df['Western Deficiency Standards'],color='red',label='Western\nDeficiency\nStandard') 
  
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    
    ax.xaxis.set_tick_params(labelsize=10)
    
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    
    ax.grid(b=True, which='major',color='lightgrey',linewidth=0.2,linestyle='-')

    ax.legend(edgecolor='darkgrey', loc='upper left')
    
    #Set the y-extent so that all plots are uniform.
    #Normally, the max is less than 20, so that is the default.
    #But, if it rises over 20, set limit 1 mS/cm over the max value.
    if df[['C-2 PDM','S-21 PDM','S-42 PDM','S-49 PDM','S-64 PDM','S-35 PDM','S-97 PDM']].max().max() < 20:
        ax.set_ylim(top=20)
    else:
        ax.set_ylim(top=df[['C-2 PDM','S-21 PDM','S-42 PDM','S-49 PDM','S-64 PDM','S-35 PDM','S-97 PDM']].max().max()+1)   
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    ax.text(x=0.5,y=1.035,s='Progressive Daily Mean Specific Conductance (mS/cm) for Last 30 Days',transform=ax.transAxes,
            bbox=dict(facecolor='white',edgecolor='midnightblue',boxstyle='round',pad=.4),ha='center',fontsize='x-large')
    
    ax.tick_params(labelright=True)
       
    df.to_csv('pdm.csv')

    fig.savefig('Progressive Daily Mean Specific Conductance for Last 30 Days.pdf',dpi=100)    
    
    
    
def emailZip():
    """Emails a zipped copy of the salinity trackers to the group."""
    
    import win32com.client as win32
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    
    emailList = [
    'emp1@water.ca.gov',
    'emp2@water.ca.gov',
    'emp3@water.ca.gov',
    ]
    
    mail.To = ';'.join(emailList)
    mail.Subject = 'Salinity Tracker'
    mail.Body = 'Please see the attached salinity tracker.  Thank you.'
    # mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional
    
    # To attach a file to the email (optional):
    attachment  = r'C:\Users\OneDrive\SalinityTrackers\salinity tracker.zip'
    mail.Attachments.Add(attachment)
    
    mail.Send()    
    
    
def report(controlStations, deficiencyPeriod):
    """Runs all the scripts for the charts, zips the PDFs, and emails them out."""
    
    from zipfile import ZipFile
    
    DMmap(controlStations, deficiencyPeriod)
    PDMmap(controlStations, deficiencyPeriod)
    PDMchart(deficiencyPeriod)
    DMchart(deficiencyPeriod)
    dto()
    sept()
    
    #Run the script to get the Predicted Tides chart using NOAA data.
    tides = 'Observed and Predicted Tides.pdf'
    mytools.predictedTidesChart(88,tides)
    tides = 'Predicted Tides for the next 30 days.pdf'
    mytools.predictedTidesChart_nDays(88, tides)
      
    #Create the zip file.
    with ZipFile('salinity tracker.zip','w') as zipFile:
        zipFile.write('dm.csv')
        zipFile.write('pdm.csv')
        zipFile.write('Progressive Daily Mean Specific Conductance for Last 30 Days.pdf')
        zipFile.write('Daily Mean Specific Conductance for Last 30 Days.pdf')
        zipFile.write('Progressive Daily Mean Salinities Map.pdf')
        zipFile.write('Daily Mean Salinities Map.pdf')
        zipFile.write('Observed and Predicted Tides.pdf')
        zipFile.write('Predicted Tides for the next 30 days.pdf')
        zipFile.write('DTO for the last 30 days.pdf')
        zipFile.write('7-Day Moving Average of Daily Mean of High Tide Specific Conductances.pdf')

    #Email it out.
    emailZip()

def sept(start=None, end=None):

    """Produces a timeseries chart of the 7-Day Moving Averages for the PDMs at
    the 7 key stations.  If no dates are given, the default is to start the data
    record on Aug. 17, and end on the present day.  If the current day is prior to
    Aug. 17, the default will fail.  
    
    The default is for monitoring the current system starting Aug. 24 of the current 
    year.
    
    Otherwise, enter custom dates to examine past years.
    """
    
    import matplotlib.dates as mdates
    
    if start==None:
        
        import pandas as pd

        start = pd.Timestamp(pd.Timestamp.today().year,8,17)    
        
        end = pd.Timestamp.today()-pd.DateOffset(days=1)
    
    data = mytools.getPDMs7(start, end, 'DM').iloc[:,:-1]
    
    ma = data.rolling(window=7).mean()
       
    ma.dropna(inplace=True,how='all')
    
    ma['trigger'] = 17
    
    fig,ax = plt.subplots(figsize=(11,8.5))
    
    ms=4
    
    ax.plot(ma['S-35'],label='S-35',color='grey',ls='--',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms) 
    ax.plot(ma['S-49'],label='S-49',color='purple',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)    
    ax.plot(ma['S-42'],label='S-42',color='firebrick',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)    
    ax.plot(ma['S-21'],label='S-21',color='forestgreen',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(ma['S-64'],label='S-64',color='mediumblue',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(ma['C-2'],label='C-2',color='goldenrod',marker='o',markerfacecolor='grey',markeredgecolor='grey',markersize=ms)
    ax.plot(ma['trigger'],label='Trigger',color='red',lw=2)    

    ax.legend()    
    
    ax.text(ma.index[0],17,'17.0  ',ha='right',va='center',color='red',fontsize='small')

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%#m-%#d'))
    
    ax.set_title('7-Day Moving Average of Daily Mean of High Tide Specific Conductances',fontsize='large',pad=10)
    
    ax.set_ylabel('Specific Conductance (mS/cm)',fontsize='large',labelpad=10)
    
    fig.savefig('7-Day Moving Average of Daily Mean of High Tide Specific Conductances.pdf',dpi=100)
    

def dto():
    """Creates a time-series plot of the Delta Total Outflow."""
    
    import matplotlib.ticker as ticker
    import matplotlib.dates as mdates    

    #Retrieve data series from CDEC.
    dto = mytools.getCDECseries('DTO','23','D',startDate,endDate)
    
    fig,ax = plt.subplots(figsize=(11,8.5))
    
    ax.plot(dto,marker='o',ms=4)
    
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    days = mdates.DayLocator(interval=5)
    
    ax.xaxis.set_major_locator(days)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    
    ax.set_title('Total Detla Outflow for the last 30 days',pad=10,fontdict={'fontsize':12})
    
    ax.set_ylabel('Flow (CFS)',labelpad=10,size=12)
    
    ax.grid('both')
    
    fig.savefig('DTO for the last 30 days.pdf',dpi=100)
    
    
    
        
if __name__=='__main__':
    
    """These scripts are used to manage the salinity in the Suisun Marsh.  The main function is report(), which
    creates the maps and charts of the DM and PDM for the last 30 days.  It also creates .csv files of the 
    data, and a chart of the observed and forecasted tides at Port Chicago.   It then combines everything into 
    a zip file for distribution.
    
    Each of the fuctions that report() runs, namely DMmap(), PDMmap(), DMchart(), and PDMchart() can also be run 
    individually.   Since the PDM Map is also used for the SRCD Board Report, and we don't want the standards 
    to show for that map, we can pass the argument, controlStations=False, to suppress the standards being 
    displayed.   The same can be done for the DM Map, and for running the entire report().
    
    When monitoring the 7-day daily average salinity in September, run the function, sept().  
    
    All charts are saved as PDFs.
    
    When wanting to compare the Delta Total Outflow observed to the predicted values from the OCO, run dto().
    """
    
    #SET PARAMETERS
    deficiencyPeriod=True
    controlStations=True


    report(controlStations, deficiencyPeriod)
    # PDMmap(controlStations=False, deficiencyPeriod=True)
    
    
    # PDMmap(controlStations, deficiencyPeriod)
    # DMmap(controlStations, deficiencyPeriod)
    # PDMchart(deficiencyPeriod)
    # DMchart(deficiencyPeriod)
 
    # sept(start='2020-8-17', end='2020-9-30')
    # sept()
 
    # dto()


 











