# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 09:15:28 2019

@author: jgalef
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import mytools

pd.set_option('display.max_columns',30)
#pd.set_option('display.max_colwidth',6)
#pd.set_option('display.precision',0)
pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.expand_frame_repr', False)


def makePlot(dfO,station):
    
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3,ncols=1,figsize=(11,8.5),sharex=True)
       
    ax1.plot(dfO.iloc[:,0],label='Observed',color='blue')
    ax1.plot(dfO.iloc[:,1],label='Modeled',color='red')
    ax2.bar(x=dfO.index,height=dfO.iloc[:,2],color='purple')
    ax3.bar(x=dfO.index,height=dfO.iloc[:,3], color='green')    
    
    ax1.legend()
    ax1.set_title('Observed vs. Modeled Comparison for {}'.format(station),pad=10)
    
    ax1.set_ylabel('Flow (CFS)', labelpad=5)
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    ax2.set_ylabel('Flow Difference (CFS)', labelpad=5)
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    
    ax3.set_ylabel('Percent Difference (%)', labelpad=5)
    ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    ax3.xaxis.set_major_locator(mdates.MonthLocator())
    ax3.xaxis.set_minor_locator(mdates.DayLocator(15))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    ax1.grid(b=True, which='major', color='grey', linestyle='-', linewidth=0.25)
    ax2.grid(zorder=0,b=True, which='major', color='grey', linestyle='-', linewidth=0.25)
    ax3.grid(zorder=0,b=True, which='major', color='grey', linestyle='-', linewidth=0.25)
    
    ax3.text(x=1,y=-.25,s="*Gaps are a result of missing Observed data.", transform=ax3.transAxes, ha='right')
    
    fig.subplots_adjust(hspace=0.07)    
    
    plt.savefig(r'R:\DAYFLOW\WY2019\Metadata\\'+station+'.pdf',dpi=600,format='pdf')
    
    

def Rio(dfO):
       
#    dfO['Rio Diff'] = dfO['Sac'] - dfO['RIO']
    dfO['Rio Diff'] = dfO['Sac'] - dfO['RIO']
    
#    dfO['Rio Per Diff'] = dfO['Rio Diff']/dfO['Sac']*100
    dfO['Rio Per Diff'] = dfO['Rio Diff']/dfO['RIO']*100
    
    dfO = dfO[['Sac','RIO','Rio Diff','Rio Per Diff']]
    
    makePlot(dfO,'Sacramento River at Rio Vista')
#    
#    print(dfO.columns)

def Jersey(dfO):
       
#    dfO['Rio Diff'] = dfO['Sac'] - dfO['RIO']
    dfO['Jersey Diff'] = dfO['SJ'] - dfO['WEST']
    
#    dfO['Rio Per Diff'] = dfO['Rio Diff']/dfO['Sac']*100
    dfO['Jersey Per Diff'] = dfO['Jersey Diff']/dfO['WEST']*100
    
    dfO = dfO[['SJ','WEST','Jersey Diff','Jersey Per Diff']]
    
    makePlot(dfO,'San Joaquin River at Jersey Point')
#    
#    print(dfO.columns)


def Chipps(dfO):
       
#    dfO['Rio Diff'] = dfO['Sac'] - dfO['RIO']
    dfO['Diff'] = dfO['Total'] - dfO['OUT']
    
#    dfO['Rio Per Diff'] = dfO['Rio Diff']/dfO['Sac']*100
    dfO['Per Diff'] = dfO['Diff']/dfO['OUT']*100
    
    dfO = dfO[['Total','OUT','Diff','Per Diff']]
    
    makePlot(dfO,'Total Delta Outflow at Chipps Island')
#    
#    print(dfO.columns)


def X2(df):
    
    fig = plt.figure(figsize=(11.5,8))
    
    axL = fig.add_axes([0.1,0.1,.8,.8])
    
    axR = axL.twinx()
    
    axL.plot(df['X2'],label='X2',color='red')
    axR.plot(df['OUT'],label='Delta Outflow',color='blue')
    
    axL.set_ylabel('X2 (km)', labelpad=5)
    axR.set_ylabel('Outflow (CFS)', labelpad=15, rotation=-90)
    axR.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    fig.legend(loc='upper right',bbox_to_anchor=(0,0,0.89,0.89))



def missing(df):
    
    print('\nMissing Sacramento River at Rio Vista dates.')
    print(df.index[df['Sac'].isnull()])
    
    print('\nMissing San Joaquin River at Vernalis dates.')
    print(df.index[df['SJ'].isnull()])
    
    
    print('\nMissing Threemile Slough near Rio Vista dates.')
    print(df.index[df['3Mile'].isnull()])
    
    
    print('\nMissing Dutch Slough at Jersey Island dates.')
    print(df.index[df['DS'].isnull()])
    
    


dayflowFile = r'R:\DAYFLOW\WY2019\Output\dayflowCalculations2019.csv'

df = pd.read_csv(dayflowFile,index_col=False,nrows=365)

df['Date'].apply(lambda x:x.title())

df['Date'] = pd.to_datetime(df['Date'], format = '%d%b%Y')

df.set_index('Date',inplace=True)

dfRio = mytools.getUSGS(parameter='72137',siteNumber = '11455420',start=df.index[0],end=df.index[-1])

df3M = mytools.getUSGS(parameter='72137',siteNumber = '11337080',start=df.index[0],end=df.index[-1])

dfSJ = mytools.getUSGS(parameter='72137',siteNumber = '11337190',start=df.index[0],end=df.index[-1])

dfDS = mytools.getUSGS(parameter='72137',siteNumber = '11313433',start=df.index[0],end=df.index[-1])

dfO = pd.concat([dfRio['CFS'],df3M['CFS'],dfSJ['CFS'],dfDS['CFS']],axis=1)

dfO.columns = ['Sac','3Mile','SJ','DS']

#dfO.interpolate(inplace=True)

dfO['Total'] = dfO.sum(axis=1,skipna=False)

#print(dfO)

dfO = dfO.join(df)

#missing(dfO)
X2(dfO)

#Rio(dfO)
#Jersey(dfO)
#Chipps(dfO)












#fig, (ax1, ax2) = plt.subplots(nrows=2,ncols=1,figsize=(11,8.5),sharex=True)
#
#ax1.plot(dfO['Dayflow'],label='Dayflow',color='blue')
#ax1.plot(dfO['Observed'],label='Observed',color='red')
#ax2.bar(x=dfO.index,height=dfO['PercentDiff'], color='green')
#
#ax1.legend()
#
#
#ax1.set_ylabel('Flow (CFS)', labelpad=5)
#ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
#
#ax2.set_ylabel('Percent Difference (%)', labelpad=5)
#ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

#ax2.xaxis.set_major_locator(mdates.MonthLocator())
#ax2.xaxis.set_minor_locator(mdates.DayLocator(15))
#ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

















