import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Read_Data import all_data

# Finds trans-resistance based on Van Der Pauw Technique & Formula
def vdp(df):
   I_AB = pd.to_numeric(df["sample current AB"])
   I_AD = pd.to_numeric(df["sample current AD"])
   I_AC = pd.to_numeric(df["sample current AC"])
   I_BD = pd.to_numeric(df["sample current BD"])
   I_BA = pd.to_numeric(df["sample current -AB"])
   I_DA = pd.to_numeric(df["sample current -AD"])
   I_CA = pd.to_numeric(df["sample current -AC"])
   I_DB = pd.to_numeric(df["sample current -BD"])

   V_CD = pd.to_numeric(df["Voltage CD"])
   V_BC = pd.to_numeric(df["Voltage BC"])
   V_BD = pd.to_numeric(df["Voltage BD"])
   V_AC = pd.to_numeric(df["Voltage AC"])
   V_DC = pd.to_numeric(df["Voltage -CD"])
   V_CB = pd.to_numeric(df["Voltage -BC"])
   V_DB = pd.to_numeric(df["Voltage -BD"])
   V_CA = pd.to_numeric(df["Voltage -AC"])

   # Convert values to numeric values
   I_DA = pd.to_numeric(I_DA)
   V_BC = pd.to_numeric(V_BC)

   # trans-resistance
   R_BADC = V_DC / I_BA
   R_DABC = V_BC / I_DA
   R_CADB = V_DB / I_CA
   R_DBAC = V_AC / I_DB
   R_ABCD = V_CD / I_AB
   R_ADCB = V_CB / I_DA

   results = {
      "R_BADC": R_BADC,
      "R_DABC": R_DABC,
      "R_CADB": R_CADB,
      "R_DBAC": R_DBAC,
      "R_ABCD": R_ABCD,
      "R_ADCB": R_ADCB
   }
   return results

# Calculate data's resistivity
def calc_resistivity(df):
   trans_resistance = vdp(df)
   R_ABCD = trans_resistance["R_ABCD"]
   R_ADCB = trans_resistance["R_ADCB"]

   d = 1.25e-3
   x = R_ABCD / R_ADCB
   f = 1 / np.cosh(np.log(x) / 2.403)

   # resistivity
   rho = (np.pi * d / np.log(2)) * 0.5 * (R_ABCD + R_ADCB) * f
   return rho

# Calculates data's hall coefficient
def calc_hall_coefficient(df):
   V_BC = pd.to_numeric(df["Voltage BC"], errors="coerce")
   V_CD = pd.to_numeric(df["Voltage CD"], errors="coerce")
   d = 1.25e-3
   I = pd.to_numeric(df["sample current AB"], errors="coerce")
   B = pd.to_numeric(df["B-Field (Gauss)"], errors="coerce")

   hall_voltage = pd.to_numeric((V_BC + V_CD) / 2, errors="coerce")
   R_H = -d * hall_voltage / (I * B)
   return R_H, hall_voltage



# Plots the data
def plotter(all_data, title, **kwargs):
   data_file = kwargs.get('data_file', False)
   find_room_temp = kwargs.get('find_room_temp', False)
   room_temp = kwargs.get('room_temp', 295)
   if find_room_temp:
      room_temp_data = {}

   # Plot configurations
   for dataset in all_data.items():
      plot_title = "{} (Sample Current: {}$\mu$A)".format(title, dataset[0][:3])
      if data_file:
         plot_title += "\nData file: {}".format(dataset[0])
      if find_room_temp:
         room_temp_data[dataset[0]] = {}
      plt.figure(figsize=(10, 8))
      for field in ["-B", "0B", "+B"]:
         dataset_idx = dataset[1][field]
         x_data_key, y_data_key = dataset_idx.keys()
         x_data = dataset_idx[x_data_key].reset_index(drop=True)
         y_data = dataset_idx[y_data_key].reset_index(drop=True)
         plt.plot(x_data, y_data, '-', label=field)
         plt.xlabel(x_data_key)
         plt.ylabel(y_data_key)

         if find_room_temp:
            for i in range(len(x_data)):
               if round(x_data[i], 4) == round(1 / room_temp, 4):
                  room_temp_data[dataset[0]][field] = y_data[i]

      plt.title(plot_title)
      plt.legend()
      plt.grid(alpha=0.3)
      plt.show()

   if find_room_temp:
      return room_temp_data

# Feeds/Puts the raw data into a more organized formate for plotting
def feed_data(all_data, x_data, y_data):
   data = {}
   for dataset in all_data.items():
      data[dataset[0]] = {}
      for field in ["-B", "0B", "+B"]:
         dataset_idx = dataset[1][field]
         dataset_filtered = dataset_idx.dropna(subset=["Temperature (K)"])
         dataset_filtered["Temperature (K)"] = pd.to_numeric(dataset_filtered["Temperature (K)"], errors="coerce")
         dataset_filtered = dataset_filtered.dropna(subset=["Temperature (K)"])
         data[dataset[0]][field] = {
            x_data[0]: x_data[1](dataset_filtered),
            y_data[0]: y_data[1](dataset_filtered)
         }
   return data

