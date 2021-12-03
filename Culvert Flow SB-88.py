# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:14:14 2020

@author: jgalef


This script estimates the water diverted into RRDS and MIDS.  

Provide a start and end date in YYY-MM-DD format in the Global parameters section below.

For RRDS, provide an input file of 15-minute data for all 8 gate openings in feet, and the stages in the 
Fish Screen pond.  State the file path in the Global parameters section below.

For MIDS, provide an input file of 15-minute stage data from the MIDS station.   File should also specify whether
the gates were 'Open' or 'Closed' for each 15-minute record in a 'Gates' field.  Also, enter the gate opening in
inches in the Global parameters section below.  State the file path in the Global parameters section below.

"""

import pandas as pd
import numpy as np
from scipy.optimize import brenth, newton
import mytools

pd.set_option('display.max_columns',50)
pd.set_option('display.max_rows',90000)



#Glabal parameters******************************************************************************************************

start,end = '2019-1-1','2019-12-31'

midsInputFile = r'MIDS Stage Data 2019.csv'
rrdsInputFile = r'RRDS Stage Data 2019.csv'


#Enter the MIDS gate openings in inches.   Currently, all 3 of the MIDS gates are only opened to 8 inches.
#If operations become more complex, this code will need to be updated.
midsGateOpening = 8


#***********************************************************************************************************************



def get_kg(percentOpen):
    """Estimates the kg parameter using linear interpolation.  Input data come from 
    "FACTORS INFLUENCING FLOW IN LARGE CONDUITS," Journal of the Hydraulics Division,
    ASCE, Fig. 4, pg. 140."""
    xp = np.linspace(0,100,11)
    fp = np.array([1000,100,24, 9,3.8,1.9,1.05,0.59,0.37,0.24,0.16])  
    kg = np.interp(percentOpen,xp,fp)
    return kg


#Root finders only find x when y=0.  For y != 0, use the args parameter when calling newton.
def f_MIDS(v,hL,kg):
    
    return ((np.square(v)/64.4)*(kg + (29*np.square(0.01)*77) + 1 + 8*np.exp(-1.15*v/2)) - hL)


#Root finders only find x when y=0.  For y != 0, use the args parameter when calling newton.
def f_RRDS(v,hL,kg):
    
    return np.square(v)/64.4*(0.9 + kg + (29*np.square(0.01)*98.5/np.power(1.25,1.33)) + 1 + 8 * np.exp(-1.15*v/np.sqrt(5))) - hL


def calculateUsage_RRDS(rrdsInputFile,start,end):
    
    #Create lists of column names.  FS stands for Fish Screen Pond Stage.
    gateCols = ['Gate'+str(i) for i in range(1,9)]
    cols = ['FS'] +  ['Gate'+str(i) for i in range(1,9)]
    cols = cols + gateCols
    
    
    #Read in the RRDS stage data.
    dfM = pd.read_csv(rrdsInputFile,parse_dates=['DateTime'],index_col='DateTime',na_values='(null)')
    
    #Restrict to start and end.
    dfM = dfM[start:end]
   
    #Rename the verbose Wonderware column names.
    WWcols = 'DTRST.RRDS_CANAL2.LEVEL_USG,DTRST.RRDS_GATE01.POS_FT,DTRST.RRDS_GATE02.POS_FT,DTRST.RRDS_GATE03.POS_FT,'\
    'DTRST.RRDS_GATE04.POS_FT,DTRST.RRDS_GATE05.POS_FT,DTRST.RRDS_GATE06.POS_FT,DTRST.RRDS_GATE07.POS_FT,'\
    'DTRST.RRDS_GATE08.POS_FT'.split(',')
    dfM.rename(columns=dict(zip(WWcols,cols)),inplace=True)
    
    #Get the series of stages for ROR.
    serM = mytools.getCDECseries('ROR',6,'E',start,end,ngvd29=True)
    
    #Rename 'VALUE' to 'ROR.'
    serM = serM.rename('ROR')
    
    #Join the two dataframes together.
    df = dfM.join(serM)   

    #Include only the values where flow into the system would occurr.
    df = df[df['FS']>df['ROR']]
       
    #Interpolate any missing values.
    df.interpolate(inplace=True)
    
    #Calculate the head differential.
    df['Diff'] = df['FS'] - df['ROR']
    
    #Create a list of column names for each of the 8 kg's.
    kgCols = ['kg'+str(i) for i in range(1,9)]    
    
    #Populate the kg columns.
    for (kgCol,gateCol) in zip(kgCols,gateCols):
        kglist = []
        for openings in df[gateCol]:
            
            #Calculate the percent open
            percentOpen = openings/5*100
            
            #Calculate kg and append to list.
            kglist.append(get_kg(percentOpen))
        
        #Create a new column and populate list kg list.
        df[kgCol] = kglist

    #Create a list of column names for each of the 8 v's.
    vCols = ['v'+str(i) for i in range(1,9)]
    
   #Create the velocity columns and populate values.
    #Loop through column names.
    for (kgCol,vCol) in zip(kgCols,vCols):
        vList = []
        #Loop through a kg column, calulate velocities, and append to a list.
        for (hL,kg) in zip(df['Diff'],df[kgCol]):
            #Use Scipy's Newton nonlinear solver. 
            if kg==1000:
                v=0
            else:
                v = newton(f_RRDS,0,args=(hL,kg))
            vList.append(v)
        #Assign velocities to a new velocity column.
        df[vCol] = vList
        
        
    #Create a list of column names for each of the 8 Q's.
    Qcols = ['Q'+str(i) for i in range(1,9)]
    
    for (gateCol,vCol,Qcol) in zip(gateCols,vCols,Qcols):
        Qlist=[]
        for (opening,v) in zip(df[gateCol],df[vCol]):
            area = np.pi * np.square(2.5)
            Q = area * v
            Qlist.append(Q)
        df[Qcol] = Qlist
     
    #Convert from seconds to minutes and calculate the 15-minute total volume.
    df['Volume'] = df[Qcols].sum(axis=1)*15*60
    
    #Total up the whole year and convert to acre-feet.
    total = df['Volume'].sum()/43560
        
     
    
    print('\nTotal water diverted into RRDS = {:,.0f} acre-feet'.format(total))
    

def calculateUsage_MIDS(midsInputFile,start,end):
    
    #Read in the MIDS stage data.
    dfM = pd.read_csv(midsInputFile,parse_dates=['Datetime'],index_col='Datetime')
    
    #Restrict to start and end.
    dfM = dfM[start:end]
    
    #Select only the records where the intake gates were open.
    dfM = dfM[dfM['Gates']=='Open']
    
    
    serG = mytools.getCDECseries('GYS',1,'E',start,end)
    
    serG = serG.rename('GYS')
    
    
    #GYS shifted by 30 mintues to account for travel time to MIDS.
    #From Google Earth, distance is 3,200 ft.   Assuming a speed of
    #2 fps, this comes to 1,800 seconds, or 26.67 minutes.
    serG.index = serG.index.shift(1800,'S')

    #Join the MIDS and GYS dataframes.    
    df = dfM.join(serG)
    
    #Interpolate any missing values.
    df = df.interpolate()
    
    
    #Select only the times where GYS stage is greater than MIDS.
    df = df[df['GYS']>df['MIDS']]
    
    #Calculate the head differential between GYS and MIDS
    df['Difference'] = df['GYS'] - df['MIDS']
    
    #Calculate the velocity (fps) for each culvert every 15 minutues.
    velocities = []
    for hL in df['Difference']:        
        percentOpen = midsGateOpening/48*100
        kg = get_kg(percentOpen)
        velocities.append(brenth(f_MIDS,0,3,args=(hL,kg)))
    

    #Assign to dataframe.
    df['v'] = velocities
    
    #Caculate the flow rate (ft3/s) for all 3 culverts.   r = 2.  r^2 = 4.
    df['Q'] = 3 * df['v'] * np.pi*4
    
    #Convert from seconds to minutes and calculate the 15-minute total volume.
    df['volume'] = df['Q'] * 15 * 60
    
    #Sum up the volumes for the year and convert to acre-ft.
    yearlyTotal = df['volume'].sum()/43560
    
    print("\nTotal water diverted into MIDS = {:,.0f} acre-feet".format(yearlyTotal))
    
    

calculateUsage_MIDS(midsInputFile,start,end)
calculateUsage_RRDS(rrdsInputFile,start,end)