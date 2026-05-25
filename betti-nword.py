#	import libraries
from classes import Text, WordManifold
from dotenv import load_dotenv
import csv, os


#	preproceses
##	difines the environment variables
load_dotenv()
local_data	= os.environ['LOCAL_DATA']
save_dir	= os.environ['SAVE_DIR']

##	defines the input variables
data_file_name 	= str()  # input in CLI
lang 			= str()  # input in CLI
k				= int()  # input in CLI
n				= int()  # input in CLI
save_file_name	= str()  # input in CLI


#	main processes
##	processes the text
text				= Text(path=f'{local_data}/{data_file_name}.txt', lang=lang)
windowed_words		= text.window_for_word(k=k)

##	builds a word manifold to obtain the betti numbers for each dimension
wm_words			= WordManifold(windowed=windowed_words, n=n)
wm_words.get_ngram()
wm_words.get_skeleton()
wm_words.get_boundary()
wm_words.get_betti()


#	result
##	writes the results to the .csv file
with open(f'{save_dir}/{save_file_name}.csv', 'a', newline='') as f:
	writer = csv.writer(f)
	writer.writerow([lang]+wm_words.betti)