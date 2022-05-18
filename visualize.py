# Visualization of Solar Irradiance
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 17.5.22

#Config
HOST = "192.168.0.122"
PORT = "5432"



import psycopg2
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

try:
    connection = psycopg2.connect(user="postgres",
                                  password="aurinko88",
                                  host=HOST,
                                  port=PORT,
                                  database="RadianceDB")
    # cursor = connection.cursor()
    sql_select_Query = "select * from radiance"

    # cursor.execute(sql_select_Query)
    print("Successfully extracted data from DB\n")
    SQL_Query = pd.read_sql_query(sql_select_Query,connection)
    df = pd.DataFrame(SQL_Query, columns=['Wavelength(nm)', 'Timestamp', 'Irradiance(W/m2/um)'])


    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True


    df.plot(x='Wavelength(nm)', y='Irradiance(W/m2/um)')

    plt.show()

except(Exception, psycopg2.Error) as Error:
    print("Error while connecting: ", Error)

finally:
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")

