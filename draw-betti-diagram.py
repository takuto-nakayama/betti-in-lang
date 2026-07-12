import argparse
from classes import Network

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'text_path',
		type=str,
		help='[str] the file path of the target text'
	)

	parser.add_argument(
		'n',
		type=int,
		help='[int] the number of n-gram that is a loop in the network. It must be >= 2.'
	)

	parser.add_argument(
		'--title',
		type=str,
		default='Network',
		help='the title that is printed on the diagram'
	)

	parser.add_argument(
		'--save_path',
		type=str,
		default='network-',
		help='[str | default="betti-diagram"] the file name for saving the diagram (an extension (.html) will be added automatically)'
	)

	parser.add_argument(
		'--save',
		action='store_true',
		help='[bool | default=False] will save the diagram if this is on.'
	)

	parser.add_argument(
		'--dont_show',
		action='store_true',
		help='[bool | default=False] will not show the diagram immediately if this is on.'
	)

	args = parser.parse_args()
	text_path = args.text_path
	n = args.n
	title = args.title
	save_path = args.save_path
	save = args.save
	dont_show = args.dont_show


	network = Network(text_path=text_path)
	network.draw_network_1(title=title, save_path=save_path, save=save, dont_show=dont_show)
	network.draw_network_n(n=n, title=title, save_path=save_path, save=save, dont_show=dont_show)
