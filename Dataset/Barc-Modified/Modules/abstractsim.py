from sklearn.feature_extraction.text import TfidfVectorizer
import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize,sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import pickle as pl
import re

from graph_shortlist import *

# abstract given by researcher x
abstract = """Automatic recommendation of citations for a manuscript is
highly valuable for scholarly activities since it can substantially improve the efficiency and quality of literature search.
The prior techniques placed a considerable burden on users,
who were required to provide a representative bibliography
or to mark passages where citations are needed. In this
paper we present a system that considerably reduces this
burden: a user simply inputs a query manuscript (without
a bibliography) and our system automatically finds locations where citations are needed. We show that the naı̈ve
approaches do not work well due to massive noise in the document corpus. We produce a successful approach by carefully examining the relevance between segments in a query
manuscript and the representative segments extracted from
a document corpus. An extensive empirical evaluation using
the CiteSeerX data set shows that our approach is effective."""

def word_token(s):	
	word = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",s)
	return word

def sent_token(s):
	sent = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', s)
	return sent

def preprocess(text):
	"""
	For stemming and removing stop words
	"""
	result = ""
	stemmer = SnowballStemmer('english')
	for word in word_token(text):
		if word not in stopwords.words('english'):
			result += stemmer.stem(word)+" "
	return result.rstrip()

def abstractsim(to):
	""""
	By Using Tf-IDF 
	"""
	# For Abstract similarity 
	f = open('./src/gist.json','r')
	text_files = json.load(f)
	stemmer = SnowballStemmer('english')
	documents = []
	new_abs = ""
	for word in word_token(abstract):
		if word not in stopwords.words('english'):
			new_abs+= stemmer.stem(word)+" "
	documents.append(new_abs)
	for i,paper in enumerate(text_files):
		text = paper['abstract']
		new_text = ""
		for word in word_token(text):
			if word.lower() not in stopwords.words('english'):
				new_text+= stemmer.stem(word)+" "
		documents.append(new_text)
		if i==to:
			break
	print("documents done")
	tfidf = TfidfVectorizer().fit_transform(documents)
	pairwise_similarity = tfidf * tfidf.T

	scores = {}
	for i in range(len(documents)-1):
		scores[text_files[i]['id']] = pairwise_similarity[0,i+1]
	# id_list = []
	# for i in range(len(documents)-2,-1,-1):
	# 	id_list.append(text_files[scores[i-1][1]]['id'])
	return scores


def alterabstractsim(to):
	"""
	For abstract similarity using lda method
	"""
	f = open('./src/gist.json','r')
	text_files = json.load(f)
	documents = []
	# documents.append(abstract)
	included_paper = shortlist()
	idx_to_paper = {}
	i = 0
	for idx,paper in enumerate(text_files):
		if paper['id'].split('.')[0] in included_paper:
			text = paper['abstract']
			documents.append(text)
			idx_to_paper[i] = paper['id']
			i+=1
			if i == to:
				break
	index = 0
	topic_to_idx = {}
	doc_to_topic = {}
	idx_to_topic = {}
	doc_to_topicscore = {}
	for paper in documents:
		n_features = 500
		tf_vectorizer = CountVectorizer(max_features=n_features,
		                                stop_words='english')
		tf = tf_vectorizer.fit_transform(sent_token(paper))
		tf_feature_names = tf_vectorizer.get_feature_names()
		lda = LatentDirichletAllocation(n_components=50, max_iter=5,
		                                learning_method='online',
		                                learning_offset=50.,
		                                random_state=0)
		doc_to_topic[paper] = []
		lda.fit(tf)
		n_top_words = 30
		doc_to_topicscore[paper] = {}
		for topic in lda.components_:
			# topic_to_idx[" ".join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]])] = index
			# doc_to_topic[paper].append(" ".join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]]))
			# index += 1
			topic_list = [preprocess(tf_feature_names[i]) for i in topic.argsort()[:-n_top_words-1:-1]]
			topic_score = 0.0
			for i in topic.argsort()[:-n_top_words-1:-1]:
				topic_score += topic[i]
			topic_score /= 100

			for wordtopic in topic_list:
				if wordtopic not in topic_to_idx:
					topic_to_idx[wordtopic] = index
					idx_to_topic[index] = wordtopic
					index+=1 
					# print(tf_feature_names[wordtopic])
				doc_to_topic[paper].append(wordtopic)
				if wordtopic not in doc_to_topicscore[paper]:
					doc_to_topicscore[paper][wordtopic] = topic_score

			# topic_orginal = " ".join(topic_list)
			# if topic_orginal not in doc_to_topicscore[paper]:
			# 	doc_to_topicscore[paper][topic_orginal] = topic_score
			# if topic_orginal not in topic_to_idx:
			# 	topic_to_idx[topic_orginal] = index
			# 	index += 1
			# doc_to_topic[paper].append(topic_orginal)
	topic_matrix = np.zeros((len(documents),len(topic_to_idx)))
	for idx,paper in enumerate(documents):
		for topic in topic_to_idx:
			if topic in doc_to_topic[paper]:
				topic_matrix[idx][topic_to_idx[topic]] += doc_to_topicscore[paper][topic]
	print(topic_matrix)
	# print(idx_to_topic)
	# print(idx_to_paper)
	with open('idx_to_topic.pkl', 'wb') as output:
	    pl.dump(idx_to_topic, output)
	with open('idx_to_paper.pkl', 'wb') as output:
	    pl.dump(idx_to_paper, output)
	with open('topic_matrix.pkl', 'wb') as output:
	    pl.dump(topic_matrix, output)
	# return idx_to_topic, idx_to_paper, topic_matrix