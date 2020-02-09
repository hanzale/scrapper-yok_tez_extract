import pickle

def save_var(variables,name):
	try:
		with open(name+'.pickle', 'wb') as handle:
			pickle.dump(variables, handle, protocol=pickle.HIGHEST_PROTOCOL)
			print('successfully saved')
	except:
		print ('unsuccessful save attempt')

def read_var(fname):
	try:	
		with open(fname+'.pickle','rb') as handle:
			loaded = pickle.load(handle)	
			print('successfully loaded')
			return loaded
	except:
		print ('unsuccessful load attempt')

