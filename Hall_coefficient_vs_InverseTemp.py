from Read_Data import all_data
from Calculations_and_Methods import feed_data, calc_hall_coefficient, plotter

# Plots of Hall coefficient vs. Inverse Temp at different sample current
coefficient_data= feed_data(all_data,
                            x_data = ("Inverse Temperature (K$^{-1}$)", lambda dataset: 1/dataset["Temperature (K)"]),
                            y_data = ("Hall Coefficient (m$^3$/C)", lambda dataset: calc_hall_coefficient(dataset)[0]))
plotter(coefficient_data, "Hall Coefficient vs. Inverse Temperature")