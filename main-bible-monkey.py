#	import libraries
from classes import TextMonkey, WordManifold
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
	parser.add_argument('--mode', type=str, default='monkey_word', help='unit in consideration: "monkey_word", "monkey_chr", "monkey_upos"')
	parser.add_argument('--n', type=int, default=7, help='max n-gram size.')
	parser.add_argument('--faster', action='store_false', help='If true, the process uses the approximate in getting betti number.')
	parser.add_argument('--total', type=int, default=100000)
	parser.add_argument('--loop_start', type=int, default=1)
	parser.add_argument('--loop_end', type=int, default=10)

	args = parser.parse_args()
	data_file_name	= args.data_file_name
	lang			= args.lang
	save_file_name	= args.save_file_name
	mode			= args.mode
	n				= args.n
	faster			= args.faster
	total			= args.total
	loop_start		= args.loop_start
	loop_end		= args.loop_end


	#	main processes
	##	processes the text
	tm		= TextMonkey(path=f'{local_data}/{data_file_name}.txt', lang=lang)
	if mode	== 'monkey_word':
		tm.count_word()
	elif mode	== 'monkey_chr':
		tm.count_chr()
	elif mode == 'monkey_upos':
		tm.count_upos()

	for i in range(loop_start, loop_end+1):
		if mode == 'monkey_chr':
			monkeyed_text = tm.generate_monkey_chr(seed=i, total=total)
		elif mode == 'monkey_word':
			monkeyed_text = tm.generate_monkey_word(seed=i, total=total)
		elif mode == 'monkey_upos':
			monkeyed_text = tm.generate_monkey_upos(seed=i, total=total)

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