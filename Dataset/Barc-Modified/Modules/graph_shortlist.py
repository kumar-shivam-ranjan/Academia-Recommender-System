def shortlist():
	f = open('./src/graph_scores.txt','r')
	papers = f.readlines()
	scores=[0 for j in range(len(papers))]
	avg=[0 for i in range(4)]
	for idx,paper in enumerate(papers):

		
		scores[idx]= [paper.split(',')[0]]+list(map(float,paper.rstrip('\n').split(',')[1:]))
		for i in range(4):
			avg[i]+=scores[idx][i+1]

	for i in range(4):
		avg[i]/=len(papers)

	ret = []

	for i in range(len(scores)):
		for j in range(1,5):
			if scores[i][j]>avg[j-1]:
				ret.append(scores[i][0])
				break
	return ret

