import networkx as nx


def compute_graph_scores():
	f = open('paper_citation_network.txt','r')
	gs = open('graph_scores.txt','w')
	citations = f.readlines()
	edges = []
	for citation in citations:
		papers = citation.split('==>')
		papers[0]=papers[0].rstrip(' ')
		papers[1]=papers[1].rstrip('\n')
		papers[1]=papers[1].lstrip(' ')
		edges.append(papers)

	G = nx.DiGraph()
	G.add_edges_from(edges)

	cc = nx.closeness_centrality(G)
	bc = nx.betweenness_centrality(G)
	eg = nx.eigenvector_centrality(G,max_iter=1000)
	ig = nx.in_degree_centrality(G)
	
	for i in cc.keys():
		gs.write(i+','+str(cc[i])+','+str(bc[i])+','+str(eg[i])+','+str(ig[i])+'\n')
	gs.close()
	f.close()

compute_graph_scores()

