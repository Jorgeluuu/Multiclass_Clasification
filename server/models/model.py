import pandas as pd
import os
# ---------------------------------------------------------------------------------------------------------------------
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, "data")
file_path = os.path.join(data_dir, "")
raw_data_csv_path = os.path.join(data_dir, "raw_data.csv")

df_students = pd.read_csv(raw_data_csv_path)

 # ---------------------------------------------------------------------------------------------------------------------