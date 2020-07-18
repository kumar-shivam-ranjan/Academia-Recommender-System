from sensim import *
from cosine import *
from normalize import *
from wordnet import *
from graph_shortlist import *
import numpy as np

def preprocess(topics):
	f=open('./../src/AAN/paper_ids.txt','r')


	list_of_papers = f.readlines()
	paper_to_topic = {}

	included_paper = shortlist()

	for paper in list_of_papers:
		paper_title = paper.split('\t')[1]
		paper_id = paper.split('\t')[0]
		if paper_id in included_paper:
			np_scores = np.zeros(len(topics))
			for idx, topic in enumerate(topics):
				score = sentence_similarity(topic,paper_title)
				score += cosine_similarity(topic,paper_title)
				score/=2
				np_scores[idx] = score
			paper_to_topic[paper_id] = topics[np_scores.argmax()]

	fil = open('./../src/topic_paper.txt',"w")
	for paper in paper_to_topic:
		fil.write(paper+","+paper_to_topic[paper]+"\n")
	fil.close()

# title = "citation recommendation without author supervision"
# titlesim(title)
topics = []
for topic in open('./../src/nlp_topics.txt',"r").readlines():
	topics.append(topic.strip(' \n'))
preprocess(topics)