import os
import scrapper_ilk
from scrapper_initial_func import scrap
name_prefix = 'result_dataframe'

files  = [name_prefix+str(i)+'.pickle' for i in range(2,123)]

years = [i for i in range(2,123)]

diction = dict(zip(files,years))

files_needed = [file for file in files if not os.path.exists(file)]
years_needed = [diction.get(file) for file in files_needed]

print(years_needed)
#scrapper_ilk.main_scrap(4)

for i in years_needed:
	try:
		scrapper_ilk.main_scrap(i)
	except:
		print(str(i)+' hata')
		pass

