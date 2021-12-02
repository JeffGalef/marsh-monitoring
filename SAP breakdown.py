# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:04:45 2020

@author: jgalef
"""

import pandas as pd
import os
# import numpy as np

# pd.options.display.float_format = '${:,.2f}'.format
pd.options.display.float_format = '{:,.2f}'.format

pd.set_option('display.max_rows', 15000)
pd.set_option('display.expand_frame_repr', False)

def getElementsMap():
    """Returns a dictionary specifying category for SAP element."""
    
    elementsMap = {
        'Electrical Supplies':'OE&E',
        'Year End Absence 60':'Labor Assessment',
        'Construction Supplie':'OE&E',
        'Consult&Pro Svcs-Ext':'Contract',
        'Consult&Pro Svcs-Int':'Contract',
        'DepExpFull WR150':'Depreciation',
        'DepExpFull WR170':'Depreciation',
        'Direct Labor':'Direct Labor',
        'Direct Labor-SRA':'Direct Labor',
        'Environmental Srvcs':'OE&E',
        'Fed Co-op Contracts':'Contract',
        'General Expense':'OE&E',
        'GM Absence Step 60':'Labor Assessment',
        'GM DEP WRRF Acq 60':'Labor Assessment',
        'GM Health Step 60':'Labor Assessment',
        'GM Labor Step 60':'Labor Assessment',
        'GM OE&E Step 60':'Labor Assessment',
        'GM RENT Step 60':'Labor Assessment',
        'GM Retirement Step 6':'Labor Assessment',
        'GM SSA Step 60':'Labor Assessment',
        'GM Work Comp Step 60':'Labor Assessment',
        'LM Absence Step 60':'Labor Assessment',
        'LM Health Step 60':'Labor Assessment',
        'LM Labor Step 60':'Labor Assessment',
        'LM OE&E Step 60':'Labor Assessment',
        'LM RENT Step 60':'Labor Assessment',
        'LM Retirement Step 6':'Labor Assessment',
        'LM SSA Step 60':'Labor Assessment',
        'LM Work Comp Step 60':'Labor Assessment',
        'LS Absence Step 60':'Labor Assessment',
        'LS Health Step 60':'Labor Assessment',
        'LS Labor Step 60':'Labor Assessment',
        'LS POE Step 60':'Labor Assessment',
        'LS Retirement Step 6':'Labor Assessment',
        'LS SSA Step 60':'Labor Assessment',
        'LS Work Comp Step 60':'Labor Assessment',
        'Lab Chem & Gases':'OE&E',
        'Private Car Mileage':'OE&E',
        'R/W & Related Costs':'OE&E',
        'Shipping / Freight':'OE&E',
        'Taxes & Assessments':'OE&E',
        'Training':'OE&E',
        'Moving Services':'OE&E',
        'Communications':'OE&E',
        'Misc Office Supplies':'OE&E'
        }    
    
    return elementsMap

def getSMBmap():
    """Returns a dictionary of SMB employees and job titles."""
    
    smbMap = {
        'JEFF':'Engineer',
        'CLAIRE':'Senior Environmental Scientist Supervisor',
        'ELIZA':'Environmental Scientist',
        'JOHN':'Environmental Scientist',
        'JAMAL':'Engineer',
        'EDWARD':'Senior Engineer',
        'LAUREN':'Environmental Scientist',
        'MICHELLE':'Engineer',
        'THEO':'Senior Environmental Scientist Specialist',
        'ALAN':'Environmental Scientist',
        'JANE':'Water Resources Engineering Associate',
        'JAY':'Environmental Scientist',
        'SABINE':'Environmental Scientist',
        'PHIL':'Senior Environmental Scientist Specialist',
        'STEVE':'Senior Environmental Scientist Supervisor',
        'TRENTON':'Environmental Scientist',
        'ARI':'Environmental Scientist',
        'JERRY':'Environmental Scientist',
        'SUSAN':'Scientific Aide'
        }
        
    return smbMap
    
    


#**********************  Quarterly Functions  ***************************************************    

def listFiles(path):
  """Returns a list of xlsx files in a given directory.   Pass the full paths
    of the directory."""
    
  #Retrieve full list of files in a directory.  
  files = os.listdir(path)  
  
  xlsx = []
  
  #Add xlsx files only to the list.  Exclude ~ lock files.
  for file in files: 
    
    ext = file.split('.')[1]
       
    if (ext == 'xlsx') and (file[0]!='~'): xlsx.append(os.path.join(path,file))
    
  return xlsx




def exploreSummary(rootDir):
    """Provides the unique values of the Element, Name, and Object columns
    from the summary.csv file.   If summary.csv has not been created, this
    function will call buildDF(rootDir).  Values are printed to the screen.
    
    Sample Output:
    
        Unique Elements:
        Construction Supplie
        Consult&Pro Svcs-Ext
        Consult&Pro Svcs-Int
        DepExpFull WR150    
        
        Unique Objects:
        DES Budget & Prog
        DES Budget & Prog / Labor rate 4000-4500
        DES Budget & Prog / Labor rate 5500-6000
        DES Environmental PI
        
        Unique Names:
        023000-1  GM Labor Step 60
        030001-1  GM Labor Step 60
        030001-10 LM Health Step 60
        030001-11 LM SSA Step 60
        
    Elements seem to be the largest class.  
    Names seem to be more detailed.  I can get the employee name or OE&E here.
    Objects tell me which division charged the cost.
        
        """
    

    summaryPath = os.path.join(rootDir, 'summary.csv')

    if not os.path.exists(summaryPath):
        df = buildDF(rootDir)
    
    df = pd.read_csv(summaryPath)
    df.fillna(value='n/a',inplace=True)
    

    elementsMap = getElementsMap()

    # for key in elementsMap.keys():
    #     print(key)
 
  
    ue = df['Element'].unique()
    ue.sort()
    print('\n')
    # for e in ue: print(e)
    
 
    diff = set(ue) - set(elementsMap.keys())   
 
    if len(diff) > 0:
        print('New Unacounted Elements:')
        for d in diff: print(d)
    else:
        print('All elements accounted for.')
        
    # import sys
    # sys.exit()   
    
    
    print('Unique Elements:')
    for i in ue: print(i)
       
    uo = df['Object'].unique()
    uo.sort()
    print('\nUnique Objects:')
    for i in uo: print(i)    
        
    consultants = df.loc[df['Element'].str.contains('Consult'),'Name'].to_frame()   
    consultants['Consultant'] = consultants['Name'].apply(lambda x:x.split(' ')[0])   
    consultants = consultants['Consultant'].unique()   
    consultants.sort()
    print('\nUnique Consultants:')
    for i in consultants: print(i)    
    
    
    print('\nUnique Names:')
    un = df['Name'].unique()
    un.sort()
    for i in un: print(i)
    
def consultantCheck(s):
    
    s = s.split(' ')[0]
    
    if s.isalpha():
        return s
    else:
        return 'OE&E'
        

def sap(rootDir):
    
    """Takes in a full xlsx file path, which is exported from SAP, reads the
    data into a Pandas dataframe, processes the data, and returns a summary of
    information.   This script serves two purposes.   The first is to create
    a summary file that breaks down spending by labor versus overhead, then by
    Susuin Marsh Branch (SMB) job classifications or labor from others that
    we've contracted with, and then returns a table with labor costs broken
    down by SMB classificatons, overhead costs proportional to the SMB 
    proportions, and totals.  If there is work done outside of the SMB, this
    will show up as a separate table.   To get this summary table, submit the
    argument, printSummary=True.   
    
    The second purpose is to return a dataframe of just labor costs that will
    be used by the COtable function to create a grand summary table that lists
    only labor costs broken down by cost object number.
    
    # Sample output:
        
    VRNBCBJ0020A
                                                          Cost  Assessment     Total
    Class                                                                   
    Senior Engineer                                       0.00        0.00      0.00
    Senior Environmental Scientist Supervisor           129.80      259.80    389.60
    Senior Environmental Scientist Specialist             0.00        0.00      0.00
    Engineer                                            414.65      829.95  1,244.60
    Environmental Scientist                           3,504.60    7,014.70 10,519.30
    Water Resources Technician II                         0.00        0.00      0.00
    Total                                             4,049.05    8,104.45 12,153.50   
    
                  Cost  Assessment     Total
    Class                               
    DES       178.84    1,269.36  1,448.20
    DOE     2,914.73   20,688.05 23,602.78
    IRWM    1,953.00   13,861.92 15,814.92
    O&M       871.17    6,183.35  7,054.52
    Total   5,917.74   42,002.68 47,920.42
    
    """
    
    summaryPath = os.path.join(rootDir, 'summary.csv')
    
    df = pd.read_csv(summaryPath)
    
    #Get dictionary of Cost Elements from function.
    elementsMap = getElementsMap()
    
    #Create the new Class column with the dictionary.
    df['Class'] = df['Element'].map(elementsMap)
    
    #Drop Depreciation and OE&E.
    df = df.query('Class != "Depreciation" and Class != "OE&E"').reset_index(drop=True)

    #Create the Organization column and populate the name of the consultant for any contracts.
    df['Organization'] = df.loc[df.loc[:,'Class']=='Contract', 'Name'].apply(func=consultantCheck)
    
    #Drop OE&E from Organization.
    #Reset the index to avoid copy/slice warnings later.
    #Drop=True will prevent the index from being added as a column.
    df = df.query('Organization != "OE&E"').reset_index(drop=True)    
    
    #Get the dictionary of SMB employees and their job classifications from function.
    smbMap = getSMBmap()
   
    #For the Direct Labor or Labor Assessment rows of Class, split off the name of the Division
    #and further populate the Organization column.
    df.loc[((df['Class']=='Direct Labor')|(df['Class']=='Labor Assessment')),'Organization'] = \
    df.loc[((df['Class']=='Direct Labor')|(df['Class']=='Labor Assessment')),'Object'].apply(lambda x:x.split()[0]) 
     
    
    #If name of employee in Name is an SMB employee, set Organization equal to 'DES SMB.'
    df.loc[df['Name'].isin(smbMap.keys()), 'Organization'] = 'DES SMB'
    
  
    #If employee is not in the SMB, set their Organization equal to one specified in the first portion of Object.
    #This further writes over any generic DES entries in Organization, and includes all other Division.s
    df.loc[(df['Class']=='Direct Labor') & (~df['Name'].isin(smbMap.keys())), 'Organization'] = \
    df.loc[(df['Class']=='Direct Labor') & (~df['Name'].isin(smbMap.keys())), 'Object'].apply(lambda x:x.split()[0]) 

    #For SMB employees, this sets the Organization equal to DES SMB for Labor Assessments.
    df.loc[(df['Class']=='Labor Assessment') & 
           ((df['Object'].str.contains('DES Environmental PI'))|
            (df['Object'].str.contains('DES Suisun Marsh')) |
            (df['Object'].str.contains('DES REG Compl LS')) |
            (df['Object'].str.contains('DISE Quality MGMT LS')) |
            (df['Object'].str.contains('DISE Estuarine S&M')) |
            (df['Object'].str.contains('DISE Envir A&P LS')) |
            (df['Object'].str.contains('DISE ITP-Biop Imp LS')) |
            (df['Object'].str.contains('DISE DTS LS')) |
            (df['Object'].str.contains('DISE Envir Moni&Asse')) |
            (df['Object'].str.contains('DISE Envir A&P LS')) |
            (df['Object'].str.contains('DISE Collab Sci & In'))          
            ), 'Organization'] = 'DES SMB'


    #For all other non-SMB DES employees, this sets Organization equal to DES Other.
    #This writes over any generic DES entries in Organization.
    df.loc[df['Organization']=='DES', 'Organization'] = 'DES Other'
    
    #nan values throw errors in boolean filters, so replace them with an n/a string.
    df.fillna('n/a',inplace=True)

    #Add a column for the job classification for any SMB employee.
    df['SMB Class'] = df.loc[df['Organization']=='DES SMB', 'Name'].map(smbMap)

    #For Labor Assessments of SMB employees, set the rows of SMB Class equal to Assessment.
    df.loc[(df['Organization']=='DES SMB') & ((df['Class']=='Labor Assessment')), 'SMB Class'] = 'Assessment'
    
    #Create an smb df that groups by CO, Class, and SMB Class.  
    #This creates a multi-level index.
    smb = df.loc[(df['Organization']=='DES SMB') & ((df['Class']=='Labor Assessment')| \
          (df['Class']=='Direct Labor'))].groupby(by=['CO','Class','SMB Class']).sum()
            
    #Reset the index twice to get the new rows transposed to columns.
    smb.reset_index(level=1, inplace=True)
    smb.reset_index(level=1, inplace=True)

    #Create an Assessment dataframe, ast that only contains Costs associated with
    #Labor Assessments.  This will be joined back to smb to broadcast these
    #summarized values across the rows.
    ast = smb.loc[smb['Class']=='Labor Assessment', 'Cost'].copy()

    #Join ast back to to smb to broadcast these summarized values across the rows.
    smb = smb.join(ast,  lsuffix='', rsuffix='_Assessment')
    
    #Now that the assessment values are in a column, drop the assessment rows.
    smb = smb[smb['SMB Class'] != 'Assessment']

    #Create a summary Cost Table df.
    ct = smb['Cost'].groupby(by='CO').sum().to_frame()
    
    #Join ct back to smb to broadcast the cost totals across the rows.
    smb = smb.join(ct,  lsuffix='', rsuffix='_Total')
    
    #Calculate the Proportion of costs by SMB job class.
    smb['Proportion'] = smb['Cost'] / smb['Cost_Total']
    
    #Multiply the Proportion values times the total Assessment to 
    #get assessments by SMB job class.
    smb['Assessment'] = smb['Cost_Assessment'] * smb['Proportion']
    
    #Total up the Direct Labor and Labor Assessment costs.
    smb['Total'] = smb['Cost'] + smb['Assessment']
    
    #Get rid of the intermediate columns we no longer need.
    smb.drop(columns=['Class', 'Cost_Assessment',  'Cost_Total',  'Proportion'], inplace=True)
  
    #Group by CO and SMB Class to resumarize into a multiindex.
    smbgp = smb.groupby(by=['CO', 'SMB Class']).sum()

    #Use a Group By with a Pivot Table with marginal totals to find the total cost per
    #CO and SMB job classificatin.
    smbpt = smbgp.groupby(by=['CO']).apply(lambda sub_df: sub_df.pivot_table(index='SMB Class', \
          values=['Cost', 'Assessment', 'Total'], aggfunc=sum, margins=True, margins_name='Total'))
        
    #Reorder the columns since Assessment was showing up before Cost for some reason.
    smbpt = smbpt[['Cost', 'Assessment', 'Total']]
    
    breakdownPath = os.path.join(rootDir, 'Breakdown.csv')
    # breakdownPath = r'C:\Users\jgalef\OneDrive - California Department of Water Resources\Temp\Breakdown.csv'
    
    print('SMB Breakdown:')
    print(smbpt)
    
    smbpt.to_csv(breakdownPath, mode='w')
       
    smbgp = smb.groupby(by=['CO']).sum()

    gp = df.loc[(df['Class']!='Contract') & (df['Organization']!='DES SMB'), :]\
        .groupby(by=['CO', 'Class', 'Organization']).sum()
        
    pt = pd.pivot_table(gp, values='Cost', index=['CO', 'Organization'], columns='Class')
    
    pt['Total'] = pt['Direct Labor'] + pt['Labor Assessment']
    
    pt.dropna(inplace=True)
    
    file = open(breakdownPath, mode='a')   
    file.write('\n')
    file.write('\n')
    file.close()
    
    print('\nNon-SMB Breakdown:')
    print(pt)
     
    pt.to_csv(breakdownPath, mode='a')
    
    file = open(breakdownPath, mode='a')   
    file.write('\n')
    file.write('\n')
    file.close()      
    
    contracts = df.loc[df['Class']=='Contract',:].groupby(by=['CO', 'Organization']).sum()
    
    print('\nContracts Breakdown:')
    print(contracts)
    
    contracts.to_csv(breakdownPath, mode='a')
    

    

def COtable(path,printTable=False):
    """Create final summary table that includes just the labor costs for each 
    of the Cost Object numbers for that quarter.  Pass the argument 'printTable=True'
    for display output.  An 'output.csv' file will be created in the same directory
    as the input XLSX files.  The csv file is intended for easy copy and paste into final
    presentation xlsx file.
    
    Sample output:
        
                                                   VRNBCBJ0010A  VRNBCBJ0020A  VRNBCBJ0030A 
    Class                                                                                                                                      
    Senior Engineer                                        0.00      6,243.75      2,643.75 
    Senior Environmental Scientist Supervisor            129.80          0.00          0.00    
    Senior Environmental Scientist Specialist              0.00      9,710.40      3,189.20   
    Engineer                                             414.65      3,333.19      5,454.62   
    Environmental Scientist                            3,504.60      4,247.61     28,262.06       
    Water Resources Technician II                          0.00        281.95     14,992.85        
    
    """
    
    #Retrieve all xlsx files in the given directory path.
    files = listFiles(path)
    
    summaries = []
    
    #Calculate labor summaries for each of the CO number xlsx file.
    for file in files: 
        
        summaries.append(sap(file))
        
    #Concatenate all results into a 'final' dataframe.    
    final = pd.concat(summaries,axis=1)

    #Print output if requested.
    if printTable==True: print(final)
    
    #Export the 'final' dataframe to csv.
    final.to_csv(os.path.join(rootDir,'output.csv'))
    

def runSAPsummaries(path):
    """Get a printed display of summaries for all of the Cost Object xlsx file.
    
    Sample output:
        
    VNRFNRJ0050B
                                                   Cost  Assessment     Total
    Class                                                                    
    Senior Engineer                            2,587.50    5,232.74  7,820.24
    Senior Environmental Scientist Supervisor  4,737.70    9,581.12 14,318.82
    Senior Environmental Scientist Specialist      0.00        0.00      0.00
    Engineer                                   6,944.45   14,043.86 20,988.31
    Environmental Scientist                      194.70      393.74    588.44
    Water Resources Technician II                  0.00        0.00      0.00
    Total                                     14,464.35   29,251.46 43,715.81
    
    .
    .
    .
    
    VFFNHRN0050C
                                                   Cost  Assessment     Total
    Class                                                                    
    Senior Engineer                                0.00        0.00      0.00
    Senior Environmental Scientist Supervisor      0.00        0.00      0.00
    Senior Environmental Scientist Specialist      0.00        0.00      0.00
    Engineer                                   8,056.30   16,261.40 24,317.70
    Environmental Scientist                    7,111.14   14,353.63 21,464.77
    Water Resources Technician II                  0.00        0.00      0.00
    Total                                     15,167.44   30,615.03 45,782.47    
    
    """
        
    #Retrieve all xlsx files in the given directory path.
    files = listFiles(path)
    
    #Run summary script on each of the xlsx file.
    for file in files: sap(file,printSummary=True)

#**********************  Monthly Functions  ***************************************************    
    
def buildDF(rootDir):
    
    """For use with the monthly(rootDir) function.
    Processes the XLSXs first into one CSV that can be read by montly(rootDir).
    
    Reads all of the XLSX files in the given rootDir folder into dataframes,
    adds a column with the IO number, and concats them all into one dataframe,
    and exports to a CSV.  
    """

    #Get a list of XLSX files.
    files = listFiles(rootDir)
    
    dfs=[]
    
    #Define columns to be used.
    cols = ['Cost element name', 'Name', 'CO partner object name', 'Val.in rep.cur.']
    
    for file in files:
        #Split off the CO Number from the name of the file.
        coNumber = os.path.split(file)[1]
        coNumber = os.path.splitext(coNumber)[0]
        df = pd.read_excel(io=file,sheet_name='Sheet1',usecols=cols)
        #Add a column and populate with the CO number.
        df['CO'] = coNumber
        dfs.append(df)

    df = pd.concat(dfs)
    
    #Define the header for the export CSV.
    header=['Element','Name','Object','Cost','CO']
    
    df.to_csv(os.path.join(rootDir,'summary.csv'),index=False,header=header)
      

def monthly(rootDir):
    
    """Breaks down the monthly XLSXs for each IO and returns a summary of the costs
    first by IO, and then by Labor (Direct and Overhead), OE&E, and Consultants.   
    Download each XLSX to a folder, and supply the name of the folder as the 
    rootDir argument.
    
    To process the XLSXs first into one CSV, run buildDF(rootDir).
    
    Check the unique rows from the "Element" column, and make sure all are listed 
    below.
    
    Sample output for January 2021:
        
    VRNBCBJ0010A DES SMB    20,324.31
    VRNBCBJ0010B DES SMB       875.53
    VRNBCBJ0020A DES SMB     3,026.52
                 OE&E           65.55
    VRNBCBJ0030A DES SMB    34,584.69
                 OE&E          200.00
    VRNBCBJ003B1 DES SMB     2,237.70
    VRNBCBJ003B4 DES SMB     1,642.46
    VRNBCBJ003B6 DES SMB       450.44
    VRNBCBJ0050A DES SMB    17,519.16
    VRNBCBJ0050B DES SMB    21,757.13
    VRNBCBJ0050C DES SMB    12,411.85
    VRNBCBJ0050D DES SMB     5,389.77
    VRNBCBJFALL3 DOE         4,580.10
                 OE&E           84.00
    VRNBCBADMIN3 OE&E          184.15
    VRNBCBJTES03 DES SMB       931.74
    VRNBCBJIONS3 DES SMB     1,572.44
    VRNBCBNNING3 DOE         2,383.55
    VRNBCBJNAGE3 DES Other   6,264.32
                 DES SMB    47,434.33
    VRNBCBJGRIV3 DES SMB    10,768.94
    VRNBCBJNAGE3 DES SMB    35,963.29
                 SRCD      101,110.53
    
    """

    df = pd.read_csv(os.path.join(rootDir,'summary.csv'))
       
    #Exclude any rows for depreciation.
    df = df.loc[~df['Element'].str.contains('DepExpFull')]
    
    #Complete ist of IO numbers associated with the Compliance Fund Center.   
    #Update this each time we have new numbers.
    complianceIOs = ['VRNBCBJANAGE3',
                 'VRNBCBJ3NCE3',
                 'VRNBCBJIONS3',
                 'VRNBCBJGRIV3',
                 'VRNBCBYSTEM3',
                 'VRNBCBATES03',
                 'VRNBCBJFALL3',
                 'VRNBCBJRMIT3',
                 'VRNBCBJMITS3',
                 'VRNBCBJRPRT3',
                 'VRNBCBJOCK03',
                 'VRNBCBJNERS3',
                 'VRNBCBJDMIN3',
                 'VRNBCBJTRNG3',
                 'VRNBCBJCESS3',
                 'VRNBCBJCTS03',
                 'VRNBCBJ0010A',
                 'VRNBCBJ003B1',
                 'VRNBCBJ003B2',
                 'VRNBCBJ003B3',
                 'VRNBCBJ003B4',
                 'VRNBCBJ003B5',
                 'VRNBCBJ003B6',
                 'VRNBCBJ0050A',
                 'VVRNBCBJ050B',
                 'VRNBCBJ0050C',
                 'VVRNBCJ0050D']

    #Complete ist of IO numbers associated with the Planning Fund Center.   
    #Update this each time we have new numbers.    
    planningIOs =   ['VRNBCBJNING3',
                     'VRNBCBJNAGE3',
                     'VRNBCBJNING3',
                     'VRNBCBJ4010B',
                     'VRNBCBJ5020A',
                     'VRNBCBJ0030A']
    
    
  #Create dictionary that returns the fund center for each IO.
    
    #Start with the IOs associated with the Planning fund center.
    fundMap = dict(zip(planningIOs,['Planning 3860357850320']*len(planningIOs)))
    
    #Update with the IOs associated with the Compliance fund center.
    fundMap.update(dict(zip(complianceIOs,['Compliance 36783249000']*len(complianceIOs))))
          
    #Define the categories for Labor Assessments. 
    #Print out the unique elements of 'Element' and add any that aren't in this list.
    labors = """Direct Labor
    GM Labor Step 60
    GM Health Step 60
    GM SSA Step 60
    GM Work Comp Step 60
    GM Retirement Step 6
    GM Absence Step 60
    GM OE&E Step 60
    GM DEP WRRF Acq 60
    GM RENT Step 60
    LM Labor Step 60
    LM Health Step 60
    LM SSA Step 60
    LM Work Comp Step 60
    LM Retirement Step 6
    LM Absence Step 60
    LM OE&E Step 60
    LM RENT Step 60
    LS Labor Step 60
    LS Health Step 60
    LS SSA Step 60
    LS Work Comp Step 60
    LS Retirement Step 6
    LS Absence Step 60
    LS POE Step 60"""

    #Split the triple-quote string into a list.
    labors = labors.split('\n    ')
       
    #Create a dictionary that assigns 'Labor' type to elements in 'labors.'
    mapClasses = dict(zip(labors,['Labor']*len(labors)))
    
    #List all categories of OE&E.  
    #Print out the unique elements of 'Element' and add any that aren't in this list.
    oees = ['Construction Supplie','Training','Private Car Mileage','Lab Chem & Gases',
            'Environmental Srvcs','Shipping / Freight']
    
    #Create a dictionary that assigns 'OE&E' type to elements in 'OE&Es.'
    oeesType = ['OE&E'] * len(oees)    
    mapOees = dict(zip(oees,oeesType))
  
    #Add new 'OE&E' entry to classes dictionary.
    mapClasses.update(mapOees)
    
    #Add new 'Consultants' entry to classes dictionary.
    mapClasses['Consult&Pro Svcs-Ext'] = 'Consultants'
    mapClasses['Consult&Pro Svcs-Int'] = 'Consultants'
    mapClasses['Fed Co-op Contracts'] = 'Consultants'
    
    #Add new 'Real Estate' entry to classes dictionary.
    mapClasses['R/W & Related Costs'] = 'Real Estate'
    
    
       
    #Create new 'Class' column using mapClasses dictionary.
    df['Class'] = df['Element'].map(mapClasses)
        
    #Identify which classes are associated with the SMB.
    df.loc[(df['Class']=='Labor') & (df['Object'].str.contains('DES Environmental PI')), 'Type'] = 'DES SMB'   
    df.loc[(df['Class']=='Labor') & (df['Object'].str.contains('DES Suisun Marsh')), 'Type'] = 'DES SMB'    
    df.loc[(df['Class']=='Labor') & (df['Object'].str.contains('DES REG Compl')), 'Type'] = 'DES SMB'
    
    
    
    df.loc[(df['Class']=='Labor') & (df['Object'].str.contains('DES Budget & Prog')), 'Type'] = 'DES Other'
        
    df.loc[(df['Class']=='Labor') & (~df['Type'].str.contains('DES', na=False)), 'Type'] = \
    df.loc[(df['Class']=='Labor') & (~df['Type'].str.contains('DES', na=False)), 'Object'].apply(lambda x:x.split()[0])
    
    df.loc[(df['Class']=='Consultants'), 'Type'] = df.loc[df['Class']=='Consultants', 'Name'].apply(lambda x:x.split()[0])
    
    df.loc[df['Class']=='OE&E', 'Type'] = 'OE&E'   
    
    df.loc[df['Class']=='Real Estate', 'Type'] = 'Real Estate'  
    
    df['Fund'] = df['CO'].map(fundMap)
    
    
    
    currentCOs = set(df['CO'].unique())
    
    allCOs = set(planningIOs+complianceIOs)

    emptyCOs = list(allCOs - currentCOs)
    
    df2 = pd.DataFrame({'CO':emptyCOs, 'Cost':[0]*len(emptyCOs), 'Type':['n/a']*len(emptyCOs),
                        'Fund':[fundMap[CO] for CO in emptyCOs]})        
    
       
    df = pd.concat([df,df2],ignore_index=True)
    
    
    gp = df.groupby(by=['Fund','CO','Type'],dropna=False).sum()
    

    print(gp)                

    gp.to_csv(os.path.join(rootDir,'Breakdown.csv'))          
    



def makeMonthlyDirs(start,end):
    
    """Makes empty directories to store monthly data.   E.g. 
    '2021_-01'
    '2021_02'
    """
    
    root = r'Z:\Projects\Budget\Monthly'
    
    end = pd.Timestamp(end) + pd.DateOffset(months=1)
    
    dr = pd.date_range(start,end,freq='M')
    
    for per in dr:
        if not os.path.exists(os.path.join(root,f'{per:%Y_%m}')):
                              os.mkdir(os.path.join(root,f'{per:%Y_%m}'))



if __name__=="__main__":
    
    """Functions to process SAP labor and overhead data.  See each function's
    docstrings for more infomration.   Note that if any employee or job classes
    change in the SMB, the empClass dictionary and the SMBclasses list need to
    be changed in the 'sap' function.
    
    In general: 
        
    *Run 'COtable' to retrieve a summary table of all labor costs broken
    down by job classication for each of the Cost Object numbers changed for the 
    quarter.  
    
    *Run 'runSummaries' to retrieve labor and assessment costs broken
    down by job classication for each of the Cost Object numbers changed for the 
    quarter.
    
    *Run 'sap' for just one particular Cost Object xlsx file.
    """

    
    
    # SET THE ROOT DIRECTORY:
    rootDir = r'Z:\Projects\Budget\Quarterly\2021 Q3'

    
    # buildDF(rootDir)
    # monthly(rootDir)
    # monthlyNEW(rootDir)
    # exploreSummary(rootDir)
    # sapNew(rootDir)
    
    makeMonthlyDirs('2021-03','2021-9')
    
    # print(listFiles(rootDir))
    
    # sap('Z:\\Projects\\Budget\\2021 Q1\\VCVRNBCBJS03.xlsx',printSummary=True)
    
    # COtable(rootDir,printTable=True)
    
    # runSAPsummaries(rootDir)
    # exploreData(rootDir)
 