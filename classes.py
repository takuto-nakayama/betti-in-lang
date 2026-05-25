from itertools import combinations
import numpy as np
import math, stanza


class Text:
	def __init__(self, path:str, lang:str):
		with open(path, mode='r', encoding='utf-8') as f:
			self.text	= f.readlines()
			self.parser	= stanza.Pipeline(lang, processors='tokenize,pos', tokenize_no_ssplit=True)


	def window_for_word(self, k:int=5):
		window = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				window.append(
					[w.text for w in words[i:i+k]]
				)

		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i), for i in sorted(set(window))]
			}


	def window_for_chr(self, k:int=5):
		window = []

		for snt in self.text:
			for i in range(len(snt)-k+1):
				window.append(tuple(snt[i:i+k]))		

		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i), for i in sorted(set(window))]
			}
	


	def window_for_upos(self, k:int=5):
		window = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				window.append(
					[w.upos for w in words[i:i+k]]
				)

		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i), for i in sorted(set(window))]
			}


	def window_for_xpos(self, k:int=5):
		window = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				window.append(
					[w.xpos for w in words[i:i+k]]
				)

		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i), for i in sorted(set(window))]
			}



class WordManifold:
	def __init__(self, window:list, n:int):
		self.window	= window
		self.k			= len(window[0])
		self.n			= n					# n must be more than and equal to 2


	def get_ngram(self):
		ngram		= []
		frequency	= []
		for n_i in range(1,self.n+1):
			ngram_i = []
			for win in self.window:
				for i in range(self.k-n_i+1):
					ngram_i.append(win[i:i+n_i])
			ngram.append(sorted(set(ngram_i)))
			frequency.append([ngram_i.count(j) for j in sorted(set(ngram_i))])
		
		self.ngram = {
			'item':ngram,
			'frequency':frequency
		}



	def get_skeleton(self):
		if self.n <= 2:
			self.skeleton = self.ngram

		else:
			self.skeleton = {
				'item':		[self.ngram['item'][0], self.ngram['item'][1]],
				'frequency':[self.ngram['frequency'][0], self.ngram['frequency'][1]]
				}
				
			for n_i in range(2,self.n):
				skeleton_i	= []
				frequency	= []

				for idx, ngram in enumerate(self.nrams['item'][n_i]):
					combo = list(combinations(ngram, n_i))
					p, q = 0, 1
					for r, c in enumerate(combo):
						if p == r:
							p 	+= math.comb(self.k-q, n_i-1)
							q	+= 1
						else:
							if c not in self.ngram['item'][n_i-1]:
								not_found = True
								break
					if not_found:
						break
					skeleton_i.append(ngram)
					frequency.append(self.ngram['frequency'][n_i][idx])
				
				self.skeleton['item'].append(skeleton_i)
				self.skeleton['frequency'].append(frequency)


	def get_boundary(self):
		self.boundary = []
		for n_i in range(self.n-1):
			skeleton_n, skeleton_n1 = self.skeleton['item'][n_i], self.skeleton['item'[n_i+1]]
			b = np.zeros((len(skeleton_n), len(skeleton_n1)))

			for i, s_n in enumerate(skeleton_n):
				for j, s_n1 in enumerate(skeleton_n1):
					for k, _ in enumerate(s_n1):
						if s_n == s_n1[:k]+s_n1[k+1:]:
							b[i,j] += (-1)**k
			self.boundary.append(b)


	def get_betti(self):
		self.betti = []
		for n_i in range(self.n-1):
			b_n		= self.B[n_i]
			b_n1	= self.B[n_i+1]

			m = b_n.shape[1]
			r = b_n1.rank()
			s = b_n.rank()

			self.betti.append(m - r - s)