# Visualization of Solar Irradiance with Plotly Lib
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 19.5.22

# Config for connectiing to database
HOST = "172.24.59.97"
PORT = "5432"

import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

try:

    connection = create_engine('postgresql://postgres:aurinko88@' + HOST + ':' + PORT + '/RadianceDB')
    # sql query to gather data, executes query and parses the timestamp column as datetime
    sql_select_Query = "select * from radiance where \"Timestamp\" NOT LIKE '%%AM1.5%%'"
    sql_standard_query = "select * from radiance where \"Timestamp\" LIKE '%%AM1.5%%'"
    SQL_Query = pd.read_sql_query(sql_select_Query, connection)
    SQL_Standard = pd.read_sql_query(sql_standard_query, connection)
    print("Successfully extracted data from DB\n")

    # converts sql data to pandas dataframe for plotting
    df = pd.DataFrame(SQL_Query, columns=['Wavelength(nm)', 'Timestamp', 'Irradiance(W/m2/um)'])
    standard_df = pd.DataFrame(SQL_Standard, columns=['Wavelength(nm)', 'Timestamp', 'Irradiance(W/m2/um)'])

    # Parameters for graph layout
    # START --- Graph Construction Get Wavelenth value as numpy array, flattens it as a normal array, converts it to
    # int, and assigns to x-xis in graph
    x_axis = df['Wavelength(nm)'].to_numpy(dtype='float')
    x_axisArray = x_axis.flatten()

    x_axis_rounded = [round(x) for x in x_axisArray]
    standardX = standard_df['Wavelength(nm)'].to_numpy(dtype='float')
    standardArray = standardX.flatten()
    x_standard_rounded = [round(x) for x in standardArray]

    fig = px.line(df, x=x_axis_rounded, y='Irradiance(W/m2/um)', color=df['Timestamp'],
                  labels={'x': 'Wavelength(nm)'})

    fig.add_scatter(cliponaxis=True, x=x_standard_rounded, y=standard_df['Irradiance(W/m2/um)'], line_color='white',
                    line_width=5, name="Direct Standard Irradiance(AM1.5)")
    # fig = go.Figure(data=go.Scatter(x=x_axis,y=y_axis, name='AM1.5', line_shape='spline'))

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



except SQLAlchemyError as Error:
    print("Error while connecting: ", Error)

finally:
   print("PostgreSQL connection is closed")
