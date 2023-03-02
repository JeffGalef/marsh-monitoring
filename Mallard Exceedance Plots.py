# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:46:09 2023

@author: Jeff Galef.

Creates an Exceedance Probability versus Stage plot, along with the Minimum
Threshold.  In DSS VUE, export a time-series by first bringing up the Table view.
Be sure to select at least two decimal places and click the box, "Print Title."

The input file name can be changed with the 'file' variable.
The output chart file name can be cahnged with the 'outFile' variable.

"""

import pandas as pd
import matplotlib.pyplot as plt



# Set the file path for the data.
file=r"test.csv"

# Open the data file and read in the first line.
with open('test.csv','r') as obj:
    line = obj.readline()
    

# Strip out the node (Channel number and upstream/downstream).
node = line.split('/')[2]

# Set the name of the output chart file.
outFile = f'Exceedance Probability for Channel {node}.pdf'


# Read the relevant data into a dataframe.
df = pd.read_csv(file,header=2,names=['Date','Stage'],usecols=[1,3],parse_dates=True,index_col='Date')


# Sort stage values so rank 1 is the highest stage.
df.sort_values(inplace=True,by='Stage',ascending=False)

# Calculate N, which is n+1.
N = len(df)+1

# Create the rank column.
df['rank'] = range(1,N)

# Calculate the exceedance probability as rank/N.
df['Exceedance Probability'] = df['rank'] / N

# Add a column for the Minimum Threshold values.
df['Minimum Threshold'] = 6.7

# Create the figure and its axes.
fig, ax = plt.subplots()

# Plot the Exceedance Probability versus Stage data.
ax.plot(df['Exceedance Probability'], df['Stage'],label='Channel '+node)

# Plot the Minimum Threshold data.
ax.plot(df['Exceedance Probability'], df['Minimum Threshold'],label='Minimum Threshold', color='red')

# Add gridlines.
ax.grid()

# Set the y label.
ax.set_ylabel('Stage (feet, NAVD88)')

# Set the x label.
ax.set_xlabel('Probability of Exceedance')

# Add a legend.
ax.legend()

# Set the limits for the x-axis.
ax.set_xlim(-0.01,1.01)

# Set the chart title.
# ax.set_title('Channel 574')

fig.savefig(outFile)


