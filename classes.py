from datetime import datetime
from itertools import combinations
from flint import fmpz_mat
import numpy as np
import itertools, math, stanza, textwrap


class Text:
	def __init__(self, path:str, lang:str):
		self.path = path
		self.lang = lang
		with open(self.path, mode='r', encoding='utf-8') as f:
			self.text	= f.readlines()
			self.parser	= stanza.Pipeline(self.lang, processors='tokenize,pos', tokenize_no_ssplit=True)


	def window_for_word(self, k:int=5):
		window = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				window.append(
					[w.text for w in words[i:i+k]]
				)
		window = [tuple(w) for w in window]
		
		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i) for i in sorted(set(window))]}
		
		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for word is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{k}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))


	def window_for_chr(self, k:int=5):
		window = []

		for snt in self.text:
			for i in range(len(snt)-k+1):
				window.append(tuple(snt[i:i+k]))		
		
		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i) for i in sorted(set(window))]}
		
		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for character is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{k}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))


	def window_for_upos(self, k:int=5):
		window = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				window.append(
					[w.upos for w in words[i:i+k]]
				)

		window = [tuple(w) for w in window]
		
		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i) for i in sorted(set(window))]}

		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for UPOS is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{k}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))


	def window_for_xpos(self, k:int=5):
		window = []		
		for snt in self.text:
			parsed	= self.parser(snt)
			words	= parsed.sentences[0].words
			for i in range(len(words)-k+1):
				window.append(
					[w.xpos for w in words[i:i+k]]
				)

		window = [tuple(w) for w in window]
		
		self.window = {
			'item':sorted(set(window)),
			'frequency':[window.count(i) for i in sorted(set(window))]}

		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for XPOS is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{k}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))



class WordManifold:
	def __init__(self, window:list, n:int):
		self.window	= window
		self.k			= len(window[0])
		self.n			= n


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

		print(textwrap.dedent(f'''
			{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ngam is done (n={self.n}).
						
			{'='*29}
			|{str('n').center(5)}|{str('type').center(10)}|{str('total').center(10)}|
			|{'-'*5}|{'-'*10}|{'-'*10}|'''))
		for n, ng in enumerate(self.ngram['item']):
			print(f'|{str(n+1).center(5)}|{str(len(ng)).center(10)}|{str(sum(self.ngram['frequency'][n])).center(10)}|')
		print(f'{'='*29}')


	def get_skeleton(self):
		if self.n <= 2:
			self.skeleton	= self.ngram

		else:
			self.skeleton	= {
				'item':		[self.ngram['item'][0], self.ngram['item'][1]],
				'frequency':[self.ngram['frequency'][0], self.ngram['frequency'][1]]
				}

			for n_i in range(2,self.n):
				skeleton_i	= []
				frequency	= []
				not_found	= False

				for idx, ngram in enumerate(self.ngram['item'][n_i]):
					combo	= list(combinations(ngram, n_i))
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
		
		print(textwrap.dedent(f'''
			{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} skeleton is done.

			{'='*29}
			|{str('n').center(5)}|{str('type').center(10)}|{str('total').center(10)}|
			|{'-'*5}|{'-'*10}|{'-'*10}|'''))
		for n, s_n in enumerate(self.skeleton['item']):
			print(f'|{str(n+1).center(5)}|{str(len(s_n)).center(10)}|{str(sum(self.skeleton['frequency'][n])).center(10)}|')
		print(f'{'='*29}')



	def get_boundary(self):
		self.boundary = []
		for n_i in range(self.n-1):
			skeleton_n, skeleton_n1 = self.skeleton['item'][n_i], self.skeleton['item'][n_i+1]
			b = np.zeros((len(skeleton_n), len(skeleton_n1)), dtype=int)

			for i, s_n in enumerate(skeleton_n):
				for j, s_n1 in enumerate(skeleton_n1):
					for k, _ in enumerate(s_n1):
						if s_n == s_n1[:k]+s_n1[k+1:]:
							b[i,j] += int((-1)**k)
			b = fmpz_mat(b.tolist())
			self.boundary.append(b)
		
		print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} boundary is done.\n')


	def get_betti(self):
		self.betti = []
		for n_i in range(self.n-2):
			b_n		= self.boundary[n_i]
			b_n1	= self.boundary[n_i+1]

			m = b_n.ncols()
			r = b_n1.rank()
			s = b_n.rank()

			self.betti.append(m - r - s)
		
		print(textwrap.dedent(f'''
			{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} betti number is done.
			==================
			|{str('n').center(5)}|{str('betti').center(10)}|
			|{'-'*5}|{'-'*10}|'''))
		for n, b in enumerate(self.betti):
			print(f'|{str(n+1).center(5)}|{str(b).center(10)}|')
		print('==================')