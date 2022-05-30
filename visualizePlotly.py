# Visualization of Solar Irradiance with Plotly Lib
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 19.5.22

# Config for connectiing to database
HOST = "172.24.59.97"
PORT = "5432"

import psycopg2
import pandas as pd
import plotly.express as px

try:
    connection = psycopg2.connect(user="postgres",
                                  password="aurinko88",
                                  host=HOST,
                                  port=PORT,
                                  database="RadianceDB")
    # sql query to gather data, executes query and parses the timestamp column as datetime
    sql_select_Query = "select * from radiance"
    SQL_Query = pd.read_sql_query(sql_select_Query, connection)
    print("Successfully extracted data from DB\n")

    # converts sql data to pandas dataframe for plotting
    df = pd.DataFrame(SQL_Query, columns=['Wavelength(nm)', 'Timestamp', 'Irradiance(W/m2/um)'])

    # Parameters for graph layout
    # START --- Graph Construction Get Wavelenth value as numpy array, flattens it as a normal array, converts it to
    # int, and assigns to x-xis in graph
    x_axis = df['Wavelength(nm)'].to_numpy(dtype='float')
    x_axisArray = x_axis.flatten()
    x_axis_rounded = [round(x) for x in x_axisArray]
    fig = px.line(df, x=x_axis_rounded, y='Irradiance(W/m2/um)', color=df['Timestamp'],#.to_numpy(dtype='str'),
                  labels={'x': 'Wavelength(nm)'})
    fig.update_layout(
        title={
            'text': "Irradiance Spectrum by Hour",
            'x': 0.5,
            'xanchor': 'right',
            'yanchor': 'top'},
        plot_bgcolor='black',
        legend_font_size=30)
    fig.show()

    # END



except(Exception, psycopg2.Error) as Error:
    print("Error while connecting: ", Error)

finally:
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")
