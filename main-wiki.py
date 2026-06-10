#	import libraries
from classes import Text, Wiki, WordManifold
from dotenv import load_dotenv
import argparse, csv, os


if __name__ == '__main__':
	#	preproceses
	##	defines the environment variables
	load_dotenv()
	save_dir	= os.environ['WIKI_SAVE_DIR']


	##	defines the input variables
	parser		= argparse.ArgumentParser()
	parser.add_argument('wiki_config', type=str, help='wiki config name (e.g., 20231101.en')
	parser.add_argument('lang', type=str, help='language code (for stanza)')
	parser.add_argument('save_file_name', type=str, help='output ".csv" file name (the directory must be set in ".env").')
	parser.add_argument('-batch', type=int, default=5000, help='batch size of Wikipedia articles per cycle')
	parser.add_argument('-mode', type=str, default='word', help='unit in consideration: "word", "chr", "upos", "xpos"')
	parser.add_argument('-n', type=int, default=7, help='max n-gram size.')
	parser.add_argument('-faster', action='store_false', help='If true, the process uses the approximate in getting betti number.')

	args = parser.parse_args()
	wiki_config	= args.wiki_config
	lang			= args.lang
	save_file_name	= args.save_file_name
	batch			= args.batch
	mode			= args.mode
	n				= args.n
	faster			= args.faster


	#	main processes
	##	processes the wiki articles
	wiki		= Wiki(wiki_config=wiki_config, lang=lang, batch=batch)
	if mode		== 'word':
		wiki.parse_to_word()
	elif mode	== 'chr':
		wiki.parse_to_chr()
	elif mode	== 'upos':
		wiki.parse_to_upos()

	##	builds a word manifold to obtain the betti numbers for each dimension
	wm	= WordManifold(parsed_text=wiki.parsed_sentences, n=n)
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