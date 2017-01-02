import time, calendar
from datetime import datetime,timedelta
from netCDF4 import Dataset
import numpy as np
import os
import pandas as pd
import string
import geoLocation

__author__ = 'Trond Kristiansen'
__email__ = 'trond.kristiansen@niva.no'
__created__ = datetime(2016, 12, 20)
__modified__ = datetime(2016, 12, 20)
__version__ = "1.0"
__status__ = "Development"

def getFerryData(infilename,outfilename,loc1,maxDistance):

	infile=open(infilename)
	out=open(outfilename,'a')
	lines=infile.readlines()
	header=True

	for line in lines:
		if header is False:
			l = string.split(line,',')
			lon=float(l[1])
			lat=float(l[2])
			loc2=geoLocation.GeoLocation.from_degrees(lon,lat)

			distance=loc1.distance_to(loc2)
			if distance<maxDistance:
				out.writelines(line)
				print line
				print loc1 
				print loc2
				print distance
				print "\n"
		else:
			header=line
			out.writelines(header)
			header=False
	infile.close()
	out.close()

def dms2dd(degrees, minutes, seconds):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    
    return dd

infilename="2016_10_dkferrybox_00_Ferrybox_Data_20161220.csv"
maxDistance=2 # Max  distance in km from station and Ferrybox

stations=["STN3","ST20925","ST1007","ST935","ST939","ST6700053"]
stationLat=[[54,36,00],[56,07,38],[57,32,00],[55,39,05],[55,22,52],[55,30,463]]
stationLon=[[10,27,00],[11,9,38],[11,19,50],[10,45,36],[10,59,85],[10,51,724]]
counter=0
for station in stations:
	outfilename="station_%s_ferrybox.csv"%(station)
	if os.path.exists(outfilename): os.remove(outfilename)

	lat=stationLat[counter]
	lon=stationLon[counter]

	longitude = dms2dd(lon[0],lon[1],lon[2])
	latitude = dms2dd(lat[0],lat[1],lat[2])
	
	loc1=geoLocation.GeoLocation.from_degrees(longitude,latitude)
	ferryData = getFerryData(infilename,outfilename,loc1,maxDistance)


	counter+=1

	