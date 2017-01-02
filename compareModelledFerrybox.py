import time, calendar
from datetime import datetime,timedelta
from netCDF4 import Dataset
import numpy as np
import os
import pandas as pd
import string
from subprocess import call
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

__author__ = 'Trond Kristiansen'
__email__ = 'trond.kristiansen@niva.no'
__created__ = datetime(2016, 12, 19)
__modified__ = datetime(2016, 12, 19)
__version__ = "1.0"
__status__ = "Development"


"""
After running extractFerryDataForStation.py  - run the following commands to removed difficult characters

sed 's/"//g' station_ST20925_ferrybox.csv > station_ST20925_ferrybox_edited.csv
sed 's/"//g' station_ST935_ferrybox.csv > station_ST935_ferrybox_edited.csv
sed 's/"//g' station_ST939_ferrybox.csv > station_ST939_ferrybox_edited.csv
sed 's/"//g' station_ST1007_ferrybox.csv > station_ST1007_ferrybox_edited.csv
sed 's/"//g' station_ST6700053_ferrybox.csv > station_ST6700053_ferrybox_edited.csv
sed 's/"//g' station_STN3_ferrybox.csv > station_STN3_ferrybox_edited.csv
sed 's/"//g' station_ST20925_ferrybox.csv > station_ST20925_ferrybox_edited.csv
"""

def getFerryData(ferryfilename):
	print "=> Running function getFerryData"

	df = pd.read_csv(ferryfilename)
	
	vals=df.columns.tolist()
	df['Time'] = df['Time'].astype('datetime64[ns]')
	df2=df.set_index(df['Time'])
	df3 = df2[df2['Flu'] < 100]
	df4 = df3[df3['Flu'] > 0]

	print "Dataframe includes:"
	for val in vals:
		s=string.split(val)
		print "=> station: %s"%(s)
	print "Data stored in dataframe"
	print "Data ranging in time from %s to %s\n"%(df4.index[0],df4.index[-1])
	return df4,vals

def getModelledData(modelfilename):
	print "=> Running function getModelledData"

	xls_file = pd.ExcelFile(modelfilename)
	df = xls_file.parse('Sheet1')

	vals=df.columns.tolist()
	df['time'] = df['time'].astype('datetime64[ns]')
	df2=df.set_index(df['time'])

	print "Dataframe includes:"
	for val in vals:
		s=string.split(val)
		print "=> station: %s"%(s)
	print "Data stored in dataframe"
	print "Data ranging in time from %s to %s\n"%(df2.index[0],df2.index[-1])
	return df2,vals,df2.index[0],df2.index[-1]

def interpolateTime(dfmodel,dfferry,headerModel,headerFerry,compareIndex,startTime,endTime,plotfilename):
	# http://stackoverflow.com/questions/25322933/pandas-timeseries-comparison
	# 1. Interpolate the two time series so that they have the same time values
	# 2. Find the difference between the two time-series
	
	s1=pd.Series(dfmodel[headerModel])
	s2=pd.Series(dfferry[headerFerry])
	print "Comparing the time-series of Ferrybox (%s) and %s"%(headerFerry,headerModel)
	
	fig=plt.figure()

	s1.plot()
	ax1=s2.plot()
 	#difference = s1.interpolate(method='time') - s2.interpolate(method='time')
 	#diff=difference[abs(difference) < 50]
 	#ax1=diff.plot(lw=1,style='m')

	ax1.set_xlim(startTime,endTime)
	ax1.set_ylim(-10,40)
 	ax1.legend(['DHI model','Ferrybox'])
 	#plt.show()
 	print "Saving plotfile: %s"%(plotfilename)
 
 	fig.savefig(plotfilename, bbox_inches='tight')
  
 #	s1.reindex(s2.index, method='pad')

 	s1, s2 = s1.align(s2)
	s1.interpolate(method='time')
	print "----------------------------"
 	print "Correlation: ", s1.corr(s2)
 	print "----------------------------"
 #	print "Average difference between time-series %s"%(np.mean(difference))

# Read the ferrybox data and the DHI modeled data and store in dataframes using time as index
modelfilename="DHIModel_chlorophylla.xlsx"
dfmodel,headerModel,startTime,endTime = getModelledData(modelfilename)

km='5km'

stations=["ST20925","ST1007","ST935","ST939","STN3","ST6700053"]

# Loop over the stations that we want to compare and create stats and plot
for compareIndex in xrange(len(stations)):

	ferryfilenameEdited="%s/station_%s_ferrybox_edited.csv"%(km,stations[compareIndex])
	plotfilename="figures/station_%s_%s_ferrybox_vs_DHImodel.png"%(stations[compareIndex],km)
	if os.path.exists(plotfilename):os.remove(plotfilename)

	print "Extracting ferry data %s"%(ferryfilenameEdited)
	dfferry,headerFerry = getFerryData(ferryfilenameEdited)

	interpolateTime(dfmodel,dfferry,stations[compareIndex],"Flu",compareIndex,startTime,endTime,plotfilename)