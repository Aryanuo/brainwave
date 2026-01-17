import os
import pandas as pd

folder_path = os.path.join("..", "..", "dataset", "extracted")
output_path = os.path.join("..", "..", "dataset", "training_data.csv")

dfs = []

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)

    if file.endswith(".csv"):
        df = pd.read_csv(file_path)
        dfs.append(df)

    elif file.endswith(".xlsx") or file.endswith(".xls"):
        df = pd.read_excel(file_path)
        dfs.append(df)

if len(dfs) == 0:
    raise Exception("No CSV or XLSX files were found in extracted folder!")

merged_df = pd.concat(dfs, ignore_index=True)
merged_df.to_csv(output_path, index=False)

print("Merged training_data.csv created successfully!")
print("Shape:", merged_df.shape)
