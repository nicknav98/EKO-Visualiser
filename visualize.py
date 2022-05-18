# Visualization of Solar Irradiance
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 17.5.22

# Config for connectiing to database
HOST = "192.168.0.122"
PORT = "5432"

import psycopg2
import pandas as pd
import numpy as np
import reprlib
from matplotlib import pyplot as plt

try:
    connection = psycopg2.connect(user="postgres",
                                  password="aurinko88",
                                  host=HOST,
                                  port=PORT,
                                  database="RadianceDB")
    # sql query to gather data, executes query and parses the timestamp column as datetime
    sql_select_Query = "select * from radiance"
    SQL_Query = pd.read_sql_query(sql_select_Query, connection, parse_dates=['Timestamp'])
    print("Successfully extracted data from DB\n")

    # converts sql data to pandas dataframe for plotting
    df = pd.DataFrame(SQL_Query, columns=['Wavelength(nm)', 'Timestamp', 'Irradiance(W/m2/um)'])
    # START - splits table based on datetime, comparison is done with previous
    # split to get dataframe chunks with same time stamp
    df1 = df[df['Timestamp'] != df.iloc[0, 1]]
    df2 = df1[df1['Timestamp'] != df1.iloc[0, 1]]
    df3 = df2[df2['Timestamp'] != df2.iloc[0, 1]]
    # END of splitting

    # Parameters for graph layout
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # START
    # initializes graph, adds subplots to support multiple y lines
    # ax acts as twins of one another, to copy the x axis from eachother, and plot
    x_axis = df1['Wavelength(nm)'].to_numpy(dtype='float')
    x_axisArray = x_axis.flatten()
    x_axis_rounded = [round(x) for x in x_axisArray]
    fig = plt.figure()
    plt.xticks(x_axis_rounded)
    plt.axes().set_xticklabels(x_axis_rounded)
    plt.plot(df['Irradiance(W/m2/um)'], 'c')
    plt.plot(df1['Irradiance(W/m2/um)'], 'r')
    plt.plot(df2['Irradiance(W/m2/um)']), 'g'
    plt.plot(df3['Irradiance(W/m2/um)'], 'y')
    # END

    # Graph labels
    plt.ylabel("Irradiance(W/m2/um)")
    plt.xlabel("Wavelength(nm)")
    plt.show()

#except(Exception, psycopg2.Error) as Error:
    #print("Error while connecting: ", Error)

finally:
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")
