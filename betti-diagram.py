import networkx as nx
import plotly.graph_objects as go
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('path', type=str)
	parser.add_argument('n', type=int)

	args = parser.parse_args()
	path = args.path
	n = args.n


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
	pos = nx.spring_layout(G, seed=42, k=0.9)
	fig = go.Figure()

	for u, v in G.edges():
		x0, y0 = pos[u]
		x1, y1 = pos[v]
		fig.add_annotation(
			x=x1, y=y1,
			ax=x0, ay=y0,
			xref='x', yref='y', axref='x', ayref='y',
			showarrow=True,
			arrowhead=0,
			arrowsize=0.5,
			arrowwidth=0.5,
			arrowcolor='grey',
		)

	node_x = [pos[n][0] for n in G.nodes()]
	node_y = [pos[n][1] for n in G.nodes()]
	node_text = [nodes[n]['label'] for n in G.nodes()]
	node_hover = [
		f'{nodes[n]['label']}<br>from: {G.out_degree(n)} / to: {G.in_degree(n)}'
		for n in G.nodes()
	]

	fig.add_trace(go.Scatter(
		x=node_x, y=node_y,
		mode='markers+text',
		marker=dict(size=10, line=dict(width=0)),
		hovertext=node_hover, hoverinfo='text',
	))

	fig.update_layout(
		showlegend=False,
		margin=dict(l=20, r=20, t=40, b=20),
		xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
		yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
				scaleanchor='x', scaleratio=1),
		plot_bgcolor='white', hovermode='closest',
	)
