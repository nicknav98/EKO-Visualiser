# Solar Irradiance AM1.5 Standard
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 16.5.22

import os
import pandas as pd
from sqlalchemy import create_engine
import secrets

engine = create_engine('postgresql+psycopg2://'+secrets.docker_user+':'+secrets.docker_password+'@172.24.59.97:5432/RadianceDB')

fileLocation = './testData/Backup/Backup.part2/standardSpec.CSV' #Change this to location of editied CSV file

df = pd.read_csv(fileLocation, sep='[,]', engine='python')
df['Irradiance(W/m2/um)'] = df['Irradiance(W/m2/um)'].astype('float')
df['Timestamp'] = df['Timestamp'].astype('string')
del df['Irradiance']
# inserts NaT fields to the converted datetime variables
df.replace({pd.NaT: 'Direct Standard Irradiance(AM1.5)'}, inplace=True)
df.dropna(subset=["Irradiance(W/m2/um)"], inplace=True)


print(df)

df.to_sql('radiance', engine, if_exists='append', index=False)
print('\nData successfully transferred to Postgres\n')

