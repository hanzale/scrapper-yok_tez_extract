import utils
import pandas as pd
import os

files = [f for f in os.listdir() if f.startswith('result_dataframe')]

df = pd.DataFrame(
	columns=['baslik', 'yil', 'tur', 'yazar', 'danisman', 'yer bilgisi', 'konu', 'dizin', 'anahtar'])

dataframes = []
for file in files:
	new_df = utils.read_var(file[:-7])
	dataframes.append(new_df)
df = pd.concat(dataframes)
df.to_html('output.html')