from collections import Counter
from datetime import datetime
import networkx as nx
import plotly.graph_objects as go
from itertools import combinations
from flint import fmpz_mat
from datasets import load_dataset
import numpy as np
import itertools, math, random, re, stanza, textwrap



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
		docs = stanza.Document([], text=self.text)
		parsed_docs = self.parser(docs)
		for snt in parsed_docs.sentences:
			self.parsed_sentences.append(
				tuple(
					w.text for w in snt.words
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


	def parse_to_monkey_word(self, seed:int=42):
		docs = stanza.Document([], text=self.text)
		parsed_docs = self.parser(docs)
		random.seed(seed)
		words = []
		for snt in parsed_docs.sentences:
			words += [w.text for w in snt.words]

		num_snt = len(self.text)
		total = len(words) + num_snt

		word_counter = Counter(words)
		set_words = sorted(word_counter)
		dict_words = word_counter
		items = list(dict_words.keys())
		prob = list(dict_words.values())
		monkey_text = random.choices(
			items,
			weights=prob,
			k=total
		)

		self.parsed_sentences = []
		indice_snt = sorted(random.sample(range(total), num_snt))
		cnt = 0
		for sep in indice_snt:
			self.parsed_sentences.append(tuple(monkey_text[cnt:sep]))
			cnt = sep + 1
		
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


	def parse_to_monkey_chr(self, seed:int=42):
		text = ''.join(self.text)
		num_snt = len(self.text)
		total = len(text) + num_snt
		random.seed(seed)

		set_chr = sorted(set(text))
		dict_chr = {}
		for c in set_chr:
			dict_chr[c] = text.count(c)
		items = list(dict_chr.keys())
		prob = list(dict_chr.values())
		monkey_text = random.choices(
			items,
			weights=prob,
			k=total
		)

		indice_snt = random.sample(range(total), num_snt)
		for i in indice_snt:
			monkey_text[i] = '[snt]'
		monkey_text = ''.join(monkey_text)
		monkey_text = re.sub(r'(\[snt\])+', r'\1', monkey_text)
		monkey_text = re.sub(r'(\s)+', r'\1', monkey_text)

		self.parsed_sentences = [snt for snt in monkey_text.split('[snt]')]

		print(textwrap.dedent(f'''
		{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} parsing into word is done.
		{'='*50}
		text source:		{self.path}
		language:		{self.lang}
		length			{len(self.parsed_sentences)}
		{'='*50}
		'''))


	def parse_to_upos(self):
		self.parsed_sentences = []
		docs = stanza.Document([], text=self.text)
		parsed_docs = self.parser(docs)
		for snt in parsed_docs.sentences:
			self.parsed_sentences.append(
				tuple(
					w.upos for w in snt.words
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
	def __init__(self, wiki_config:str, lang:str, batch:int, seed:int=42):
		self.wiki_config = wiki_config
		self.lang = lang
		self.parser	= stanza.Pipeline(
			self.lang,
			processors='tokenize,pos',
			tokenize_no_ssplit=True,
			use_gpu=True
			)
		random.seed(seed)


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
		docs = stanza.Document([], text=self.sentences)
		parsed_docs = self.parser(docs)
		for snt in parsed_docs.sentences:
			self.parsed_sentences.append(
				tuple(
					w.text for w in snt.words
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
		docs = stanza.Document([], text=self.sentences)
		parsed_docs = self.parser(docs)
		for snt in parsed_docs.sentences:
			self.parsed_sentences.append(
				tuple(
					w.upos for w in snt.words
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
				for i in range(len(snt)-n_i+1):
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
				self.betti_norm.append(
					round((self.betti[n_i+1] / m), 7)
					)
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
			r = self._rank_mod2(coo, n_rows, n_cols)
			print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} rank of boundary[{n_i+1}] ({n_rows}x{n_cols}) = {r}', flush=True)
			rank.append(r)

		_, m, _ = self._boundary_coo[0]
		self.betti.append(m - rank[0])
		self.betti_norm.append(
			round((m - rank[0]) / m, 7)
			)


		for n_i in range(self.n-2):
			_, _, m = self._boundary_coo[n_i]
			self.betti.append(m - rank[n_i+1] - rank[n_i])
			if m > 0:
				self.betti_norm.append(
					round((self.betti[n_i+1] / m), 7)
					)
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


	def _rank_mod2(self, coo, n_rows, n_cols):
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
	

class Network:
	def __init__(self, text_path:str):
		with open(text_path, 'r') as f:
			self.text = f.read()
		self.G = nx.DiGraph()

	def draw_network_1(self, title:str='network', save_path:str='network-1', save:bool=False, dont_show:bool=False):
		initial_nodes = sorted(set(self.text))
		initial_edges = sorted(set([(self.text[i], self.text[i+1]) for i in range(len(self.text)-1)]))
		self.skeleta = [''.join(edge) for edge in initial_edges]

		for node in initial_nodes:
			self.G.add_node(node, **{'label':node})
		self.G.add_edges_from(initial_edges)
		position = nx.spring_layout(self.G, seed=42, k=0.8)

		bidir_count = {
			node: sum(1 for v in self.G.successors(node) if self.G.has_edge(v, node))
			for node in self.G.nodes()
		}


		edge_x, edge_y = [], []
		for u, v in self.G.edges():
			x0, y0 = position[u]
			x1, y1 = position[v]
			edge_x += [x0, x1, None]
			edge_y += [y0, y1, None]

		edge_trace = go.Scatter(
			x=edge_x, y=edge_y,
			mode="lines",
			line=dict(width=0.5, color='grey'),
			hoverinfo="none",
		)

		node_x = [position[node][0] for node in self.G.nodes()]
		node_y = [position[node][1] for node in self.G.nodes()]
		node_text = [node if node != '\n' else '\\n' for node in self.G.nodes()]
		# ホバー時に出る詳細（次数なども入れられる）
		node_hover = [
			f'{node}<br>from: {self.G.out_degree(node)} / to: {self.G.in_degree(node)} / bd: {bidir_count[node]}'
			if node != '\n' 
			else f'\\n<br>from: {self.G.out_degree(node)} / to: {self.G.in_degree(node)} / bd: {bidir_count[node]}'
			for node in self.G.nodes()
		]

		node_trace = go.Scatter(
		x=node_x, y=node_y,
		mode="markers+text",          # マーカー + 常時表示ラベル
		marker=dict(
			size=5,
			line=dict(width=0.5),
			color='#636efa'),
		text=node_text,               # マーカー脇に出る固定ラベル
		textposition="top center",
		textfont=dict(size=13),
		hovertext=node_hover,         # ホバーで出る詳細
		hoverinfo="text")

		# --- 図の組み立て ---
		fig = go.Figure(data=[edge_trace, node_trace])
		fig.update_layout(
			showlegend=False,
			margin=dict(l=20, r=20, t=40, b=20),
			xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
			yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
					scaleanchor="x", scaleratio=1),  # アスペクト比を固定
			plot_bgcolor="white",
			hovermode="closest",
			title=title
		)

		fig.add_annotation(
				text=(
					f'n:       1<br>'
					f'nodes:   {len(self.G.nodes)}<br>'
					f'edges:   {len(self.G.edges)}<br>'
				),
				xref='paper', yref='paper',
				x=0.01, y=0.99,
				xanchor='left', yanchor='top',
				showarrow=False,
				align='left',
				font=dict(size=13, color='black'),
				bgcolor='rgba(255,255,255,0.8)',
				bordercolor='grey', borderwidth=1, borderpad=6,
			)
		
		if save:
			fig.write_html(f'{save_path}-1.html', include_plotlyjs='cdn')
			print(f'n=1: : saved to {save_path}-1.html ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

		if not dont_show:
			fig.show()



	def draw_network_n(self, n, title:str='network', save_path:str='network-', save:bool=False, dont_show:bool=False):
		if n < 2:
			print('n is too small.\nIt must be greater than or eualt to 2.')
		
		else:
			for n_i in range(3, n+2):
				previous_skeleta = self.skeleta

				ngrams = sorted(
					set(
						[self.text[i:i+n_i] for i in range(len(self.text)-n_i+1)]
					)
				)

				new_nodes = []
				new_edges = []
				self.skeleta = []
				for ngram in ngrams:
					sub_gram = [ngram[:k] + ngram[k+1:] for k in range(n_i)]
					if all(x in set(previous_skeleta) for x in sub_gram):
						new_nodes += [g for g in ngram]
						new_edges += [c for c in combinations(ngram, 2)]
						self.skeleta.append(ngram)
				new_nodes = sorted(set(new_nodes))
				new_edges = sorted(set(new_edges))
				self.skeleta = sorted(set(self.skeleta))


				self.G = nx.DiGraph()
				for new_node in new_nodes:
					self.G.add_node(new_node, **{'label':new_node})
				self.G.add_edges_from(new_edges)
				position = nx.spring_layout(self.G, seed=42, k=0.8)

				if not self.G.nodes():
					print(f'n_i={n_i}: no valid simplices found, process terminated.')
					break

				bidir_count = {
					node: sum(1 for v in self.G.successors(node) if self.G.has_edge(v, node))
					for node in self.G.nodes()
				}


				edge_x, edge_y = [], []
				for u, v in self.G.edges():
					x0, y0 = position[u]
					x1, y1 = position[v]
					edge_x += [x0, x1, None]   # None で線を分割
					edge_y += [y0, y1, None]

				edge_trace = go.Scatter(
					x=edge_x, y=edge_y,
					mode="lines",
					line=dict(width=0.5, color='grey'),
					hoverinfo="none",
				)

				node_x = [position[node][0] for node in self.G.nodes()]
				node_y = [position[node][1] for node in self.G.nodes()]
				node_text = [node if node != '\n' else '\\n' for node in self.G.nodes()]
				# ホバー時に出る詳細（次数なども入れられる）
				node_hover = [
					f'{node}<br>from: {self.G.out_degree(node)} / to: {self.G.in_degree(node)} / bd: {bidir_count[node]}'
					if node != '\n'
					else f'\\n<br>from: {self.G.out_degree(node)} / to: {self.G.in_degree(node)} / bd: {bidir_count[node]}'
					for node in self.G.nodes()
				]

				node_trace = go.Scatter(
				x=node_x, y=node_y,
				mode="markers+text",          # マーカー + 常時表示ラベル
				marker=dict(
					size=5,
					line=dict(width=0.5),
					color='#636efa'),
				text=node_text,               # マーカー脇に出る固定ラベル
				textposition="top center",
				textfont=dict(size=13),
				hovertext=node_hover,         # ホバーで出る詳細
				hoverinfo="text")

				# --- 図の組み立て ---
				fig = go.Figure(data=[edge_trace, node_trace])
				fig.update_layout(
					showlegend=False,
					margin=dict(l=20, r=20, t=40, b=20),
					xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
					yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
							scaleanchor="x", scaleratio=1),  # アスペクト比を固定
					plot_bgcolor="white",
					hovermode="closest",
					title=title
				)

				fig.add_annotation(
						text=(
							f'n:       {n_i-1}<br>'
							f'nodes:   {len(self.G.nodes)}<br>'
							f'edges:   {len(self.G.edges)}<br>'
							f'skeleta: {len(self.skeleta)}'
						),
						xref='paper', yref='paper',
						x=0.01, y=0.99,
						xanchor='left', yanchor='top',
						showarrow=False,
						align='left',
						font=dict(size=13, color='black'),
						bgcolor='rgba(255,255,255,0.8)',
						bordercolor='grey', borderwidth=1, borderpad=6,
					)


				if save:
					fig.write_html(f'{save_path}-{n_i-1}.html', include_plotlyjs='cdn')
					print(f'n={n_i-1}: saved to {save_path}-{n_i-1}.html ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
					

				if not dont_show:
					fig.show()
