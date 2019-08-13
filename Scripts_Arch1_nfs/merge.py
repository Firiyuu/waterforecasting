import pandas as pd
import datetime as dt

df_a = pd.read_csv("Mandulog_interpol.csv")
df_a.columns = ['DATETIME',"WATERLEVEL"]
df_b = pd.read_csv("Digkilaan_interpol.csv")
df_b.columns = ['DATETIME',"RAINFALL"]



reference_date = dt.datetime(2019,1,1) # Arbitrary date used for reference
df_a.index = df_a['DATETIME'].apply(lambda x: reference_date + pd.DateOffset(x))
df_b.index = df_b['DATETIME'].apply(lambda x: reference_date + pd.DateOffset(x))

new_a = df_a['RAINFALL'].groupby(pd.TimeGrouper(freq='30T')).apply(lambda x: x.tolist())
new_b = df_b['WATERLEVEL'].groupby(pd.TimeGrouper(freq='30T')).apply(lambda x: x.tolist())

merged_df = pd.concat({'RAINFALL': new_a, 'WATERLEVEL': new_b}, axis = 1, sort=True)

merged = merged_df.index = (merged_df.index - reference_date).seconds # Return to original Time format

merged_df.to_csv(r'merged.csv')