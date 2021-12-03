# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 09:37:37 2021

@author: jgalef
"""


"""Produces a stacked time-series chart showing the PDMs at the Compliance and 
Control Stations, whether the SMSCGs are operating, the Total Delta Outflow,
the phases of the Moon, and the stage at Port Chicago."""


import mytools
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from matplotlib.ticker import FixedLocator
import matplotlib.dates as mdates


start='2021-10-1'
end='2021-10-31'  
start='2021-10-15'
end='2021-11-15'  

dto = mytools.getCDECseries('DTO', '23', 'D', start, end)
phases = mytools.getLunarPhases(start,end)
met = mytools.get_PortChicago(start,end,'met')
stages = mytools.get_PortChicago(start,end,'stage')     
df = mytools.getPDMs7(start, end, 'DM', standards=True)
ops = mytools.get_gateOps(start,end)

fig, (axEC,axOps,axFlow,axLunar,axStage) = plt.subplots(5,1,figsize=(11,8.5),gridspec_kw=
                                                                   {'height_ratios':[3,1,2,1,3]})
axFlow.plot(dto,color='royalblue')
#axFlow.yaxis.set_major_locator(LinearLocator(numticks=4))
axFlow.margins(y=0.2)

axEC.plot(df['S-35'],label='S-35',color='grey',ls='--')
axEC.plot(df['S-97'],label='S-97',color='darkgoldenrod',ls='--')
axEC.plot(df['S-49'],label='S-49',color='purple')  
axEC.plot(df['S-42'],label='S-42',color='firebrick')  
axEC.plot(df['S-21'],label='S-21',color='forestgreen')
axEC.plot(df['S-64'],label='S-64',color='mediumblue')
axEC.plot(df['C-2'],label='C-2',color='goldenrod')
axEC.step(df.index,df['Standard'],label='Standard',color='red')
axEC.xaxis.set_ticks([])
axEC.set_ylabel('Daily Mean\nEC (mS/cm)',labelpad=10)

axOps.step(x=ops.index,y=ops,color='orangered')
axOps.set_ylabel('SMSCG\nOps',labelpad=10)
axOps.yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
axOps.yaxis.set_major_locator(FixedLocator([0,1]))
axOps.margins(y=0.2)
axOps.xaxis.set_ticks([])
axOps.set_ylim([-.1,1.5])
    
axStage.plot(stages)

markersize=30

#Map the lunar phases to unicode characters.
phaseMap={'full moon':'$\u25CB$',
          'new moon':'$\u25CF$',
          'first quarter':'$\u25D0$',
          'last quarter':'$\u25D1$'}

for i in range(len(phases)):
    axLunar.plot(phases.index[i],10,linewidth=0,markeredgecolor='None',
              markerfacecolor='black',mew=.0001,markersize=markersize,marker=phaseMap[phases.iloc[i,0]])


axLunar.set_ylabel('Lunar\nPhase',labelpad=10)
axStage.set_ylabel('Stage at\nPort Chicago\n(feet)',labelpad=10)
axFlow.set_ylabel('Delta Total\nOutflow (cfs)',labelpad=10)


axLunar.yaxis.set_ticks([])
axLunar.yaxis.set_ticklabels([])
axLunar.xaxis.set_ticks([])


axFlow.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))


locator = mdates.DayLocator(interval=7,tz='US/Pacific',interval_multiples=True)
axFlow.xaxis.set_major_locator(locator)

axFlow.xaxis.set_ticks([])



axStage.xaxis.set_major_formatter(mdates.DateFormatter('%#m/%#d/%y'))

fig.subplots_adjust(hspace=0.00,top=0.95,bottom=0.1)