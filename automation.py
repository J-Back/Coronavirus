import requests
import pandas as pd
from io import StringIO

def GetData():
	response = requests.Session()

	dtype = {
		'X': float,
		'Y': float,
		'OBJECTID': str,
		'Province_State': str,
		'Country_Region': str,
		'Last_Update': str,
		'Lat': float,
		'Long_': float,
		'Confirmed': str,
		'Recovered': str,
		'Deaths': str,
		'Active': str,
		'Admin2': str,
		'FIPS': str,
		'Combined_Key': str,
		'Incident_Rate': str,
		'People_Tested': str
	}

	data = pd.read_csv(StringIO(response.get('https://opendata.arcgis.com/datasets/628578697fb24d8ea4c32fa0c5ae1843_0.csv').text), dtype = dtype, parse_dates = True)
	
	return data

def Main():
	data = GetData().rename(columns = {'Province_State': 'State', 'Admin2': 'County'})[['State', 'County', 'Confirmed', 'Recovered', 'Deaths']].sort_values(by = 'State', ascending = True).to_csv('data.csv')

if __name__ == '__main__':
	Main()
