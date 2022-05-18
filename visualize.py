# Visualization of Solar Irradiance
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 17.5.22

import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

df = pd.read_csv("./output.csv")

df.plot(x='Wavelength(nm)', y='Irradiance(W/m2/um)')

plt.show()


