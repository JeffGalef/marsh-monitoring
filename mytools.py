# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 13:21:26 2019

@author: jgalef
"""


import pandas as pd
# import aiohttp
# import asyncio
# import nest_asyncio
# nest_asyncio.apply()




pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 50)
pd.options.display.expand_frame_repr = False
pd.set_option('precision',2)

class Station:
    
    """Create a Station object, complete with names, symbols, and type.  Use methods to get data.
    For instantiation, pass an integer representing the ISN.  E.g., for Collinsville, enter
    Station(2).  For Sunrise, enter Station(21)."""
    
    def __init__(self,number):
        
        self.cdec = getStationInfo(number,'cdec')
        self.isn = getStationInfo(number,'isn')
        self.portal = getStationInfo(number,'portal')        
        self.nickname = getStationInfo(number,'nickname')
        self.formal = getStationInfo(number,'formal')
        self.combo = getStationInfo(number,'combo')
        self.kind = getStationInfo(number,'kind')
        
    def get_PDM(self,start,end):
        
        return getPDMseries(self.portal,start,end,'PDM')
    
    def get_DM(self,start,end):
        
        return getPDMseries(self.portal,start,end,'DM')
    
    def get_stage(self,start,end):
        
        return getCDECseries(self.cdec,'1','E',start,end,ngvd29=False)
    

def getStationInfo(number,type):    
    
    d = getStationDict(type)
    
    return d[number]

def getStationDict(type):
    

    if type=='isn':        
        return {2:'C-2',
                21:'S-21',
                42:'S-42',
                49:'S-49',
                64:'S-64',
                35:'S-35',
                97:'S-97',
                71:'S-71'}

    elif type=='nickname':
        return {2:'Collinsville',
                21:'Sunrise',
                42:'Volanti',
                49:'Beldons',
                64:'National Steel',
                35:'Morrow Island',
                97:'Ibis',
                71:'Montezuma Slough'}

    elif type=='portal':
        return  {2:'2',
                21:'21',
                42:'42',
                49:'49',
                64:'64',
                35:'35',
                97:'97',
                71:'71'}
  
    elif type=='formal':
        return  {2:'Sacramento River at Collinsville',
                21:'Chadborne Slough at Sunrise Club',
                42:'Suisun Slough 300 feet south of Volanti Slough',
                49:'Montezuma Slough near Beldons Landing',
                64:'Montezuma Slough at National Steel',
                35:'Goodyear Slough at Morrow Island',
                97:'Cordelia Slough at Ibis',
                71:'Montezuma Slough at Roaring River Distribution System'}  

    elif type=='combo':
        return  {2:'C-2 Collinsville',
                21:'S-21 Sunrise',
                42:'S-42 Volanti',
                49:'S-49 Beldons',
                64:'S-64 National Steel',
                35:'S-35 Morrow Island',
                97:'S-97 Ibis',
                71:'S-71 Montezuma Slough'}     
    
    elif type=='cdec':
        return  {2:'CSE',
                21:'SNC',
                42:'VOL',
                49:'BDL',
                64:'NSL',
                35:'GYS',
                97:'IBS',
                71:'MSL'}
    
    elif type=='kind':
        return  {2:'Eastern Compliance',
                21:'Western Compliance',
                42:'Western Compliance',
                49:'Eastern Compliance',
                64:'Eastern Compliance',
                35:'Control',
                97:'Control',
                71:'Monitoring'}   



def getWaterYearType():
    """Returns a dictionary of Water Years and Types for the Sacramento Basin.
    E.g., passing '2009-2010' will return 'Below Normal'.  """

    waterYears = ["2009-2010","2010-2011","2011-2012","2012-2013","2013-2014","2014-2015","2015-2016","2016-2017","2017-2018","2018-2019","2019-2020"]
    types = ["Below Normal","Wet","Below Normal","Dry","Critical","Critical","Below Normal","Wet","Below Normal","Wet","Dry"]

    return(dict(zip(waterYears,types)))
    
    

def getStandards():
    """Returns a dictionary of the monthly salinity standards."""
       
    from numpy import nan
    standards = {1:12.5, 2:8.0, 3:8, 4:11.0, 5:11.0, 6:nan, 7:nan, 8:nan, 9:nan, 10:19.0, 11:15.5, 12:15.5}  
    
    return standards


def getStandardsDetailed():
    """Returns 3 dictionaries showing normal standards for the Easter Marsh, for the Western Marsh, and for the Western
    Marsh when in a Deficiency Period."""
    
    from numpy import nan    

    #Create dictionaries for the eastern stations, and for the western stations under normal and deficiency periods.
    standardsEastern           = {10:19.0, 11:15.5, 12:15.5, 1:12.5, 2:8.0,  3:8.0,  4:11.0, 5:11.0, 6:nan, 7:nan, 8:nan, 9:nan}    
    normalStandardsWestern     = {10:19.0, 11:16.5, 12:15.5, 1:12.5, 2:8.0,  3:8.0,  4:11.0, 5:11.0, 6:nan, 7:nan, 8:nan, 9:nan}    
    deficiencyStandardsWestern = {10:19.0, 11:16.5, 12:15.6, 1:15.6, 2:15.6, 3:15.6, 4:14.0, 5:12.5, 6:nan, 7:nan, 8:nan, 9:nan}
    
    return standardsEastern, normalStandardsWestern, deficiencyStandardsWestern


def getDRFtriggers():
    """Returns a dictionary of Drought Response Fund trigger values."""
    
    from numpy import nan
    
    triggers = {10:20.0, 11:nan, 12:nan, 1:nan, 2:9.0,  3:9.0,  4:12.0, 5:12.0, 6:nan, 7:nan, 8:nan, 9:nan}   
    
    return triggers



def getStations(type):
    """Returns a list of the 5 compliance stations, and the 2 control stations."""
    
    if type=='ISN':
        stations = ['C-2','S-21','S-42','S-49','S-64','S-35','S-97']
    
    elif type=='nicknames':
        stations = ['Collinsville','Sunrise','Volanti','Beldons','National Steel','Morrow Island',
                    'Ibis']
    
    elif type=='portal':
        stations = ['2','21','42','49','64','35','97']
    
    elif type=='formal':
        stations = ['Sacramento River at Collinsville','Chadborne Slough at Sunrise Club',
                    'Suisun Slough 300 feet south of Volanti Slough','Montezuma Slough near Beldons Landing',
                    'Montezuma Slough at National Steel','Goodyear Slough at Morrow Island',
                    'Cordelia Slough at Ibis']   
    elif type=='combo':
        stations = ['C-2 Collinsville','S-21 Sunrise','S-42 Volanti','S-49 Beldons','S-64 National Steel',
                    'S-35 Morrow Island','S-97 Ibis']
    elif type=='CDEC':
        stations = ['CSE','SNC','VOL','BDL','NSL','GYS','IBS']
    return stations

     
        
def getPDM(station, date, meanType):
    """Gets a Pandas series for a station for the entire month of a given date.  
    Enter meanType='DM' or meanType='PDM'.  Date can be a string.
    Sample function call: getPDM('21','2019-3-14','PDM')."""
        
    date = pd.Timestamp(date) 
    
    try:
        dfG = pd.read_csv(r'PRIVATE API URL' \
        .format(station, str(date.year), str(date.month)),na_values=0.00,parse_dates=['StartDateTime'],index_col='StartDateTime')
                       
    except:
        raise RuntimeError("Webservice down")    
        
    if pd.isnull(dfG['DailyMean']).any():

        try:
            dfU= pd.read_csv(r'PRIVATE API URL' \
            .format(station, str(date.year), str(date.month)),na_values=0.00,parse_dates=['StartDateTime'],index_col='StartDateTime')
        except:
            raise RuntimeError("Webservice down")    
    
        dfPDM = dfG.combine_first(dfU)
        
    else:
        
        dfPDM = dfG

    dfPDM.rename(columns={'DailyMean':'Daily Mean'},inplace=True)
           
    if meanType=='DM':
        dfPDM['Daily Mean'] = dfPDM['Daily Mean']/1000.0
        return dfPDM['Daily Mean']
    
    if meanType=='PDM':
        dfPDM['Progressive Daily Mean'] = dfPDM['Progressive Daily Mean']/1000.0
        return dfPDM['Progressive Daily Mean']
    
    if meanType=='both':
        dfPDM['Daily Mean'] = dfPDM['Daily Mean']/1000.0
        dfPDM['Progressive Daily Mean'] = dfPDM['Progressive Daily Mean']/1000.0
        return dfPDM[['Daily Mean','Progressive Daily Mean']] 
    
    

def getPDMseries(station, startDate, endDate, meanType):
    """Returns a series of DM's or PDM's for a station for a given date range.    
    Enter meanType='DM' or meanType='PDM'.Dates must be date objects.
    Sample function call: getPDMseries('21',dt.date(2019,3,14),dt.date(2019,8,27),'PDM')."""
    
    pr = pd.period_range(startDate, endDate, freq='M')
    
    dfs=[]

    for period in pr: 
        
        period = period.to_timestamp(freq='D') 
        dfs.append(getPDM(station, period, meanType))
        
    df = pd.concat(dfs)
    
    df = df[startDate:endDate]
    
    return df



def getPDMs7(startDate, endDate, meanType, mean=False, standards=False, detailedStandards=False, minimum=False, maximum=False, random=False, DRFtriggers=False):
    """Returns a dataframe of PDM or DM values for the 5 compliance stations, and 2 control stations.
    Set random==False if real data aren't needed - say for development purposes.  This only works for meanType='DM' or 'PDM'; it does not work for 'both.'
    """
    stations = ['2','21','42','49','64','35','97']
    
    if random==True:
        import numpy as np
        dr = pd.date_range(start=startDate, end=endDate, freq='1 D')
        df = pd.DataFrame(index=dr,data=np.random.rand(len(dr),7),columns=getStations('ISN'))


    else:    
        dfs=[]       
        cols = getStations('ISN')
        for (station,col) in zip(stations,cols):
            df = getPDMseries(station, startDate, endDate, meanType)
            # df = df.rename(col)
            dfs.append(df)
        # print(dfs)
        df = pd.concat(dfs,axis=1)     
        
    if (meanType=='DM' or meanType=='PDM'):
        df.columns=['C-2','S-21','S-42','S-49','S-64','S-35','S-97']
        if (mean==True): df['Mean'] = df.mean(axis=1,skipna=True)
        if (minimum==True): df['Minimum'] = df.min(axis=1,skipna=True)
        if (maximum==True): df['Maximum'] = df.max(axis=1,skipna=True)
        
    elif (meanType=='both'):
        df.columns=['C-2 DM','C-2 PDM','S-21 DM','S-21 PDM','S-42 DM','S-42 PDM','S-49 DM','S-49 PDM',
                    'S-64 DM','S-64 PDM','S-35 DM','S-35 PDM','S-97 DM', 'S-97 PDM']           
        if (mean==True): 
            df['DM Mean'] = df[['C-2 DM','S-21 DM','S-42 DM','S-49 DM','S-64 DM','S-35 DM','S-97 DM']].mean(axis=1,skipna=True)
            df['PDM Mean'] = df[['C-2 PDM','S-21 PDM','S-42 PDM','S-49 PDM','S-64 PDM','S-35 PDM','S-97 PDM']].mean(axis=1,skipna=True)
        if (minimum==True):
            df['DM Minimum'] = df[['C-2 DM','S-21 DM','S-42 DM','S-49 DM','S-64 DM','S-35 DM','S-97 DM']].min(axis=1,skipna=True)
            df['PDM Minimum'] = df[['C-2 PDM','S-21 PDM','S-42 PDM','S-49 PDM','S-64 PDM','S-35 PDM','S-97 PDM']].min(axis=1,skipna=True)
        if (maximum==True):
            df['DM Maximum'] = df[['C-2 DM','S-21 DM','S-42 DM','S-49 DM','S-64 DM','S-35 DM','S-97 DM']].max(axis=1,skipna=True)
            df['PDM Maximum'] = df[['C-2 PDM','S-21 PDM','S-42 PDM','S-49 PDM','S-64 PDM','S-35 PDM','S-97 PDM']].max(axis=1,skipna=True)            
            
    df.index = pd.to_datetime(df.index)
    

    if (standards==True): 
        standards = getStandards()
        df['Standard'] = [standards[x] for x in df.index.month]


    if (detailedStandards==True):
        standardsEastern, normalStandardsWestern, deficiencyStandardsWestern = getStandardsDetailed()
        df['Eastern Standards'] = df.index.month.map(standardsEastern)
        df['Western Standards'] = df.index.month.map(normalStandardsWestern)
        df['Western Deficiency Standards'] = df.index.month.map(deficiencyStandardsWestern)
        
    if (DRFtriggers==True):
        DRFtriggers = getDRFtriggers()
        df['DRF Triggers'] = df.index.month.map(DRFtriggers)
        
    return df        


def getPDMvalue(station, date, meanType):
    """Returns the Daily Mean or Progressive Daily Mean for a station on the 
    specified date.  Enter mean Type='DM' or meanType='PDM'.  Return type is float.
    Sample function call: getPDMvalue('21','2020-10-15','PDM')."""
    
    dfPDM = getPDM(station, date, meanType)
           
    return dfPDM.loc[date]





def getCDECseries(symbol, sensor, duration, start, end, ngvd29=False, get_url=False):
    """Returns a Pandas series of data from CDEC.  Enter symbol as CDEC code, sensor as the sensor number, 
    duration at E, H, D, etc., and start and end dates as strings.
    Sample function call: getCDECseries('RUM','41','D','2019-1-1','2019-4-15').
    Sample URL: http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=nsl&SensorNums=21&dur_code=E&Start=2018-10-27&End=2019-10-28"""
      
    start = pd.to_datetime(start)
    
    end = pd.to_datetime(end) + pd.Timedelta(days=1)  
                          
    url = r'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations={}&SensorNums={}&dur_code={}&Start={:%Y-%m-%d}&End={:%Y-%m-%d}'.\
                      format(symbol,sensor,duration,start,end)                     
                                                     
   
    try:   
        df = pd.read_csv(url,na_values='---',parse_dates=['DATE TIME'],index_col='DATE TIME')
    except RuntimeError:
        print(f'Webservice down for {symbol}')
        print(f'URL: {url}')

    
    df = df['VALUE']
 

    if duration=='E':
        end = end - pd.Timedelta(minutes=15)
    elif duration=='D':
        end = end - pd.Timedelta(days=1)
    elif duration == 'H':
        end = end - pd.Timedelta(hours=1)
    
    df = df[start:end]
              
    if ngvd29==True: df = df - 2.488
    
    df.name = symbol
        
    if get_url==True: print(url)
        
    return df



def getCDECdf(stations):

    sList = []
    
    for station in stations:
        
        if len(station) > 5:
            sList.append(getCDECseries(symbol=station[0], sensor=station[1], duration=station[2], start=station[3], end=station[4], ngvd29=station[5]))
        else:
           sList.append(getCDECseries(symbol=station[0], sensor=station[1], duration=station[2], start=station[3], end=station[4]))
           
    df = pd.concat(sList,axis=1)
    
    return df



        
        

def getWonderwareData(path=r'data.csv'):
    """Returns a dataframe of the 8 gate openings, the velocities at the fish screens, the head
    differential between MSL and the fish screen pond, and the average opening for the 8 gates 
    for the RRDS."""
    
    #Make a list of column names. 
    cols =  ['StageDiff'] + ['Velocity'] + ['Gate'+str(i) for i in range(1,9)]   
    
    cols2 = ['RRDS_HEADDIFF.LEVEL_USG',
       'RRDS_FS.VELOCITY_FPS',
       'RRDS_GATE01.POS_FT',
       'RRDS_GATE02.POS_FT',
       'RRDS_GATE03.POS_FT',
       'RRDS_GATE04.POS_FT',
       'RRDS_GATE05.POS_FT',
       'RRDS_GATE06.POS_FT',
       'RRDS_GATE07.POS_FT',
       'RRDS_GATE08.POS_FT']
    
    cols = dict(zip(cols2,cols))    

    #Read the csv, set the index column, parse the dates, specify the header row from the file,
    #and replace it with new column names.
    df = pd.read_csv(path, index_col='DateTime', parse_dates=['DateTime'], na_values='(null)')
    
    df = df.rename(columns=cols)
        
    df['GatesMean'] = df[['Gate'+str(i) for i in range(1,9)]].mean(axis=1)
    
    return df



def get_tidePredictions(station,start,end):
    """Rereive tidal predictions from NOAA."""

          
    #Station map:https://tidesandcurrents.noaa.gov/map/index.html
    
    #Marsh stations: Bradmoor:9414811, Mallard:9415112, Port Chicago:9415144, Martinez:9415102, 
    #Suisun Slough Entrance (near Godfather):9415265, Point Buckler (in Grizzly Bay):9415227, 
    #Montezuma Slough Bridge (near Beldon's):9415402, #Meins Landing:9415307, 
    #Montezuma Slough (near RRDS):9415205, Collinsville:9415176

    #Datums: MLLW, NAVD     

    codesDict={
        'Bradmoor':'9414811',
        'Mallard':'9415112', 
        'Port Chicago':'9415144',
        'Martinez':'9415102', 
        'Suisun Slough Entrance':'9415265', 
        'Point Buckler':'9415227', 
        'Montezuma Slough Bridge':'9415402',
        'Meins Landing':'9415307', 
        'Montezuma Slough':'9415205', 
        'Collinsville':'9415176',
        'San Francisco':'9414290'
        }
 
    datumsDict={}
    intervalsDict={}
    for key in codesDict.keys():
        if (key=='Port Chicago') or (key=='San Francisco'):
            datumsDict[key]='NAVD'
            intervalsDict[key]='h'
        else:
            datumsDict[key]='MLLW'
            intervalsDict[key]='hilo'
    

    start,end = pd.to_datetime(start), pd.to_datetime(end)
    

    #URL for hi-lo values.
    # url = 'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='\
    # f'{start:%Y%m%d}&end_date={end:%Y%m%d}&datum=MLLW&station=9415307&time_zone=lst_ldt&units=english&interval=hilo&format=csv'

    #URL for hourly values.
    # url = 'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='\
    # f'{start:%Y%m%d}&end_date={end:%Y%m%d}&datum=MLLW&station=9415307&time_zone=lst_ldt&units=english&interval=hilo&format=csv'                        

    #URL for hi-lo values with hours and minutes.
    # url = 'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='\
    # f'{start:%Y%m%d%%20%H:%M}&end_date={end:%Y%m%d%%20%H:%M}&datum=MLLW&station=9415307&time_zone=lst_ldt&units=english&interval=hilo&format=csv'

    url = 'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='\
    f'{start:%Y%m%d%%20%H:%M}&end_date={end:%Y%m%d%%20%H:%M}&datum={datumsDict[station]}&station={codesDict[station]}&'\
    f'time_zone=lst_ldt&units=english&interval={intervalsDict[station]}&format=csv'

    # print(url)

    df = pd.read_csv(url,parse_dates=['Date Time'],index_col='Date Time')
    
    df.rename(columns={' Prediction':'Prediction'},inplace=True)
    
    return df
    
    

                     
                     
#https://waterdata.usgs.gov/nwis/dv?cb_0060=on&format=rdb&site_no=11303500&referred_module=sw&period=&begin_date=2019-07-01&end_date=2019-08-31
#https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=11303500&referred_module=sw&period=&begin_date=2017-10-01&end_date=2018-09-30


def getUSGS(siteNumber, parameter, start, end, displayURL=False):
    
    
    start, end = pd.to_datetime(start), pd.to_datetime(end)
    
    #sample URL: https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=11453000&referred_module=sw&period=&begin_date=2017-10-01&end_date=2018-09-30

    #This URL is out of date.
    # url = 'https://waterdata.usgs.gov/nwis/dv?cb_{}=on&format=rdb&site_no={}&referred_module=' \
    # 'sw&period=&begin_date={:%Y-%m-%d}&end_date={:%Y-%m-%d}'.format(parameter,siteNumber,start,end)
    
    url = f'https://nwis.waterdata.usgs.gov/nwis/dv?cb_00010=on&format=rdb&site_no={siteNumber}&referred_module=sw&period=&begin_date={start:%Y-%m-%d}&end_date={end:%Y-%m-%d}'


    if displayURL==True: print(url)

    df = pd.read_csv(url,comment='#',sep='\t',header=1,names=['USGS','site_no','Date','CFS','Flag'],
                     usecols=['Date','CFS','Flag'],parse_dates=['Date'],index_col='Date')
    
    df['CFS'] = df['CFS'].apply(lambda x:float(x))
    
    return(df)


def getCIMIS(start,end):
    
    """Returns a series of daily precipitation values for the Concord station.   Can be modified in the future to change location,
    frequency, and parameter types.   Simply enter a start and end date."""
    
    import requests
    
    start,end = pd.to_datetime(start), pd.to_datetime(end)
    
    #A key is required to retrieve data.   Create an account, click on "Account", click on "Get AppKey" and save.
    key = 'Private API key'
      
    url = 'Private API URL'
    
    payload = {'Private payload'}
    
    try:
        #Use the Request library to add a header specifying a return of JSON instead of the default XML.
        r = requests.get(url,params=payload,headers={'Accept':'application/json'})
    except:
        print(r.url)
       


    #The retrieved JSON dictionary is verbose, so parsing is requried.
    records = r.json()['Data']['Providers'][0]['Records']

    # print(records)    
    
    dates = [pd.to_datetime(record['Date']) for record in records]
    
    print(dates)

    precips = [float(record['DayPrecip']['Value']) for record in records]

   
    serP = pd.Series(data=precips,index=dates,name='Precip_inches')
    
    return serP



def getLunarPhases(start,end):
    
    import ephem
    
    #Set location at Port Chicago station.
    gatech = ephem.Observer()
    gatech.lon = -121.999971
    gatech.lat =  38.056788  

    #Birds Landing coordinates
    # gatech.lon = -121.869686
    # gatech.lat =  38.132772

    #Convert possible strings to Timestamps.
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
      
    dateFM=start
    dateNM=start
    dateFQ=start
    dateLQ=start
    endTemp=start
    phases=[]
    while endTemp <= end:
        next_full_moon = ephem.localtime(ephem.next_full_moon(dateFM))
        phases.append((next_full_moon,'full moon'))
        dateFM = next_full_moon + pd.DateOffset(days=1)
        
        next_new_moon = ephem.localtime(ephem.next_new_moon(dateNM))
        phases.append((next_new_moon,'new moon'))
        dateNM = next_new_moon + pd.DateOffset(days=1)
        
        next_first_quarter_moon = ephem.localtime(ephem.next_first_quarter_moon(dateFQ))
        phases.append((next_first_quarter_moon,'first quarter'))
        dateFQ = next_first_quarter_moon + pd.DateOffset(days=1)              
    
        next_last_quarter_moon = ephem.localtime(ephem.next_last_quarter_moon(dateLQ))
        phases.append((next_last_quarter_moon,'last quarter'))
        dateLQ = next_last_quarter_moon + pd.DateOffset(days=1)      
    
        phases.sort()
        endTemp = phases[-1][0]
        
    dates = [tup[0] for tup in phases]
    phases = [tup[1] for tup in phases]
  
    phases = pd.DataFrame(index=dates,data=phases,columns=['Phase'])  
    
        
    return phases[start:end]
        
def get_PortChicago(start,end,product):
    
    """Retrieves Port Chicago data from NOAA.  For a list of available products, see here:
        Enter 'stage' or 'met'"""
    
    
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    

    dr2=pd.date_range(start,start,periods=1)
    dr = pd.date_range(start,end,freq='MS')
    dr=dr.union(dr2)

    dfs=[]
    
    for date in dr:
        
        eom = date+pd.offsets.MonthEnd()
        
        if product=='stage':
    
            url = f'https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application='\
                f'NOS.COOPS.TAC.WL&begin_date={date:%Y%m%d}&end_date={eom:%Y%m%d}&datum=NAVD&'\
                    'station=9415144&time_zone=lst_ldt&units=english&format=csv'
                                        
            df = pd.read_csv(url,parse_dates=['Date Time'],index_col='Date Time', usecols=['Date Time',' Water Level'])
                         
        elif product=='met':
            
            url = 'https://tidesandcurrents.noaa.gov/cgi-bin/newdata.cgi?type=met&id=9415144&'\
                f'begin={date:%Y%m%d}&end={eom:%Y%m%d}&units=standard&timezone=LST/LDT&mode=csv&interval=h'

            df = pd.read_csv(url,parse_dates=['DATE TIME'],index_col='DATE TIME').iloc[:,:-2]           

        # print(url)    
        
        dfs.append(df)
                
    df = pd.concat(dfs)
    df = df[start:end]
    
    if product=='stage':
        df.rename(columns={' Water Level':'Stage'},inplace=True)
    
    

    
    return df


def get_gateOps(start,end):
    
    path=r'SMSCG Log.xlsx'

    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
        
    df = pd.read_excel(path,sheet_name='Sheet1',parse_dates=['DATETIME'],index_col='DATETIME')
    
    df.sort_index(inplace=True)    
    
    df = df[(df['ACTION']=='Tidal Operations')|(df['ACTION']=='Open Position')]
    
    dfToday = df.tail(1)
    
    dfToday.index=[pd.Timestamp.today()]
    
    df = df.append(dfToday)
        
    df = df.asfreq('T').fillna(method='pad')
    
    df['Mode']=1
        
    df.loc[(df['GATE 1']=='Tidal')|(df['GATE 2']=='Tidal')|(df['GATE 3']=='Tidal'),'Mode'] = 1
    
    df.loc[(df['GATE 1']=='Open')|(df['GATE 2']=='Open')|(df['GATE 3']=='Open'),'Mode'] = 0
    
    df = df.loc[start:end,'Mode']
           
    return df



def predictedTidesChart(datum,outFile=None,start=pd.Timestamp.now()-pd.DateOffset(days=7),
                        end=pd.Timestamp.now()+pd.DateOffset(days=7)):
    
    """Produces a chart of observed and predicted tides at Port Chicago.   The 
    default is for 7 days of observed stages, and 7 days of forecasted stages,
    but the user may input custom start and end dates.   The user may also choose
    between the 'NGVD 29' and 'NAVD 88' datums.   Simply enter '29' or '88' (as integers), 
    respectively.  The user has the option to include a file path for the 
    PDF.  If no outFile argument is provided, no output file will be created.
    
    """
    
    import matplotlib.pyplot as plt  

    
    pc = get_tidePredictions('Port Chicago',start,end)
    
    
    if datum==29:  pc['Prediction'] = pc['Prediction']-2.49

    
    fig,ax = plt.subplots(figsize=(12,8))
    
    
    ax.plot(pc.loc[start:pd.Timestamp.now()+pd.DateOffset(hours=1),'Prediction'],
            ls='-',color='steelblue',label='observed')
    
    ax.plot(pc.loc[pd.Timestamp.now():,'Prediction'],color='steelblue',ls='--',label='predicted')
    
    
    ax.set_title('Observed and Predicted Tides at Port Chicago',size='large',pad=10)
    
    if datum==29:
        
        ax.set_ylabel('Stage (feet, NGVD 29)', size='larger',labelpad=2)
        
    elif datum==88:
        
        ax.set_ylabel('Stage (feet, NAVD 88)', size='larger',labelpad=10)
    
    ax.legend()
    
    if not outFile==None:
        
        fig.savefig(outFile)   
        
        
def predictedTidesChart_nDays(datum,outFile=None,start=pd.Timestamp.now(),
                        n=30):
    
    """Produces a chart of predicted tides at Port Chicago for the next n days.   The 
    default is for 30 days, but the user may input custom start and end dates.   
    The user may also choose between the 'NGVD 29' and 'NAVD 88' datums.   
    Simply enter '29' or '88' (as integers), respectively.  The user has the 
    option to include a file path for the PDF.  If no outFile argument is provided, 
    no output file will be created.
    
    """
    
    import matplotlib.pyplot as plt  
    import matplotlib.dates as mdates
    
    end = start + pd.DateOffset(days=n)

    
    pc = get_tidePredictions('Port Chicago',start,end)
    
    
    if datum==29:  pc['Prediction'] = pc['Prediction']-2.49

    
    fig,ax = plt.subplots(figsize=(12,8))
    
    ax.plot(pc.loc[pd.Timestamp.now():,'Prediction'],color='steelblue',label='predicted')
    
    
    ax.set_title(f'Predicted Tides at Port Chicago for the next {n} days',size='large',pad=10)
    
    if datum==29:
        
        ax.set_ylabel('Stage (feet, NGVD 29)', size='larger',labelpad=2)
        
    elif datum==88:
        
        ax.set_ylabel('Stage (feet, NAVD 88)', size='larger',labelpad=10)
    
    ax.grid(axis='both', alpha=.5)
    
    # weeks = mdates.WeekdayLocator(byweekday=1, interval=7)
    
    weeks = mdates.DayLocator(interval=7)
        
    ax.xaxis.set_major_locator(weeks)
    
    ax.axvline((start+pd.offsets.MonthBegin()).normalize(), color='darkgrey', ls='--')
    
    
    
    if not outFile==None:
        
        fig.savefig(outFile)           
        
        
        
        

def adf_test(series,title=''):
    
    """Runs the Augmented Dicky-Fuller Test.  Pass in a time series and optional title, 
    and generate an ADF report."""
    
    from statsmodels.tsa.stattools import adfuller
    
    print(f'Augmented Dickey-Fuller Test: {title}')
    
    #Get tuple of results from df test.
    #The dropna() gets rid of NaNs from differenced data.
    result = adfuller(series.dropna(),autolag='AIC')
    
    #Create a new series that begins by holding the first 4 values, and assign an index of parameter returned.
    out = pd.Series(result[:4],index=['ADF Test Statistic','p-value','# Lags Used','# Observations'])
    
    #The fourth entry in the output is a dictionary of critical values.  
    #Append these values along with their index identifiers to the 'out' series.
    for key,val in result[4].items():
        out[f'Critical value ({key})'] = val
    
    #Print the output.  The to_string() removes the dtype information.
    print(out.to_string())
    
    print('Null hypothesis: the time-series is non-stationary.')
    
    #Evaluate the p-value, which from Investopedia is defined as the probability of obtaining results at least as 
    #extreme as the observed results of a statistical hypothesis test, assuming that the null hypothesis is correct.
    #The null hypothesis stated that the data are non-stationary.
    if result[1] <= 0.05:
        print('Strong evidence against the null hypothesis.')
        print('Reject the null hypothesis.')
        print('Data have no unit root and are STAIONARY.')
    else:
        print('Weak evidence against the null hypothesis.')
        print('Fail to reject the null hypothesis.')
        print('Data have a unit root and are NON-STATIONARY.')   


def getWYdict(start,end):
    
    wys = range(start,end+1)
    
    labels=[]
    for wy in wys:
            labels.append(f'{wy-1}-{str(wy)[2:]}')
    labels=dict(zip(wys,labels))
    
    return(labels)



def getPDMseriesAsync(station,start,end,meanType,flag='*'):
    
    """Like getPDM(), but uses asyncio to greatly speed up the process."""
    
    from io import StringIO
    import asyncio
      
    periods = pd.period_range(start,end,freq='M')
    
    responses = asyncio.run(fetch_all(station,periods,flag))
    
    cols = ['StartDateTime','DailyMean','Progressive Daily Mean']
    
    dfs = []
       
    for response in responses:
        
        io = StringIO(response)
        
        df = pd.read_csv(io,na_values=0.00,parse_dates=['StartDateTime'],index_col='StartDateTime',usecols=cols)
        
        dfs.append(df)
               
    df = pd.concat(dfs)
    
    df = df.loc[start:end]    
           
    df = df/1000
  
    df.rename(columns={'DailyMean':'Daily Mean'},inplace=True)
       
    if meanType=='DM':
        
        return df.loc[:,'Daily Mean']
    
    if meanType=='PDM':
    
        return df.loc[:,'Progressive Daily Mean']

    
    if meanType=='both':
        
        return df

async def fetch(session, url):
    """Execute an http call async
    Args:
        session: contexte for making the http call
        url: URL to call
    Return:
        responses: A text response from the API.
    """
    async with session.get(url) as response:
        resp = await response.text()
        return resp

async def fetch_all(urls):
    """ Gather many HTTP call made asynchronously
    Args:
        urls: a python list of URLs
    Return:
        responses: A list of text responses.
    """
    import aiohttp, asyncio
    
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session,url))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses
    

def getPortalData(start,end):
       
    """Returns a dataframe of stage and operational data.  Only is called
    when data are to be retrieved from data portal.  This function does NOT use asycio, since
    it causes Spyder to lock up.  Discontinue use if Spyder fixes the issue."""
    
    #Cannot share due to agency security policy.
    
    
    return df    




if __name__ == "__main__":
    
    
    start='2020-10-1'
    # end='2020-10-31'   
    end='2020-10-3'     
    
    # predictedTidesChart_nDays(88)
    

    
    
