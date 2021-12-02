# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 08:11:42 2019

@author: jgalef
"""
import mytools
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


pd.set_option('display.max_colwidth', 20)
pd.options.display.float_format = '{:,.2f}'.format
pd.options.display.expand_frame_repr = False
pd.set_option('display.max_rows',1000000)

def fig1(df, start, end, newDir, deficiencyPeriod):
    """Creates Figure 1: Suisun Marsh Progressive Daily Mean High Tide Specific Conductance."""
      
    fig, ax = plt.subplots(figsize=(11,8.5))
          
    plt.subplots_adjust(left=0.1,right=0.95,top=0.8,bottom=0.1)

    ax.text(0.5,1.1,'Figure 1: Suisun Marsh Progressive Daily Mean High Tide Specific Conductance\n'
            'for the Compliance Stations\n' f'{start:%B %Y}''\n', fontweight='bold', 
            transform=ax.transAxes, ha='center', size='large')   

    easternHandles = []
    easternHandles.append(ax.plot(df['S-49'],label= "Beldon's Landing (S-49)",color='seagreen')[0])
    easternHandles.append(ax.plot(df['S-64'],label='National Steel (S-64)',color='steelblue')[0])
    easternHandles.append(ax.plot(df['C-2'],label='Collinsiville (C-2B)',color='darkslateblue')[0])
    
    easternLegend = plt.legend(handles=easternHandles,title='Eastern Stations',loc=(.76,1.02))
    ax.add_artist(easternLegend)


    westernHandles = []
    westernHandles.append(ax.plot(df['S-21'],label='Sunrise (S-21)',color='firebrick')[0])
    westernHandles.append(ax.plot(df['S-42'],label='Volanti (S-42)',color='darkorange')[0])   
    westernLegend = plt.legend(handles=westernHandles, title='Western Stations',loc=(.01,1.02))
    ax.add_artist(westernLegend)        

    ax.set_ylim([0,20])
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
    
    ax.set_xlabel('Day of month',fontsize='large',fontweight='bold',labelpad=10)
    ax.set_ylabel('Specific Conductance (milliSiemens/cm)', fontsize='large', fontweight='bold', labelpad=10)
          
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%#d")) 
    ax.xaxis.set_tick_params(labelsize=10)    
        
    ax.margins(x=1/df.shape[0])
    
    standardsEastern, normalStandardsWestern, deficiencyStandardsWestern = mytools.getStandardsDetailed()
        
    month = start.month
    
    if deficiencyPeriod==False:
        
        #If any month in the Control Season except November.
        if ((month==10) or (month==12)) or ((month >= 1) and (month <= 5)):
            
            ax.plot(df.index,[standardsEastern[month] for i in range(len(df))],color='red',ls='--')   
            ax.text(df.index[0],standardsEastern[month]+.25, f'Eastern and Western Marsh Standards = {standardsEastern[month]}', 
                     fontsize='medium', ha='left',va='bottom') 
   
        #If November.
        if (month==11):
            ax.plot(df.index,[standardsEastern[month] for i in range(len(df))],color='red',ls='--')   
            ax.text(df.index[0],standardsEastern[month]-.25, f'Eastern Marsh Standard = {standardsEastern[month]}', 
                     fontsize='medium', ha='left',va='top')  
            ax.plot(df.index,[normalStandardsWestern[month] for i in range(len(df))],color='red',ls='--')   
            ax.text(df.index[0],normalStandardsWestern[month]+.25, f'Western Marsh Standard = {normalStandardsWestern[month]}', 
                     fontsize='medium', ha='left',va='bottom')            
               
        
    if deficiencyPeriod==True:
        
        #If October.
        if (month==10):
            ax.plot(df.index,[standardsEastern[month] for i in range(len(df))],color='red',ls='--')   
            ax.text(df.index[0],standardsEastern[month]+.25, f'Eastern and Western Marsh Standards = {standardsEastern[month]}', 
                     fontsize='medium', ha='left',va='bottom') 

        elif ((month==11) or (month==12) or (month>=1 and month<=5)):
            ax.plot(df.index,[standardsEastern[month] for i in range(len(df))],color='red',ls='--')   
            ax.text(df.index[0],standardsEastern[month]-.25, f'Eastern Marsh Standard = {standardsEastern[month]}', 
                     fontsize='medium', ha='left',va='top')  
            ax.plot(df.index,[deficiencyStandardsWestern[month] for i in range(len(df))],color='red',ls='--')   
            ax.text(df.index[0],deficiencyStandardsWestern[month]+.25, f'Western Marsh Deficiency Standard = {deficiencyStandardsWestern[month]}', 
                     fontsize='medium', ha='left',va='bottom')             

    fig.savefig(os.path.join(newDir,'SWRCB figure 1.pdf'), dpi=300)  
    

def fig2(df,start, end,newDir):
    """Creates Figure 2: Suisun Marsh Progressive Daily Mean High Tide Specific Conductance."""
    
    fig, ax = plt.subplots(figsize=(11,8.5))      
    
    plt.subplots_adjust(left=0.1,right=0.95,top=0.8,bottom=0.1)
    
    ax.set_ylim([0,20])
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))

    ax.plot(df['S-35'], label='Morrow Island (S-35)')
    ax.plot(df['S-97'], label='Ibis (S-97)')    
       
    ax.set_title('Figure 2: Suisun Marsh Progressive Daily Mean High Tide Specific Conductance\n'
                  'for the Control Stations\n'
                  '{:%B %Y}\n'.format(start), fontweight='bold')
    
    ax.set_xlabel('Day of month',fontsize='large',labelpad=10,fontweight='bold')
    ax.set_ylabel('Specific Conductance (milliSiemens/cm)', fontsize='large', fontweight='bold', labelpad=8)
    
    ax.legend()
       
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%#d"))
    ax.xaxis.set_tick_params(labelsize=10)    
        
    ax.margins(x=1/df.shape[0])
   
    fig.savefig(os.path.join(newDir,'SWRCB figure 2.pdf'), dpi=300)    


def fig3(start,end,newDir,dfP):
    """Creates Figure 3: Daily Delta Total Outflow and Precipitation."""
    
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)

    fig, ax = plt.subplots(figsize=(11,8.5))    

    dfF = mytools.getCDECseries('DTO', '23', 'D', start, end)
        
    ax.plot(dfF, label='Delta Total Outflow',linewidth=2.3,zorder=20)       
       
    ax.set_ylabel('Delta Total Outflow (cfs)', labelpad=8, fontsize='large', fontweight='bold')
     
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    ax.yaxis.set_tick_params(labelsize=10)
           
    ax2 = ax.twinx()
    ax2.set_ylabel('Rainfall (inches)',rotation=270, labelpad=19, fontsize='large', fontweight='bold')
    
    ax2.bar(dfP.index, dfP,label='Rainfall', color='#CB4335',edgecolor='navy')
  
    ax.grid(axis='y')

    ax.set_zorder(1)
    ax.patch.set_visible(False)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%#d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.margins(x=.015)                                                  
                                                      
    ax.xaxis.set_tick_params(labelsize=11)
   
    ax.set_xlabel('Day of month',fontsize='large',labelpad=10, fontweight='bold')

    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    ax.set_title('Figure 3: Daily Delta Total Outflow and Precipitation\n{:%B %Y}'.format(start),pad=20, fontsize='large', fontweight='bold')
       
    ax.text(-.1,-0.1,'*Rainfall data recorded at Gregory Hill\n in Fairfield, CA',transform=ax.transAxes)
           
    ax.margins(x=0.015)
    ax2.margins(x=0.015)
    
    ax2.set_ylim(bottom=0)
    
    ax.set_ylim([0,dfF.max()+dfF.max()*0.1])
    
    if dfP.max() < 1: ax2.set_ylim(0,1)
   
    fig.savefig(os.path.join(newDir,'SWRCB figure 3.pdf'), dpi=300)
    
    
def fig4(start,newDir,overwriteFigs):
    """Creates Figure 4. Monthly Mean Specific Conductance at High Tide."""
 
    stations = ['C-2 Collinsville','S-64 National Steel','S-49 Beldons','S-42 Volanti','S-21 Sunrise',
                    'S-35 Morrow Island','S-97 Ibis']
    
    stationsWQP = ['2','64','49','42','21', '35','97']    
    
    #Calculate the final day of last month.
    # end = pd.Timestamp.today() - pd.DateOffset(months=1) + pd.offsets.MonthEnd()
    end = start + pd.offsets.MonthEnd()
 
    #Subtract 10 years from 'end.'
    start = end - pd.DateOffset(years=9)

    #Create a list of dates for the end of last month for the last 10 years.
    dates = pd.date_range(start=start, end=end, freq=pd.DateOffset(years=1))

    #Create a list of lists, where each inner list contains the year, station, and end-of-month PDM.
    table=[]
    for date in dates:
        for (station, wqp) in zip(stations, stationsWQP):  
            pdm = mytools.getPDMvalue(wqp,f'{date:%Y-%m-%d}','PDM')
            table.append((date.year,station, pdm))
         
    #Convert the list into a dataframe.       
    df = pd.DataFrame(table, columns=['Year','Station','value'])        
  
    dfY = df.groupby('Year').mean()
    dfY.rename(columns={'value':'Mean'},inplace=True)
   
    wyDict = waterYearTypes()
    wyList = []
    
    #Adjust for water year from WSI page only having one year.  E.g., 2018-2019 is listed as, 2019.
    for year in dfY.index:
        
        if end.month >= 10 and end.month <= 12:
            year = year - 1
 
        wyList.append(year)       
    
    dfY['Water Year'] = wyList
       
    dfY['Type'] = dfY['Water Year'].map(wyDict)
       
    dfY['Diff'] = [abs(dfY['Mean'].iloc[-1] - mean) for mean in dfY['Mean']]
            
    dfY['Rank'] = dfY['Mean'].rank().astype('int32')
    
    dfY['Type'].fillna('Not yet classified',inplace=True)
            
    cards = [1,2,3,4,5,6,7,8,9,10]
    ords = ['','second','third','fourth','fifth','sixth','seventh','eigth','ninth','tenth']
        
    dictOrds = dict(zip(cards,ords))
    
    dfY['Ordinal'] = dfY['Rank'].map(dictOrds)
    
    wy = dfY['Water Year'].loc[dfY['Diff'].iloc[:-1].idxmin()]
    
       
    if (not os.path.exists(os.path.join(newDir,'SWRCB figure 4.pdf')) or overwriteFigs==True):
        
        print("Creating Figure 4")
        
        import seaborn as sns
        
        fig = plt.figure(figsize=(11,8.5))
              
        ax = sns.barplot(x=df['Year'],y=df['value'],hue=df['Station'], edgecolor='darkgrey' )
               
        ax.legend(loc='upper left')   
        
        ax.set_title('Figure 4. Monthly Mean Specific Conductance at High Tide:\n' 
            'Comparison of Monthly Values for Selected Stations\n{:%B} of {:%Y}-{:%Y}\n'
            .format(dates[0], dates[0], dates[-1]), fontweight='bold')
        
        ax.set_xlabel('Year',fontweight='bold',fontsize='large')
        ax.set_ylabel('Specific Conductance (milliSiemens/cm)',fontweight='bold',fontsize='large',labelpad=10)
    
        ax.xaxis.set_tick_params(labelsize=10)
    
        fig.savefig(os.path.join(newDir,'SWRCB figure 4.pdf'), dpi=300)
    
    rank = dictOrds[dfY['Rank'].iloc[-1]]

    return (rank,wy,wyDict[wy])


def gateOps(start):
    
    """Takes information from our SMSCGs operations log, and creates a table for the report.  The ops
    log is an irregular time series that states when operations started and stopped.  The table states,
    for the month of the report, how many days the Gates were in either Tidal or Open modes."""
     
    path=r'Facilities\SMSCG\SMSCG Log.xlsx'
    
    #Set the start equal to the start of the month of the report.
    start = pd.Timestamp(start)
    
    #Set the end to be 23:59 of the final day of the month.
    end = start + pd.offsets.MonthBegin(normalize=True) - pd.Timedelta(minutes=1)
       
    df = pd.read_excel(path,sheet_name='Sheet1',parse_dates=['DATETIME'],index_col='DATETIME',
                       usecols=['DATETIME','FLASHBOARDS', 'GATE 1', 'GATE 2', 'GATE 3','ACTION'])
    
        
  #Need to make a final row with the end date and attributes of the last row of log.
    
    #Make a new dataframe consisting of just the final row.
    last = df.tail(1).copy()    

    #Reset the index to the end date.
    last.index = [pd.Timestamp.today()]
       
    # last.index = [end]
    
    #Append this dataframe to the main dataframe from log.
    df = df.append(last)  
      
    #df was an irregular timeseries.  Now, make a regular timeseries, df2.
    df2 = df.asfreq('T').fillna(method='pad')
              
    #Limit df2 to the reporting month and year.
    df2=df2.loc[start:end]
    
    changeDates = df2.loc[(df2!=df2.shift(1)).any(axis=1)]
      
    log = changeDates.append(df2.tail(1))

    table=[]
    for i in range(len(log)-1):
        
        if log.iloc[i,0]=='OUT':
            fbStatus='Removed'
            blStatus='Non-Operational'
        elif log.iloc[i,0]=='IN':
            fbStatus='Installed'      
            blStatus='Operational'
            
      
        row = f'{log.index[i]:%b. %d %H:%M}\\newline {log.index[i+1]:%b. %d %H:%M}' \
            f' & {log.iloc[i,1]} & {log.iloc[i,2]} & {log.iloc[i,3]} & {fbStatus} & {blStatus}' \
            r' \\ \hline''\n'    
        table.append(row)
        
        
    return table
    

def getHistoricalRainfall(date):
    
    """Returns the historical monthly average rainfall in inches at Fairfield, CA.  Data are retrieved from 
    the US Climate Data webpage."""
    
    #Retrieve a list of html code blocks from the US Climate Data webpage for average rainfaill.
    hList = pd.read_html('https://www.usclimatedata.com/climate/fairfield/california/united-states/usca0364')

    #Parse the html into two tables; one for Jan - Jun, and one for Jul - Dec.
    p1, p2 = hList[0].tail(1).iloc[:,1:].to_numpy()[0], hList[1].tail(1).iloc[:,1:].to_numpy()[0]
    
    #Make a dictionary that returns the average rainfall based on the month entered.
    d = {}
    
    for i in range(1,7): d[i]=p1[i-1]
    for i in range(7,13): d[i]=p2[i-7]
    
    return d[date.month]
    

def waterYearTypes():
    
    """Returns a dictionary that provides the water year type for a given water year.   Data are
    retrieved from CDEC's Water Supply Index (WSI) page."""
    
    from bs4 import BeautifulSoup
    import requests
    
    #Create a request object that retrieves website data.
    r = requests.get('http://cdec.water.ca.gov/reportapp/javareports?name=WSIHIST')
    
    #Parse the website data text.
    soup = BeautifulSoup(r.text,'html.parser')
    
    #The entire WSI data table is stored in the Preamble, so retrieve data in between preamble tags.
    preamble = soup.pre.text    

    #Split each line of the preamble into a list.
    lines = preamble.split('\n')
    
    wyTypes = {'W':'Wet','AN':'Above Normal','BN':'Below Normal','C':'Critical','D':'Dry'}
    
    #Create a dictionary that returns the water year type for a given water year.
    dictWY = {}

    #Start at line 20 of preamble.
    i=20
    while len(lines[i])!=1:
        line = lines[i].split()
        dictWY[int(line[0])] = wyTypes[line[5]]      
        
        i = i+1
    
    lastYear = (pd.Timestamp.today() - pd.DateOffset(years=1)).year
    
    if lastYear not in dictWY:
        dictWY[lastYear] = "Not yet classified"
    
    return(dictWY)


def mergePDFs(newDir,agency):
    
    """Merges together the report PDF and the four figure PDFs into one final PDF."""

    import PyPDF2
    

    #Create the full path of the new pdf file.
    report = os.path.join(newDir,os.path.split(newDir)[1]+'.pdf')
      
    #Make a list of the full paths to each of the Figure PDFs.     
    if agency=='SWRCB':    
        figs = [os.path.join(newDir,f'SWRCB figure {i}.pdf') for i in range(1,5)]
    elif agency=='USBR':
        figs = [os.path.join(newDir.replace('USBR','SWRCB'),f'SWRCB figure {i}.pdf') for i in range(1,5)]

       
    #Add the report path to the list of figure paths.
    pdfs = [report] + figs
    
    #Instantiate a PDF file merger object.
    merger = PyPDF2.PdfFileMerger()
    
    print(f'Merging {agency} Report PDF with Figures')
    
    #For each PDF in the list, read it using the PDF file reader, and append it to the merger object.
    for pdf in pdfs:
        merger.append(PyPDF2.PdfFileReader(pdf,'rb'))


    #Write-out the final merged PDF.
    merger.write(report)


def controlStatement(ser,station):
    """Creates a statement of how the contol stations
    Case 1: Missing PDMs at start and end of month.
    Case 2: Missing PDM at start of month only.
    Case 3: Missing PDM at end of month only.
    Case 4: Data missing for entire month.
    Case 5: No missing PDMs at start or end of month.
    """
    

    #Check for nulls.
    if ser.isnull().any():
        
        #Remove the nans.
        noNulls = ser.copy().dropna()
        
        startDate = noNulls.index[0]
        startValue = noNulls.iloc[0]
        endDate = noNulls.index[-1]
        endValue = noNulls.iloc[-1]
            
        # #Case 1: Missing PDMs at start and end of month.
        if pd.isnull(ser.iloc[0]) and pd.isnull(ser.iloc[-1]):
            statement = f'Due to problems with equipment, data were missing for both the '\
            'beginning and end of the month.  The earliest PDM value of '\
            f'{startValue:.2f} mS/cm was recorded on {startDate:%#m/%#d/%#Y}, and the final PDM value of '\
            f'{endValue:.2f} mS/cm was recorded on {endDate:%#m/%#d/%#Y}.' 
            case=1                     

        #Case 2: Missing PDM at start of month only.
        elif pd.isnull(ser.iloc[0]) and not pd.isnull(ser.iloc[-1]):
             statement = f'Due to problems with equipment, data were missing for the '\
            'beginning of the month.  The earliest PDM value of '\
            f'{startValue:.2f} mS/cm was recorded on {startDate:%#m/%#d/%#Y}.  The salinity ended'\
            f'the month at {endValue:.2f} mS/cm.'
             case=2
        
        #Case 3: Missing PDM at end of month only.
        elif not pd.isnull(ser.iloc[0] and pd.isnull(ser.iloc[-1])):           
            statement = f'Salinity at {station} began the month at {ser.iloc[0]:.2f} mS/cm, but due to problems '\
            'with equipment, data were missing for the end of the month.  The last PDM value of '\
            f'{endValue:.2f} mS/cm was recorded on {endDate:%#m/%#d/%#Y}.'
            case=3
            
        #Case 4: Data missing for entire month.
        elif noNulls.size==0:
            statement = f'Due to problems with equipment at {station}, data were missing for the entire month.'
            case=4
            
    #Case 5: No missing PDMs at start or end of month.
    else:
        statement =  f'Salinity at {station} began the month at {ser.iloc[0]:.2f} mS/cm, and ended the month at '\
        f'{ser.iloc[-1]:.2f} mS/cm.'
        case=5
        endValue=ser.iloc[-1]
        
                
    return statement,case,endValue


def latex(start,deficiencyPeriod=False,overwriteFigs=False):
    
    """Creates a new directory for the month of reporting, creates a LaTeX text file, issues a
    shell command to turn the text file into a PDF, creates the four figure PDFs, and merges them
    all together. """

    #Recast date to timestamp if it was entered as a string.
    start = pd.to_datetime(start)
    
    #Set the end of the month.
    end = start + pd.offsets.MonthEnd()

    #Set the root directory for the reports.
    rootDir = r'Projects\SWRCB Report'
    
    #Create a variable of the year and month for both the name of the directory and the report.  E.g., '2020_02'.
    yearMonth = f'{start:%Y_%m}'
    
    print('\n'f'Creating report for {yearMonth}')
    
    #Set the path for the directory housing the reporting month's files.
    newDir = os.path.join(rootDir,yearMonth) 
    
    #If the directory does not yet exist, create it.
    if not os.path.exists(newDir): 
        print('Creating new directory')
        os.mkdir(newDir)
    
    #Set the name of the tex file for the report.  E.g. '2020_02.tex'.
    texFile = os.path.join(newDir,f'{yearMonth}.tex')
    
    #Open the new tex file for writing.      
    file = open(texFile,'w')
    print('Starting TeX file')

  #Set the preamble.  
    #Lines regarding table colors were commented out.  See doc string. 
    file.write(r'\documentclass[11pt]{article}'+'\n')
    file.write(r'{\renewcommand{\familydefault}{\sfdefault}'+'\n')
    file.write(r'\usepackage{setspace}\onehalfspace'+'\n')
    file.write(r'\usepackage{fancyhdr}'+'\n')
    file.write(r'\usepackage{enumitem}'+'\n')
    file.write(r'\usepackage[margin=1.0in]{geometry}'+'\n')
    file.write(r'\usepackage{array}  '+'\n')
    # file.write(r'\usepackage{color, colortbl}  '+'\n')
    file.write(r'\pagestyle{fancy}'+'\n')
    file.write(r'\setlength{\headheight}{15.2pt}'+'\n')
    file.write(r'\lhead[Channel Water Salinity Report]{Channel Water Salinity Report}'+'\n')
    file.write(f'\\rhead[{start:%B} {start:%Y}]{{{start:%B} {start:%Y}}}'+'\n')
    file.write(r'\renewcommand{\headrulewidth}{0pt}'+'\n')
    # file.write(r'\definecolor{Gray}{gray}{0.8}'+'\n')
    
  #Begin the document.
    file.write(r'\begin{document}'+'\n')
        
  #Set the title page.
    file.write(r'\thispagestyle{empty}'+'\n')
    file.write(r'\begin{center}'+'\n')
    file.write(r'-----------------------------------------------------------------------------------------------\- \\'+'\n')
    file.write(r'\vspace{0.4 in}'+'\n')
    file.write(r'\textbf{{\LARGE Suisun Marsh Monitoring Program}}\\\vspace{0.05 in}'+'\n')
    file.write(r'\textbf{{\LARGE Channel Water Salinity Report}}\break'+'\n\n')
    file.write(f'{{\\Large Reporting Period: {start:%B} {start:%Y}}}'+'\n')
    file.write(r'\vspace{0.4 in}\break'+'\n')
    file.write(r'-----------------------------------------------------------------------------------------------\- \\'+'\n')
    file.write(r'\vspace{4 in}'+'\n')
    file.write(r'Questions regarding this report should be directed to:\\'+'\n')
    file.write(r'\textbf{Jeff Galef}\\'+'\n')
    file.write(r'{\setstretch{1.0}'+'\n')
    file.write(r'California Department of Water Resources\\'+'\n')
    file.write(r'Division of Environmental Services\\'+'\n')
    file.write(r'\clearpage'+'\n')
    file.write(r'\break'+'\n')
    
  #Set the Table of Contents.
    file.write(r'\textbf{\underline{TABLE OF CONTENTS}}\break'+'\n')
    file.write(r'\end{center}'+'\n')
    file.write(r'\begin{flushleft}'+'\n')
    file.write(r'{\setstretch{1.0}'+'\n')
    file.write(r'\begin{enumerate}[label=\arabic*,leftmargin=*,labelsep=2ex,ref=\arabic*]'+'\n')
    file.write(r'\item \textbf{SUISUN MARSH MONITORING STATIONS AND REPORTING REQUIREMENT \dotfill} \pageref{s1}'+'\n\n')
    file.write(r'\item \textbf{MONITORING RESULTS \dotfill} \pageref{s2} '+'\n\n')
    file.write(r'\begin{enumerate}[label*=.\arabic*,leftmargin=*,labelsep=2ex]'+'\n\n')
    file.write(r'\item Channel Water Salinity Compliance \dotfill \pageref{s2.1}'+'\n\n')
    file.write(r'\item  Delta Outflow \dotfill \pageref{s2.2}'+'\n\n')
    file.write(r'\item Precipitation \dotfill \pageref{s2.3}'+'\n\n')
    file.write(r'\item  Suisun Marsh Salinity Control Operations \dotfill \pageref{s2.4} '+'\n\n')
    file.write(r'\end{enumerate}'+'\n\n')
    file.write(r'\item \textbf{DISCUSSION} \dotfill \pageref{s3}'+'\n\n')
    file.write(r'\begin{enumerate}[label*=.\arabic*,leftmargin=*,labelsep=2ex]'+'\n\n')
    file.write(r'\item Factors Affecting Channel Water Salinity in the Suisun Marsh \dotfill \pageref{s3.1}'+'\n\n')
    file.write(r'\item  Observations and Trends \dotfill \pageref{s3.2}'+'\n\n')
    file.write(r'\begin{enumerate}[label*=.\arabic*,leftmargin=*,labelsep=2ex]'+'\n\n')
    file.write(r'\item Conditions During the Reporting Period \dotfill \pageref{s3.2.1}'+'\n\n')
    file.write(r'\item Comparison of Reporting Period with Previous Years \dotfill \pageref{s3.2.2}'+'\n\n')
    file.write(r'\end{enumerate}'+'\n\n')
    file.write(r'\end{enumerate}'+'\n\n')
    file.write(r'\item \textbf{LIST OF FIGURES} '+'\n\n')
    file.write(r'\begin{enumerate}[label=Figure \arabic*,leftmargin=*,labelsep=2ex]'+'\n\n')
    file.write(r'\item Suisun Marsh Progressive Daily Mean High Tide Specific Conductance for Compliance Stations'+'\n\n')    
    file.write(r'\item Suisun Marsh Progressive Daily Mean High Tide Specific Conductance for Monitoring Stations'+'\n\n')  
    file.write(r'\item Daily Net Delta Outflow and Precipitation'+'\n\n')  
    file.write(r'\item Monthly Mean Specific Conductance at High Tide: Comparison of Monthly Values for Selected Stations '+'\n\n')  
    file.write(r'\end{enumerate}'+'\n') 
    file.write(r'\end{enumerate}}  '+'\n') 
    file.write(r'\clearpage'+'\n') 
    
  #Section 1.  SUISUN MARSH MONITORING STATIONS AND REPORTING REQUIREMENT
    file.write(r'\textbf{1.  SUISUN MARSH MONITORING STATIONS AND REPORTING REQUIREMENT} \label{s1} \break'+'\n\n') 
    file.write(r'As per the State Water Resources Control Board (SWRCB) Water Rights Decision 1641 (D-1641),' 
               'the California Department of Water Resources (DWR) is required to provide monthly channel water'
               ' salinity compliance reports for the Suisun Marsh to the SWRCB.  Conditions of channel water salinity '
               'in the Suisun Marsh are determined by monitoring specific electrical conductivity, which is referred '
               r'as "specific conductance" (SC).\break'+'\n\n') 
    file.write(r'The monthly reports are submitted during the Control Season each year in accordance with SWRCB '
               'requirements.  The reports are required to include salinity data from the stations listed below to '
               r'ensure salinity standards are met to protect habitat for waterfowl in managed wetlands: \break'+'\n\n')   

  #Table listing compliance stations.
    file.write(r'\begin{center}'+'\n')  
    file.write(r'\begin{tabular}{| c | c | c | }'+'\n')  
    file.write(r'\hline'+'\n')  
    # file.write(r'\rowcolor{Gray}'+'\n')  
    file.write(r'\multicolumn{3}{|c|}{\textbf{Compliance Stations:}}\\'+'\n')  
    file.write(r'\hline'+'\n')  
    file.write(r'\textbf{Station Identification} & \textbf{Station Name} & \textbf{General Location} \\'+'\n')  
    file.write(r'\hline'+'\n')  
    file.write(r'C-2 & Collinsville & Western Delta\\'+'\n')  
    file.write(r'\hline'+'\n')  
    file.write(r'S-21 & Sunrise & North-Western Suisun Marsh\\'+'\n')  
    file.write(r'\hline'+'\n')  
    file.write(r'S-42 & Volanti & North-Western Suisun Marsh\\'+'\n')      
    file.write(r'\hline'+'\n')  
    file.write(r"S-49 & Beldon's Landing & North-Central Suisun Marsh\\"+'\n') 
    file.write(r'\hline'+'\n')  
    file.write(r'S-64 & National Steel & Eastern Suisun Marsh\\'+'\n')         
    file.write(r'\hline'+'\n')  
    file.write(r'\end{tabular}\break'+'\n')             
    file.write(r'\end{center}'+'\n')     
    
    file.write(r'Data from the stations listed below are included in the monthly reports to provide '
               r'information on salinity conditions in the western Suisun Marsh: \break'+'\n')
    
  #Table listing control stations.
    file.write(r'\begin{center}'+'\n')   
    file.write(r'\begin{tabular}{| c | c | c | }'+'\n')   
    file.write(r'\hline'+'\n')   
    file.write(r'\multicolumn{3}{|c|}{\textbf{Control Stations:}}\\'+'\n')   
    file.write(r'\hline'+'\n')  
    # file.write(r'\rowcolor{Gray}'+'\n') 
    file.write(r'\textbf{Station Identification} & \textbf{Station Name} & \textbf{General Location} \\'+'\n')   
    file.write(r'\hline'+'\n')   
    file.write(r'S-35 & Morrow Island & South-Western Suisun Marsh\\'+'\n')   
    file.write(r'\hline'+'\n') 
    file.write(r'S-97 & Ibis & Western Suisun Marsh\\'+'\n')   
    file.write(r'\hline'+'\n')   
    file.write(r'\end{tabular}\break'+'\n')   
    file.write(r'\end{center}'+'\n')       
    
    file.write(r'Information on Delta outflow, area rainfall, and operation of the Suisun Marsh Salinity '
               'Control Gates are also included in the monthly reports to provide information on '
                r'conditions that could affect channel water salinity in the Marsh.\break'+'\n\n')
    
  #Section 2.  MONITORING RESULTS.
    file.write(r'\textbf{2.  MONITORING RESULTS} \label{s2} \break'+'\n\n')   
    file.write(r'\textbf{2.1 Channel Water Salinity Compliance} \label{s2.1} \break'+'\n\n')   
 
    #Retrieve dataframe of PDMs for the reporting month for the 7 stations.           
    df = mytools.getPDMs7(start, end, 'PDM', standards=True)     
    

    #Create Figures 1 and 2.


    if (not os.path.exists(os.path.join(newDir,'SWRCB figure 1.pdf')) or overwriteFigs==True): 
        print('Creating Figure 1')        
        fig1(df,start,end,newDir,deficiencyPeriod)

    if (not os.path.exists(os.path.join(newDir,'SWRCB figure 2.pdf')) or overwriteFigs==True): 
        print('Creating Figure 2')        
        fig2(df,start,end,newDir)

          
    #Make list of the compliance stations.
    comps = ['C-2','S-21','S-42','S-49','S-64']       

         
  #Create a dataframe for the report text and Table 1, stating whether each compliance station met the standard.    
    
    #Dataframe will have the complaince stations for the index, and standards info for the columns.
    table1 = pd.DataFrame(index=comps,columns=['EC','Normal Standard','Normal Standard Met',
                                               'Deficiency Standard','Deficiency Standard Met'])

    #Add a new column that contains the end-of-month PDM for each of the compliance stations.   
    # table1['EC'] = df[comps].tail(1).copy().to_numpy()[0]
    table1['EC'] = df[comps].tail(1).to_numpy(copy=True).flatten()
    

    if ((start.month>=1) and (start.month<=5) or (start.month>=10)):
        inControlSeason = True
    else:
        inControlSeason = False

 
    #Populate table with 'Yes' or 'No' for each station if standard met.
    if (inControlSeason==False):
        table1.loc[:,2:] = 'N/A'
        file.write('There are no standards outside of the Control Season.\\break \n\n')
        
        table1.loc[comps,['Normal Standard','Normal Standard Met','Deficiency Standard',
                          'Deficiency Standard Met']] = 'N/A'
      
    
    elif (inControlSeason==True):                  
        
        
        #Retrieve detailed standards dictionaries.
        standardsEastern, normalStandardsWestern, deficiencyStandardsWestern = mytools.getStandardsDetailed()           
    
        if (deficiencyPeriod==False):       
            table1.loc[['C-2','S-49','S-64'],'Normal Standard'] = standardsEastern[start.month]
            table1.loc[['S-21','S-42'],'Normal Standard'] = normalStandardsWestern[start.month]
            table1.loc[:,['Deficiency Standard','Deficiency Standard Met']] = 'N/A'
            table1['Normal Standard Met'] = ["Yes" if (row['Normal Standard']>row['EC']) else "No" for index,row in table1.iterrows()]
            valueCounts = table1['Normal Standard Met'].value_counts()
        
        elif (deficiencyPeriod==True):
            table1.loc[['C-2','S-49','S-64'],'Deficiency Standard'] = standardsEastern[start.month]
            table1.loc[['S-21','S-42'],'Deficiency Standard'] = deficiencyStandardsWestern[start.month]
            table1.loc[:,['Normal Standard','Normal Standard Met']] = 'N/A'
            table1['Deficiency Standard Met'] = ["Yes" if (row['Deficiency Standard']>row['EC']) else "No" for index,row in table1.iterrows()]     
            valueCounts = table1['Deficiency Standard Met'].value_counts()
        
        #Total up the number of stations in compliance.
        if 'Yes' in valueCounts:
            total_compliance = valueCounts['Yes']
        else: 
            total_compliance = 0
            
        #Make a dictionary of statements depending on the number of stations in compliance.       
        statements = {0:'none of the five compliance stations were',
                      1:'one of the five compliance stations was',
                      2:'two of the five compliance stations were',
                      3:'three of the five compliance stations were',
                      4:'four of the five compliance stations were',
                      5:'all five compliance stations were'}
        
        #Write compliance paragraph with statement from dictionary above.    
        file.write(f'During the month of {start:%B} {start:%Y}, {statements[total_compliance]} within '
                   'channel water salinity standards (Table 1). Compliance with standards for the month '
                   'was determined for each compliance station by comparing the progressive daily mean '
                   f'(PDM) of high tide SC with respective standards.  ')
        
        #Add final sentence stating what the standards were for that month.           
        if (start.month!=11 and deficiencyPeriod==False):
            file.write(f'The {start:%B} standard for all Marsh stations was {standardsEastern[start.month]} '
                       'mS/cm.\\break'+'\n\n')           
        elif (start.month==11 and deficiencyPeriod==False):
            file.write(f'The {start:%B} standard for the Eastern Marsh stations was {standardsEastern[start.month]} mS/cm, '
                       f'while the standard for the Western Marsh stations was {normalStandardsWestern[start.month]} '
                       'mS/cm.\\break'+'\n\n')       
        elif deficiencyPeriod==True:
            file.write(f'The {start:%B} standard for the Eastern Marsh stations was {standardsEastern[start.month]} mS/cm, '
                       f'while the deficiency standard for the Western Marsh stations was {deficiencyStandardsWestern[start.month]} '
                       'mS/cm.\\break'+'\n\n')   
    
        #State the PDM equation.      
        file.write(r'The progressive daily mean is the monthly average of both daily high tide SC values.  '
                   'The mathematical equation is shown below:\\break'+'\n\n') 
        file.write(r'\[ \mbox{PDM} = \frac{\Sigma \mbox{ daily average of high tide specific conductance}  }  {\mbox{number of days in the month}}\]\break'+'\n\n')             




  #Section 2.2  Delta Outflow.
    file.write(r'\textbf{2.2 Delta Outflow} \label{s2.2} \break'+'\n\n')             

    #Retrieve Delta Total Outflow daily flow values for the reporting month from the CDEC web api.
    dfF = mytools.getCDECseries('DTO', '23', 'D', start, end)
    
    #Use Pandas' describe method to calculate statistics on the DTO series and write to document.
    dfS = dfF.describe()
    file.write(r'Delta outflow is represented by the Delta Total Outflow (DTO) parameter. The DTO for '
               f'{start:%B %Y} ranged between {dfS["min"]:,.0f} cfs and {dfS["max"]:,.0f} cfs. The mean DTO for the month '
               f'was {dfS["mean"]:,.0f} cfs.\\break'+'\n\n')  

  #Section 2.3  Precipitation.        
    file.write(r'\textbf{2.3 Precipitation} \label{s2.3} \break'+'\n\n')

    #Retrieve the historical average rainfall at Fairfield for the reporting month.    
    histAvg = getHistoricalRainfall(start)    
    
    #Retrieve the daily rainfall values at the Gregory Hill station in Fairfield.
    serP = mytools.getCDECseries('GGH','45','E',start,end,get_url=False).resample('D').sum()
       
    #Sum the month's rainfall.
    total = serP.sum()
       
    #Total the number of days of rainfall.
    days = serP[serP > 0].count()        
 
    #Avoid division by 0.
    if histAvg==0:
        
        if days==1:
            
             file.write(f'There was {days} recorded day of precipitation in {start:%B} in Fairfield. The total rainfall was '
                       f'{total:.2f} inches. The historical average precipitation for {start:%B} in Fairfield is {histAvg:.2f} inches.  '
                       'Measurements were recorded at Gregory Hill in Fairfield.\\break'+'\n\n')               
        else:    
        
             file.write(f'There were {days} recorded days of precipitation in {start:%B} in Fairfield. The total rainfall was '
                       f'{total:.2f} inches. The historical average precipitation for {start:%B} in Fairfield is {histAvg:.2f} inches.  '
                       'Measurements were recorded at Gregory Hill in Fairfield.\\break'+'\n\n')      
         
    elif histAvg>0:
 
        #Calculate the percent of the historical average.    
        percent = total/histAvg*100
        
        if days==1:
            file.write(f'There was {days} recorded day of precipitation in {start:%B} in Fairfield. The total rainfall was '
                   f'{total:.2f} inches. The historical average precipitation for {start:%B} in Fairfield is {histAvg:.2f} inches.  '
                   f'The total rainfall was {percent:.1f} percent of average. Measurements were recorded at '
                   'Gregory Hill in Fairfield.\\break'+'\n\n')               
            
        else:
            file.write(f'There were {days} recorded days of precipitation in {start:%B} in Fairfield. The total rainfall was '
                       f'{total:.2f} inches. The historical average precipitation for {start:%B} in Fairfield is {histAvg:.2f} inches.  '
                       f'The total rainfall was {percent:.1f} percent of average. Measurements were recorded at '
                       'Gregory Hill in Fairfield.\\break'+'\n\n')     


    #Create Figure 3.
    if (not os.path.exists(os.path.join(newDir,'SWRCB figure 3.pdf')) or overwriteFigs==True): 
        fig3(start,end,newDir,serP)  
        print('Creating Figure 3')

    
  #2.4 Suisun Marsh Salinity Control Gates Operations

    file.write(r'\textbf{2.4 Suisun Marsh Salinity Control Gates Operations} \label{s2.4} \break'+'\n\n')            

    file.write(r'Operations and flashboard/boat lock installations at the Suisun Marsh Salinity Control '
             f'Gates (SMSCG) during {start:%B %Y} are summarized below:\\break'+'\n\n') 
     
    #Retrieve table of gate operations for the reporting month.
    gateTable = gateOps(start)
     
    #Make SMSCGs Operations Table. 
    file.write(r'\begin{center}'+'\n')  
    file.write(r'\bgroup''\n')
    file.write(r'\def\arraystretch{1.2}''\n')  
    file.write(r'\begin{singlespace}''\n')   
    file.write(r'\newcolumntype{M}[1]{>{\centering\arraybackslash}m{#1}}''\n')  
    file.write(r'\begin{tabular}{ |  M{2.6cm} | M{1.3cm} | M{1.3cm} | M{1.3cm} | M{2cm} | M{2cm} |} \hline''\n')      
    file.write(r'\textbf{Dates} & \textbf{Gate 1} & \textbf{Gate 2} & \textbf{Gate 3} & \textbf{Flashboards} '\
               r'& \textbf{Boat Lock} \\ \hline''\n')
    for row in gateTable:
        file.write(row)        
    file.write(r'\end{tabular}''\n')    
    file.write(r'\end{singlespace}''\n')  
    file.write(r'\egroup''\n')  
    file.write(r'\end{center}'+'\n')  
    file.write(r'\break'+'\n') 
          
  #DISCUSSION
  #3.1  Factors Affecting Channel Water Salinity in the Suisun Marsh
    file.write(r'\textbf{3. DISCUSSION} \label{s3} \break'+'\n\n')             
    file.write(r'\textbf{3.1 Factors Affecting Channel Water Salinity in the Suisun Marsh} \label{s3.1} \break'+'\n\n')
    file.write(r'Factors that affect channel water salinity levels in the Suisun Marsh include:'+'\n')   
    file.write(r'\begin{itemize}'+'\n')   
    file.write(r'\setlength\itemsep{0em}'+'\n')   
    file.write(r'\item Delta outflow'+'\n')   
    file.write(r'\item tidal exchange'+'\n')   
    file.write(r'\item rainfall and local creek inflow'+'\n')   
    file.write(r'\item managed wetland operations'+'\n')   
    file.write(r'\item operations of the SMSCG and flashboard configurations\break'+'\n')   
    file.write(r'\end{itemize} '+'\n\n')     
    
  #3.2 Observation and Trends
    file.write(r'\textbf{3.2 Observation and Trends} \label{s3.2} \break'+'\n\n') 
    
  #3.2.1 Conditions During the Reporting Period    
    file.write(r'\textbf{3.2.1 Conditions During the Reporting Period} \label{s3.2.1} \break'+'\n\n')             

    file.write(f'For {start:%B %Y}, PDM salinity levels at the five compliance stations are shown in '
               f'Figure 1. Salinity levels for {start:%B} started in the range of {df[comps].min(axis=1).iloc[0]:.2f} '
               f'mS/cm to {df[comps].max(axis=1).iloc[0]:.2f} mS/cm, and ended the month in the range of '
               f'{df[comps].min(axis=1).iloc[-1]:.2f} mS/cm to {df[comps].max(axis=1).iloc[-1]:.2f} mS/cm.\\break'+'\n\n')      

    file.write('PDM salinity levels at the control stations S-35 and S-97 are shown in Figure 2. ')
    file.write(controlStatement(df['S-35'],'S-35')[0]+'  ')
    file.write(controlStatement(df['S-97'],'S-97')[0] + '\\break \n\n')          
                  
  #3.2.2 Comparison of Reporting Period Conditions with Previous Years
    file.write(r'\textbf{3.2.2 Comparison of Reporting Period Conditions with Previous Years} \label{s3.2.2} \break'+'\n\n') 
        
    #Create Figure 4 and retrieve information about how this month compared with the same month in the last 10 years.
    rank, closestYear, closestType = fig4(start,newDir,overwriteFigs)   
       
    file.write(f'Monthly mean high tide SC at the compliance and monitoring stations for {start:%B %Y} '
                'were compared with means for those months during the previous nine years (Figure 4).  '
                f'The average salinity for {start:%B %Y} at all compliance and monitoring stations ranked '
                f'{rank} lowest in the past 10 years. The salinity trend is similar to {start:%B} {closestYear}, ')
    
    if closestType=='Not yet classified':
        file.write(r'which belonged to a water year whose type has yet to be classified.' +  '\\break \n\n') 
    else:
        file.write(f'which belonged to a water year classified as, {closestType}. \\break'+'\n\n')    
         
    file.write(r'\pagebreak'+'\n')    

  #Create Table 1.         
    file.write(r'\begin{center}'+'\n')             
    file.write(r'{\setstretch{1.0}\textbf{Table 1: Monthly Mean High Tide Specific Conductance at \\Suisun Marsh'+'\n')
    file.write(r'Water Quality Compliance Stations\\'+'\n') 
    file.write(f'{start:%B %Y}'+'\n')   
    file.write(r'}}\break'+'\n\n')  
    file.write(r'\newcolumntype{M}[1]{>{\centering\arraybackslash}m{#1}}'+'\n')   
    file.write(r'\begin{tabular}{ |  M{2.4cm} | M{2.4cm} | M{2cm} | M{2cm} | M{2cm} | M{2cm} | }'+'\n')   
    file.write(r'\hline'+'\n')   
    # file.write(r'\rowcolor{Gray}'+'\n') 
    file.write(r'\textbf{\hfil Station \newline Identification} & \textbf{Specific \newline Conductance* \newline (mS/cm)} '
               r'& \textbf{Normal Standard} & \textbf{Normal Standard Met?}'+'\n')   
    file.write(r'& \textbf{Deficiency Standard} & \textbf{Deficiency Standard Met?} \\'+'\n')   
    file.write(r'\hline'+'\n')   


    for comp in comps:

        file.write(f'{comp} & {table1.loc[f"{comp}","EC"]:.2f} & {table1.loc[f"{comp}","Normal Standard"]} & {table1.loc[f"{comp}","Normal Standard Met"]}'
                    f'& {table1.loc[f"{comp}","Deficiency Standard"]} & {table1.loc[f"{comp}","Deficiency Standard Met"]}\\\\'+'\n')   
        file.write(r'\hline'+'\n')   
 
    file.write(r'\end{tabular}'+'\n') 
    file.write(r'\end{center}'+'\n\n') 
    file.write(r'*milliSiemens per centimeter'+'\n\n') 
    file.write(r'\end{flushleft}'+'\n') 
    file.write(r'\end{document}'+'\n')       
    
    #Close the TeX file.
    file.close()
    
    #Issue shell command to pdflatex program to turn the TeX file into a PDF.
    print('Compiling TeX file into PDF')
    os.system(f'pdflatex -output-directory "{newDir}" "{texFile}"')
    os.system(f'pdflatex -output-directory "{newDir}" "{texFile}"')

    #Merge the PDFs into one final document.
    # print('Merging report PDF with Figures')
    # mergePDFs(newDir)


def usbr(start):
    """Takes the SWRCB Report and modifies to create the USBR Report."""

    start = pd.to_datetime(start)
    
    #Set the root directory for the reports.
    rootDir = r'Projects\USBR Report'
    
    #Create a variable of the year and month for both the name of the directory and the report.  E.g., '2020_02'.
    yearMonth = f'{start:%Y_%m}'
    
    print('\n'f'Creating report for {yearMonth}')
    
    #Set the path for the directory housing the reporting month's files.
    newDir = os.path.join(rootDir,yearMonth) 
    
    #If the directory does not yet exist, create it.
    if not os.path.exists(newDir): 
        print('Creating new directory')
        os.mkdir(newDir)
    
    #Set the name of the tex file for the report.  E.g. '2020_02.tex'.
    texFile = os.path.join(newDir,f'{yearMonth}.tex')
    
    #Open the new tex file for writing.      
    file = open(texFile,'w')
    print('Starting TeX file')
       
    input = open(f'SWRCB Report\{yearMonth}\{yearMonth}.tex','r')
    
    lines = input.readlines()
    
    for i in range(91):
        file.write(lines[i])
        
    file.write(r'As per the State Water Resources Control Board (SWRCB) Water Rights Decision 1641 (D-1641),' 
               'the California Department of Water Resources (DWR) and the United States Bureau of Reclamation (USBR) '
               'are required to monitor channel water salinity and channel statge within the Suisun Marsh.  Conditions ' 
               'of channel water salinity in the Suisun Marsh are determined by monitoring specific electrical conductivity, '
               'which is referred as "specific conductance" (SC). Channel stage is monitored in feet based on the height of '
               r'the channel water above sea level. \break'+'\n\n') 

    file.write(r'USBR has entered into a Financial Assistance Agreement (No. R19AC00084) with DWR to share a percentage of costs '
               'incurred by DWR related to maintaining water quality and quantity, and improving wetland habitat in the '
               'Suisun Marsh to mitigate the adverse effects on the Marsh of the Central Valley Project and a portion of the '
               'adverse effects of the upstream diversions. As a commitment to the Agreement, DWR is obligated to provide USBR a '
               'monthly summary of SC and channel stage collected at each of the stations. Monthly summary reports are submitted '
               'year-round in accordance with Objective 5 "Compliance and Reporting" of the Agreement with USBR. Monthly reports '
               'will be submitted to the USBR Grants Office Technical Representative (GOTR) for review. The reports are required '
               'to summarize salinity and channel stage data from the stations listed below to ensure salinity standards are met '
               r'to protect and improve habitat for waterfowl and wildlife in the Suisun Marsh: \break'+'\n\n')  

    for line in lines[95:]:
        file.write(line)        
        
        
    file.close()    
    
    print('Compiling TeX into PDF')
    os.system(f'pdflatex -output-directory "{newDir}" "{texFile}"')
    os.system(f'pdflatex -output-directory "{newDir}" "{texFile}"')
    
    
    


if __name__ == "__main__":
    
    """This script automates the generation of the SWRCB Channel Water Salinity Report.  This report is due monthly during the
    Control Season.  The script will automatically create the report for the previous month, since the report is due the month
    after the reporting period.  To change the date, either change the number of months in the pd.DateOfsset(months=n) statment
    below, or simply enter a string for the first day of the month desired.  E.g., start = '2020-1-1'.  
    
    This script will make a new directory for month of the report.  E.g., '2020_02.' The report will be called, '2020_02.pdf'.  
    
    Since there was no way to automate the setting of whether we're in a Deficiency Period, this must be passed to the latex 
    function.  E.g., if we are in a Deficiency Period, write, latex(start, deficiencyPeriod=True).   When we are NOT in Deficiency
    Period, one does not have to state, deficiencyPeriod=False.  One simply starts the program with, latex(start).
    
    This script makes use of the following Python packages: BeautifulSoup4, Matplotlib, Pandas, Requests, and Seaborn.   
    It also uses a module I wrote called, mytools.
    It uses a Web API to retrieve data from CDEC,  US Climate Data, and the WQP.  It also pulls in data from the SMSCGs Log.
    It typesets the document using, LaTex.  This requires the user to have a MikTex installation.  It requires the following LaTEX packages:
    array, enumitem, fancyhdr, and geometry.  I tried adding row coloring, but it had issues on the final table because the row headers
    were split across multiple rows.  The code is still there, but has been commented out.  
    
    """

    # start = pd.Timestamp.today() - pd.offsets.MonthEnd() - pd.offsets.MonthBegin()

    start = '2021-1-1'
    start = '2020-9-1'
    start = '2020-5-1'
    start = '2021-1-1'
    # gateOps(start)
    
    
    
    # end = '2019-11-30'

    
    latex(start,overwriteFigs=False)
    # usbr(start)    
    
    



    


    

    














