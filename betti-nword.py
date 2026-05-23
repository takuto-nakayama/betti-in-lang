from classes import Text, WordManifold


path 	= str()  # input in CLI
lang 	= str()  # input in CLI
k		= int()  # input in CLI
n		= int()  # input in CLI


text			= Text(path=path, lang=lang)
windowed_words	= text.window_for_word(k=k)

wm_words		= WordManifold(windowed=windowed_words)
skeleton_words	= wm_words.skeleton(N=n)
boundary_words	= wm_words.boundary()
