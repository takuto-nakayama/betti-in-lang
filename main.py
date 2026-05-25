#	import libraries
from classes import Text, WordManifold
from dotenv import load_dotenv
import argparse, csv, os


if __name__ == '__main__':
	#	preproceses
	##	difines the environment variables
	load_dotenv()
	local_data	= os.environ['LOCAL_DATA']
	save_dir	= os.environ['SAVE_DIR']

	##	defines the input variables
	parser		= argparse.ArgumentParser()
	parser.add_argument('data_file_name', type=str, help='input ".txt" file name (the directory must be set in ".env").')
	parser.add_argument('lang', type=str, help='language code (for stanza)')
	parser.add_argument('save_file_name', type=str, help='output ".csv" file name (the directory must be set in ".env").')
	parser.add_argument('-mode', type=str, default='word', help='unit in consideration: "word", "chr", "upos", "xpos"')
	parser.add_argument('-k', type=int, default=5, help='window size')
	parser.add_argument('-n', type=int, default=5, help='n-gram size (must be smaller than or equal to the window size).')

	args = parser.parse_args()
	data_file_name	= args.data_file_name
	lang			= args.lang
	save_file_name	= args.save_file_name
	mode			= args.mode
	k				= args.k
	n				= args.n


	#	main processes
	##	processes the text
	text		= Text(path=f'{local_data}/{data_file_name}.txt', lang=lang)
	if mode		== 'word':
		text.window_for_word(k=k)
	elif mode	== 'chr':
		text.window_for_chr(k=k)
	elif mode	== 'upos':
		text.window_for_upos(k=k)
	elif mode	== 'xpos':
		text.window_for_xpos(k=k)	
	##	builds a word manifold to obtain the betti numbers for each dimension
	wm_words	= WordManifold(window=text.window['item'], n=n)
	wm_words.get_ngram()
	wm_words.get_skeleton()
	wm_words.get_boundary()
	wm_words.get_betti()


	#	result
	##	writes the results to the .csv file
	with open(f'{save_dir}/{save_file_name}.csv', 'a', newline='') as f:
		writer	= csv.writer(f)
		writer.writerow([lang]+wm_words.betti)