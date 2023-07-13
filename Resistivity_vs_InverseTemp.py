import pandas as pd
from Read_Data import all_data
from Calculations_and_Methods import feed_data, calc_resistivity, plotter

# Plots of resistivity vs Inverse Temp at different sample currents
resistivity_data= feed_data(all_data,
                            x_data = ("Inverse Temperature (K$^{-1}$)", lambda dataset: 1/pd.to_numeric(dataset["Temperature (K)"])),
                            y_data = ("Resistivity ($\Omega$m)", lambda dataset: calc_resistivity(dataset)))
room_temp = plotter(resistivity_data, "Resistivity vs. Inverse Temperature", find_room_temp = True)