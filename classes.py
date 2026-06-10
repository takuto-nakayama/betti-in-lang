from collections import Counter
from datetime import datetime
from itertools import combinations
from flint import fmpz_mat
from datasets import load_dataset
import numpy as np
import itertools, math, random, stanza, textwrap



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
			self.text	= [line.strip() for line in f.readlines()]
			self.parser	= stanza.Pipeline(
				self.lang,
				processors='tokenize,pos',
				tokenize_no_ssplit=True,
				use_gpu=True
				)


	def parse_to_word(self):
		self.parsed_sentences = []
		docs = [stanza.Document([], text=snt) for snt in self.text]
		parsed_docs = self.parser(docs)
		for parsed in parsed_docs:
			self.parsed_sentences.append(
				tuple(
					w.text for w in parsed.sentences[0].words
				)
			)
		
		print(textwrap.dedent(f'''
		{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} parsing into word is done.
		{'='*50}
		text source:		{self.path}
		language:		{self.lang}
		length			{len(self.parsed_sentences)}
		{'='*50}
		'''))


	def parse_to_chr(self):
		self.parsed_sentences =self.text

		print(textwrap.dedent(f'''
		{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} parsing into character is done.
		{'='*50}
		text source:		{self.path}
		language:		{self.lang}
		length			{len(self.parsed_sentences)}
		{'='*50}
		'''))


	def parse_to_upos(self):
		self.parsed_sentences = []
		docs = [stanza.Document([], text=snt) for snt in self.text]
		parsed_docs = self.parser(docs)
		for parsed in parsed_docs:
			self.parsed_sentences.append(
				tuple(
					w.upos for w in parsed.sentences[0].words
				)
			)
		
		print(textwrap.dedent(f'''
		{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} parsing into upos is done.
		{'='*50}
		text source:		{self.path}
		language:		{self.lang}
		length			{len(self.parsed_sentences)}
		{'='*50}
		'''))




class Wiki:
	def __init__(self, wiki_config:str, lang:str, batch:int):
		self.wiki_config = wiki_config
		self.lang = lang
		self.parser	= stanza.Pipeline(
			self.lang,
			processors='tokenize,pos',
			tokenize_no_ssplit=True,
			use_gpu=True
			)


		dataset = load_dataset('wikimedia/wikipedia', wiki_config, split='train')
		indices = random.sample(range(len(dataset)), k=batch)
		sampled = dataset.select(indices)
		self.sentences = []

		for article in sampled:
			for para in article['text'].split('\n'):
				if para.strip():
					self.sentences.append(para.strip())


	def parse_to_word(self):
		self.parsed_sentences = []
		docs = [stanza.Document([], text=snt) for snt in self.sentences]
		parsed_docs = self.parser(docs)
		for parsed in parsed_docs:
			self.parsed_sentences.append(
				tuple(
					w.text for w in parsed.sentences[0].words
				)
			)
		
		print(textwrap.dedent(f'''
		{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} parsing into word is done.
		{'='*50}
		text source:		{self.wiki_config}
		language:		{self.lang}
		sentences		{len(self.parsed_sentences)}
		tokens			{len([_ for snt in self.parsed_sentences for _ in snt])}
		{'='*50}
		'''))


	def parse_to_chr(self):
		self.parsed_sentences =self.sentences

		print(textwrap.dedent(f'''
		{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} parsing into character is done.
		{'='*50}
		text source:		{self.wiki_config}
		language:		{self.lang}
		sentences			{len(self.parsed_sentences)} sentences.
		tokens			{len([_ for snt in self.parsed_sentences for _ in snt])}
		{'='*50}
		'''))


	def parse_to_upos(self):
		self.parsed_sentences = []
		docs = [stanza.Document([], text=snt) for snt in self.sentences]
		parsed_docs = self.parser(docs)
		for parsed in parsed_docs:
			self.parsed_sentences.append(
				tuple(
					w.upos for w in parsed.sentences[0].words
				)
			)
		
		print(textwrap.dedent(f'''
		{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} parsing into upos is done.
		{'='*50}
		text source:		{self.wiki_config}
		language:		{self.lang}
		sentences		{len(self.parsed_sentences)}
		tokens			{len([_ for snt in self.parsed_sentences for _ in snt])}
		{'='*50}
		'''))



class WordManifold:
	def __init__(self, parsed_text:list, n:int):
		self.parsed_text = parsed_text
		self.n = n


	def get_ngram(self):
		ngram		= []
		frequency	= []

		for n_i in range(1,self.n+1):
			ngram_i = []
			for snt in self.parsed_text:
				for i in range(self.n-n_i+1):
					ngram_i.append(snt[i:i+n_i])
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
			print(f'|{str(n).center(5)}|{str(len(ng)).center(10)}|{str(sum(self.ngram['frequency'][n])).center(10)}|')
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
			print(f'|{str(n).center(5)}|{str(len(s_n)).center(10)}|{str(sum(self.skeleton['frequency'][n])).center(10)}|')
		print(f'{'='*29}')



	def get_boundary(self):
		self.boundary = []
		for n_i in range(self.n-1):
			skeleton_n	= self.skeleton['item'][n_i]
			skeleton_n1 = self.skeleton['item'][n_i+1]
			row_index = {s: i for i, s in enumerate(skeleton_n)}

			n_rows = len(skeleton_n)
			n_cols = len(skeleton_n1)

			b = fmpz_mat(n_rows, n_cols)

			for j, s_n1 in enumerate(skeleton_n1):
				for k in range(len(s_n1)):
					face = s_n1[:k] + s_n1[k+1:]
					i = row_index.get(face)
					if i is not None:
						b[i, j] = b[i, j] + (-1)**k
			
			self.boundary.append(b)
		
		print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} boundary is done.\n')


	def get_boundary_mod2(self):
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

		print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} boundary is done.\n')


	def get_betti(self):
		self.betti = []
		self.betti_norm = []
		rank = []
		for n, B_n in enumerate(self.boundary):
			r = B_n.rank()
			rank.append(r)
			print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} rank of boundary_{n+1}: {r}', flush=True)

		m = len(self.skeleton['item'][0])
		self.betti.append(m - rank[0])
		self.betti_norm.append(
			round((m - rank[0]) / m, 7)
			)

		for n_i in range(self.n-2):
			m = len(self.skeleton['item'][n_i+1])
			self.betti.append(m - rank[n_i] - rank[n_i+1])
			if m > 0:
				self.betti_norm.append(round(self.betti[n_i+1] / m, 7))
			else:
				self.betti_norm.append(0)

		print(textwrap.dedent(f'''
			{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} betti number is done.
			===============================
			|{str('n').center(5)}|{str('betti').center(10)}|{str('normalized').center(12)}|
			|{'-'*5}|{'-'*10}|{'-'*12}|'''))
		for n, b in enumerate(self.betti):
			print(f'|{str(n).center(5)}|{str(b).center(10)}|{str(self.betti_norm[n]).center(12)}|')
		print('===============================')


	def get_betti_mod2(self):
		rank = []
		self.betti = []
		self.betti_norm = []
		for n_i, (coo, n_rows, n_cols) in enumerate(self._boundary_coo):
			r = _rank_mod2(coo, n_rows, n_cols)
			print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} rank of boundary[{n_i+1}] ({n_rows}x{n_cols}) = {r}', flush=True)
			rank.append(r)

		_, _, m = self._boundary_coo[0]
		self.betti.append(m - rank[0])
		self.betti_norm.append((
			(m - rank[0]) / m, 7)
			)


		for n_i in range(self.n-2):
			_, _, m = self._boundary_coo[n_i]
			self.betti.append(m - rank[n_i+1] - rank[n_i])
			if m > 0:
				self.betti_norm.append(round(self.betti[n_i+1] / m, 7))
			else:
				self.betti_norm.append(0)
		
		print(textwrap.dedent(f'''
			{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} betti number is done.
			===============================
			|{str('n').center(5)}|{str('betti').center(10)}|{str('nominalized').center(12)}|
			|{'-'*5}|{'-'*10}|{'-'*12}|'''))
		for n, b in enumerate(self.betti):
			print(f'|{str(n).center(5)}|{str(b).center(10)}|{str(self.betti_norm[n]).center(12)}|')
		print('===============================')