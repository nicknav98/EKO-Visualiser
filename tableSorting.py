# Solar Irradiance Data Cleaning
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 16.5.22
import pandas as pd
from sqlalchemy import create_engine
import numpy as np


# handles connection to database, replace IP and table name to whatever database
# this uses a postgres docker container that is running on the nerc-postgres raspberry pi - connected to the NERC network.
# IP address is raspi. ip on network.
engine = create_engine('postgresql+psycopg2://postgres:aurinko88@192.168.0.122:5432/RadianceDB')
# file location of the CSV exported by EOX
fileLocation = './testData/2022051315.CSV'
# If you want to record the cleaned data to a CSV, use panda to parse to desired output CSV File
outputFile = './output.csv'

# reads csv file from file location variable, change as necessary
df = pd.read_csv(fileLocation, sep='[,]', engine='python', header=None)
# removes top 7 rows of data, these include sensor temp. and model, which is not needed
topObj = df.iloc[:6]
topObjNew = topObj.iloc[:2]
# transposes the data to column format, if you need to export it
topObjTransposed = topObjNew.T


# Time recording section, isolates date and time, and transposes it horizontally
dateTime = topObjTransposed

dateTime.columns = dateTime.iloc[0]
dateTime.drop(index=dateTime.index[0], axis=0, inplace=True)
isolatedDateTime = dateTime.iloc[1]

print(isolatedDateTime)
# isolates the first row for date time, converts it into a 2d array
# converts 2d day to numpy array and flattens it to list.
timeStamp2DArray = isolatedDateTime.values.tolist()
timeStamp2DArray = np.array(timeStamp2DArray)
flatten = timeStamp2DArray.flatten()
print(flatten)

# converses the flatten list to datetime format
# timeStamp = pd.to_datetime(dateTimeTransposed['Date'] + ' ' + dateTimeTransposed['Time'], cache=True)
merged = ' '.join(flatten)
timeStampTest = pd.to_datetime(merged)
print(merged) # checking if date time conversion was done correctly

# END ----------------


# Data readings, wavelength and irradiance
bottomData = df.iloc[7:]
# Focus only on the first data points, at EOX updates every hour, meaning first data set in XX:00
hourData = bottomData.drop(columns=[2, 3, 4, 5, 6, 7])

# Resets headers of dataframe to 'wavelength and irradiance'
hourData.columns = hourData.iloc[0]
# Resets index so first data entry is '0' on index
hourData.drop(index=hourData.index[0], axis=0, inplace=True)

# before conversion takes place, original datatypes are held, not important, but good for error catching
beforeConversion = hourData.dtypes

# converts all data on irradiance column to float, important for comparison
hourData['Irradiance(W/m2/um)'] = hourData['Irradiance(W/m2/um)'].astype('float')

# -----------------------------------------
# This section of code focuses on cleaning of data, further development needed.
# iterates value per row on column irradiance to see if value is lower than 200 (Limit set by Hugo)
# hourData.drop(hourData[hourData['Irradiance(W/m2/um)'] < 200.0].index, inplace=True)
# ------------------------------------------


# resets the index again so that the first data point is 0 on index
hourData = hourData.reset_index(drop=True)

# inserts NaT fields to the converted datetime variables
hourData.insert(1, 'Timestamp', 'x')
hourData['Timestamp'] = merged
hourData.replace({pd.NaT: str(merged)}, inplace=True)

# -------------------------------
# Takes only first 3 columns
finalData = hourData[hourData.columns[0:3]]

print(finalData)
# sends data to csv, for testing purposes - uncomment to run, will need 'output.csv' file in the same directory
# finalData.to_csv(r'./output.csv', index=False)

# sends data to sql using sql alchemy engine, and replaces the data on database.
finalData.to_sql('radiance', engine, if_exists='append', index=False)
