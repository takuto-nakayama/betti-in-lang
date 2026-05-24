from classes import Text, WordManifold


path 	= str()  # input in CLI
lang 	= str()  # input in CLI
k		= int()  # input in CLI
N		= int()  # input in CLI


text				= Text(path=path, lang=lang)
windowed_words		= text.window_for_word(k=k)

wm_words			= WordManifold(windowed=windowed_words)
skeleton_words_n	= wm_words.skeleton(N=1)

for n in range(1,N):
	skeleton_words_n1	= wm_words.skeleton(N=n+1)
	boundary_words		= wm_words.boundary(
		skeleton_words_n,
		skeleton_words_n1
		)
	skeleton_words_n = skeleton_words_n1
