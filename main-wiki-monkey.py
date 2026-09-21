#	import libraries
from classes import WikiMonkey, WordManifold
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
	parser.add_argument('--batch', type=int, default=3000, help='batch size of Wikipedia articles per cycle')
	parser.add_argument('--mode', type=str, default='word', help='unit in consideration: "word", "chr", "upos", "xpos"')
	parser.add_argument('--n', type=int, default=7, help='max n-gram size.')
	parser.add_argument('--faster', action='store_false', help='If true, the process uses the approximate in getting betti number.')
	parser.add_argument('--total', type=int, default=100000)
	parser.add_argument('--num_roop', type=int, default=10)

	args = parser.parse_args()
	wiki_config	= args.wiki_config
	lang			= args.lang
	save_file_name	= args.save_file_name
	batch			= args.batch
	mode			= args.mode
	n				= args.n
	faster			= args.faster
	total			= args.total
	num_roop		= args.num_roop


	#	main processes
	##	processes the text
	for i in range(1,num_roop+1):
		wmonkey	= WikiMonkey(wiki_config=wiki_config, lang=lang, batch=batch, seed=i)
		if mode == 'monkey_chr':
			wmonkey.count_chr()
			monkeyed_text = wmonkey.generate_monkey_chr(seed=i, total=total)
		elif mode == 'monkey_word':
			wmonkey.count_word()
			monkeyed_text = wmonkey.generate_monkey_word(seed=i, total=total)
		elif mode == 'monkey_upos':
			wmonkey.count_upos()
			monkeyed_text = wmonkey.generate_monkey_upos(seed=i, total=total)

		##	builds a word manifold to obtain the betti numbers for each dimension
		wm	= WordManifold(parsed_text=monkeyed_text, n=n)
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
			writer.writerow([f'{lang}-{i}']+wm.betti)

		with open(f'{save_dir}/{save_file_name}-norm.csv', 'a', newline='') as f:
			writer	= csv.writer(f)
			writer.writerow([f'{lang}-{i}']+wm.betti_norm)