import networkx as nx
import plotly.graph_objects as go
import argparse, json


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('path',
						type=str,
						help='[str] the file path of the target text')
	parser.add_argument('--save_name',
						type=str,
						default='betti-diagram',
						help='[str | default="betti-diagram"] the file name for saving the diagram (an extension (.html) will be added automatically)')
	parser.add_argument('--dont_show',
					 	action='store_false',
						help='[bool | default=True] will not show the diagram immediately')

	args = parser.parse_args()
	path = args.path
	save_name = args.save_name
	dont_show = args.dont_show


	with open(path, 'r', encoding='utf-8') as f:
		text = f.read()
		alphabets = sorted(set(text))
		bigrams = sorted(set([text[i:i+2] for i in range(len(text)-1)]))
	
	nodes = {}
	for chr in alphabets:
		nodes[chr] = {'label':chr}
	edges = [(pair[0], pair[1]) for pair in bigrams]


	G = nx.DiGraph()
	for nid, attr in nodes.items():
		G.add_node(nid, **attr)
	G.add_edges_from(edges)
	pos = nx.spring_layout(G, seed=42, k=0.8)


	edge_x, edge_y = [], []
	for u, v in G.edges():
		x0, y0 = pos[u]
		x1, y1 = pos[v]
		edge_x += [x0, x1, None]   # None で線を分割
		edge_y += [y0, y1, None]

	edge_trace = go.Scatter(
		x=edge_x, y=edge_y,
		mode="lines",
		line=dict(width=0.5, color='grey'),
		hoverinfo="none",
	)


	node_x = [pos[n][0] for n in G.nodes()]
	node_y = [pos[n][1] for n in G.nodes()]
	node_text = [nodes[n]["label"] for n in G.nodes()]
	node_hover = [
		f'{nodes[n]['label']}<br>from: {G.out_degree(n)} / to: {G.in_degree(n)}'
		for n in G.nodes()
	]

	node_trace = go.Scatter(
		x=node_x, y=node_y,
		mode="markers+text",
		marker=dict(size=5,
					line=dict(width=0.5),
					color='#636efa'),
		text=node_text,
		textposition='top center',
		textfont=dict(size=13),
		hovertext=node_hover,
		hoverinfo='text'
		)


	fig = go.Figure(data=[edge_trace, node_trace])
	fig.update_layout(
		showlegend=False,
		margin=dict(l=20, r=20, t=40, b=20),
		xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
		yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
				scaleanchor='x', scaleratio=1),  # アスペクト比を固定
		plot_bgcolor='white',
		hovermode='closest',
	)

	fig.write_html(f'{save_name}.html', include_plotlyjs='cdn')
	if dont_show:
		fig.show()
