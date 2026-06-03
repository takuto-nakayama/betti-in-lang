from collections import Counter
# from concurrent.futures import as_completed, ThreadPoolExecutor  # used by fmpz_mat rank (commented out)
from datetime import datetime
from itertools import combinations
from flint import fmpz_mat
# from multiprocessing import Pool  # used by parallel get_boundary() (commented out)
import numpy as np
import itertools, math, stanza, textwrap


# [parallel] worker for get_boundary() — disabled due to Pool hang on macOS (spawn mode)
# def _boundary_worker(args):
# 	skeleton_n, skeleton_n1, n_i = args
# 	row_index  = {s: i for i, s in enumerate(skeleton_n)}
# 	n_rows     = len(skeleton_n)
# 	n_cols     = len(skeleton_n1)
# 	simplex_len = n_i + 2
# 	entries = {}
# 	for k in range(simplex_len):
# 		sign = 1 if k % 2 == 0 else -1
# 		for j, s_n1 in enumerate(skeleton_n1):
# 			face = s_n1[:k] + s_n1[k+1:]
# 			i = row_index.get(face)
# 			if i is not None:
# 				entries[(i, j)] = entries.get((i, j), 0) + sign
# 	coo = [(i, j, v) for (i, j), v in entries.items() if v != 0]
# 	return coo, n_rows, n_cols


def _rank_mod2(coo, n_rows, n_cols):
	cols = [set() for _ in range(n_cols)]
	for i, j, v in coo:
		if v % 2 != 0:
			cols[j].symmetric_difference_update({i})

	pivots = {}
	rank = 0
	for j in range(n_cols):
		col = set(cols[j])
		while col:
			r = min(col)
			if r not in pivots:
				pivots[r] = j
				cols[j] = col
				rank += 1
				break
			col ^= cols[pivots[r]]

	return rank


class Text:
	def __init__(self, path:str, lang:str):
		self.path = path
		self.lang = lang
		with open(self.path, mode='r', encoding='utf-8') as f:
			self.text	= f.readlines()
			self.parser	= stanza.Pipeline(
				self.lang,
				processors='tokenize,pos',
				tokenize_no_ssplit=True,
				use_gpu=True
				)


	def window_for_word(self, n:int=7):
		window	= []
		docs	= [stanza.Document([], text=snt) for snt in self.text]
		parsed_docs = self.parser(docs)
		for parsed in parsed_docs:
			words	= parsed.sentences[0].words
			for i in range(len(words)-n+1):
				window.append(tuple(w.text for w in words[i:i+n]))

		window_counter = Counter(window)
		items = sorted(window_counter)

		self.window = {
			'item':items,
			'frequency':[window_counter[w] for w in items]}

		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for word is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{n}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))


	def window_for_chr(self, n:int=7):
		window = []

		for snt in self.text:
			for i in range(len(snt)-n+1):
				window.append(tuple(snt[i:i+n]))

		window_counter = Counter(window)
		items = sorted(window_counter)
		self.window = {
			'item':items,
			'frequency':[window_counter[w] for w in items]}

		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for character is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{n}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))


	def window_for_upos(self, n:int=7):
		window = []
		docs	= [stanza.Document([], text=snt) for snt in self.text]
		parsed_docs = self.parser(docs)
		for parsed in parsed_docs:
			words	= parsed.sentences[0].words
			for i in range(len(words)-n+1):
				window.append(tuple(w.upos for w in words[i:i+n]))

		window_counter = Counter(window)
		items = sorted(window_counter)

		self.window = {
			'item':items,
			'frequency':[window_counter[w] for w in items]}

		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for UPOS is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{n}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))


	def window_for_xpos(self, n:int=7):
		window = []
		docs	= [stanza.Document([], text=snt) for snt in self.text]
		parsed_docs = self.parser(docs)
		for parsed in parsed_docs:
			words	= parsed.sentences[0].words
			for i in range(len(words)-n+1):
				window.append(tuple(w.xpos for w in words[i:i+n]))

		window_counter = Counter(window)
		items = sorted(window_counter)

		self.window = {
			'item':items,
			'frequency':[window_counter[w] for w in items]}

		print(textwrap.dedent(f'''
				{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} window for XPOS is done.
				
				{'-'*60}
				text source:		{self.path}
				language:		{self.lang}
				window size:		{n}
				types of windows	{len(self.window['item'])}
				total windows		{sum(self.window['frequency'])}
				{'-'*60}\n
			'''))



class WordManifold:
	def __init__(self, window:list):
		self.window	= window
		self.n			= len(window[0])


	def get_ngram(self):
		ngram		= []
		frequency	= []

		for n_i in range(1,self.n+1):
			ngram_i = []
			for win in self.window:
				for i in range(self.n-n_i+1):
					ngram_i.append(win[i:i+n_i])
			ngram_i_counter = Counter(ngram_i)
			ngram.append(sorted(ngram_i_counter))
			frequency.append([ngram_i_counter[j] for j in sorted(ngram_i_counter)])
		
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
				skeleton_i		= []
				frequency		= []
				lower_skeleton	= set(self.skeleton['item'][n_i-1])

				for idx, ngram in enumerate(self.ngram['item'][n_i]):
					all_faces_exist = all(
						ngram[:k] + ngram[k+1:] in lower_skeleton
						for k in range(len(ngram))
					)
					if all_faces_exist:
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
		self._boundary_coo = []
		for n_i in range(self.n-1):
			skeleton_n	= self.skeleton['item'][n_i]
			skeleton_n1 = self.skeleton['item'][n_i+1]
			row_index = {s: i for i, s in enumerate(skeleton_n)}
			n_rows = len(skeleton_n)
			n_cols = len(skeleton_n1)
			simplex_len = n_i + 2

			entries = {}
			for k in range(simplex_len):
				sign = 1 if k % 2 == 0 else -1
				for j, s_n1 in enumerate(skeleton_n1):
					face = s_n1[:k] + s_n1[k+1:]
					i = row_index.get(face)
					if i is not None:
						key = (i, j)
						entries[key] = entries.get(key, 0) + sign
			coo = [(i, j, v) for (i, j), v in entries.items() if v != 0]
			self._boundary_coo.append((coo, n_rows, n_cols))

			# [original] fmpz_mat construction — causes OOM for large matrices (e.g. word mode)
			# self.boundary = []
			# mat = fmpz_mat(n_rows, n_cols)
			# for i, j, v in coo:
			# 	mat[i, j] = v
			# self.boundary.append(mat)

			# [original] dense list construction + fmpz_mat
			# b = [[0] * n_cols for _ in range(n_rows)]
			# for k in range(simplex_len):
			# 	sign = 1 if k % 2 == 0 else -1
			# 	for j, s_n1 in enumerate(skeleton_n1):
			# 		face = s_n1[:k] + s_n1[k+1:]
			# 		i = row_index.get(face)
			# 		if i is not None:
			# 			b[i][j] += sign
			# self.boundary.append(fmpz_mat(b))
			# [original] O(|S_n| × |S_n1| × n) の三重ループ実装
			# b = np.zeros((len(skeleton_n), len(skeleton_n1)), dtype=int)
			# for i, s_n in enumerate(skeleton_n):
			# 	for j, s_n1 in enumerate(skeleton_n1):
			# 		for k, _ in enumerate(s_n1):
			# 			if s_n == s_n1[:k]+s_n1[k+1:]:
			# 				b[i,j] += int((-1)**k)
			# b = fmpz_mat(b.tolist())
			# self.boundary.append(b)

		# [parallel] macOS の spawn 方式では Pool が hang するため無効化
		# args = [(self.skeleton['item'][n_i], self.skeleton['item'][n_i+1], n_i)
		# 		for n_i in range(self.n-1)]
		# with Pool() as pool:
		# 	results = pool.map(_boundary_worker, args)
		# self.boundary = []
		# for coo, n_rows, n_cols in results:
		# 	b = [[0] * n_cols for _ in range(n_rows)]
		# 	for i, j, v in coo:
		# 		b[i][j] = v
		# 	self.boundary.append(fmpz_mat(b))

		print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} boundary is done.\n')


	def get_betti(self):
		ranks = []
		for n_i, (coo, n_rows, n_cols) in enumerate(self._boundary_coo):
			r = _rank_mod2(coo, n_rows, n_cols)
			print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} rank of boundary[{n_i}] ({n_rows}x{n_cols}) = {r}', flush=True)
			ranks.append(r)

		# [original] fmpz_mat exact rank over Z (slow for large matrices)
		# ranks = [None] * len(self.boundary)
		# with ThreadPoolExecutor() as executor:
		# 	futures = {executor.submit(b.rank): n_i for n_i, b in enumerate(self.boundary)}
		# 	for future in as_completed(futures):
		# 		n_i = futures[future]
		# 		b = self.boundary[n_i]
		# 		ranks[n_i] = future.result()
		# 		print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} rank of boundary[{n_i}] ({b.nrows()}x{b.ncols()}) = {ranks[n_i]}', flush=True)

		self.betti = []
		for n_i in range(self.n-2):
			_, _, m = self._boundary_coo[n_i]
			self.betti.append(m - ranks[n_i+1] - ranks[n_i])
		
		print(textwrap.dedent(f'''
			{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} betti number is done.
			==================
			|{str('n').center(5)}|{str('betti').center(10)}|
			|{'-'*5}|{'-'*10}|'''))
		for n, b in enumerate(self.betti):
			print(f'|{str(n+1).center(5)}|{str(b).center(10)}|')
		print('==================')