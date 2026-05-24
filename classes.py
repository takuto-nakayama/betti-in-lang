from itertools import combinations
import math, stanza


class Text:
	def __init__(self, path:str, lang:str):
		with open(path, mode='r', encoding='utf-8') as f:
			self.text	= f.readlines()
			self.parser	= stanza.Pipeline(lang, processors='tokenize,pos', tokenize_no_ssplit=True)


	def window_for_word(self, k:int=5):
		windowed_text = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				windowed_text.append(
					[w.text for w in words[i:i+k]]
				)

		return windowed_text


	def window_for_chr(self, k:int=5):
		windowed_text = []

		for snt in self.text:
			for i in range(len(snt)-k+1):
				windowed_text.append(tuple(snt[i:i+k]))
			
		return windowed_text


	def window_for_upos(self, k:int=5):
		windowed_text = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				windowed_text.append(
					[w.upos for w in words[i:i+k]]
				)

		return windowed_text


	def window_for_xpos(self, k:int=5):
		windowed_text = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				windowed_text.append(
					[w.xpos for w in words[i:i+k]]
				)

		return windowed_text



class WordManifold:
	def __init__(self, windowed:list):
		self.windowed	= windowed
		self.k			= len(windowed[0])


	def skeleton(self, N:int=3):
		skeleton = []

		if N > self.k:
			print('ERROR: n is greater than the window size.')

		else:
			for window in self.windowed:
				combo = list(combinations(window, 1))
				for subseq in combo:
					skeleton.append(subseq)

				for n in range(2, N+1):
					combo = list(combinations(window, n))
					i, j, l = 0, 1, 0

					while i < len(combo):
						if i 	== l:
							skeleton.append(combo[i])
							i 	+= math.comb(self.k-j, n-1)
							j 	+= 1
							l 	+= 1

						else:
							for win in self.windowed:
								for m in range(self.k-n+1):
									if combo[l] == win[m:m+n]:
										skeleton.append(combo[l])
							l += 1

		set_skeleton	= set(skeleton)
		dict_skeleton	= {s:skeleton.count(s) for s in set_skeleton}

		return dict_skeleton


	def boundary(self):
		pass


	def betti(self):
		pass