#	import libraries
from classes import Text, WordManifold
from dotenv import load_dotenv
import argparse, csv, os


if __name__ == '__main__':
	#	preproceses
	##	defines the environment variables
	load_dotenv()
	local_data	= os.environ['BIBLE_DATA']
	save_dir	= os.environ['BIBLE_SAVE_DIR']


	##	defines the input variables
	parser		= argparse.ArgumentParser()
	parser.add_argument('data_file_name', type=str, help='input ".txt" file name (the directory must be set in ".env").')
	parser.add_argument('lang', type=str, help='language code (for stanza)')
	parser.add_argument('save_file_name', type=str, help='output ".csv" file name (the directory must be set in ".env").')
	parser.add_argument('-mode', type=str, default='word', help='unit in consideration: "word", "chr", "upos", "xpos"')
	parser.add_argument('-n', type=int, default=7, help='max n-gram size.')
	parser.add_argument('-faster', action='store_false', help='If true, the process uses the approximate in getting betti number.')

	args = parser.parse_args()
	data_file_name	= args.data_file_name
	lang			= args.lang
	save_file_name	= args.save_file_name
	mode			= args.mode
	n				= args.n
	faster			= args.faster


	#	main processes
	##	processes the text
	text		= Text(path=f'{local_data}/{data_file_name}.txt', lang=lang)
	if mode		== 'word':
		text.parse_to_word()
	elif mode	== 'chr':
		text.parse_to_chr()
	elif mode	== 'upos':
		text.parse_to_upos()
	elif mode	== 'monkey_word':
		text.parse_to_monkey_word()
	elif mode	== 'monkey_chr':
		text.parse_to_monkey_chr()

	##	builds a word manifold to obtain the betti numbers for each dimension
	wm	= WordManifold(parsed_text=bible.parsed_sentences, n=n)
	wm.get_ngram()
	wm.get_skeleton()
	if faster:
		wm.get_boundary_mod2()
		wm.get_betti_mod2()
	else:
		wm.get_boundary()
		wm.get_betti()


	#	result
	##	writes the results to the .csv file
	with open(f'{save_dir}/{save_file_name}.csv', 'a', newline='') as f:
		writer	= csv.writer(f)
		writer.writerow([lang]+wm.betti)

	with open(f'{save_dir}/{save_file_name}-norm.csv', 'a', newline='') as f:
		writer	= csv.writer(f)
		writer.writerow([lang]+wm.betti_norm)