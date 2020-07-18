import textract 
import nltk
from nltk.corpus import stopwords
from tika import parser
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import PorterStemmer
import math
from stop_words import get_stop_words
from gensim import models,corpora
import numpy as np
import json 


def preprocess(content):
	to_return = []
	stemmer = PorterStemmer()
	print
	for line in sent_tokenize(content):
		words = [stemmer.stem(i) for i in word_tokenize(line)]
		to_return.append(words)
	return to_return
	
	

def tf_idf_transform(content):

	word_to_idx={}
	idx=0

	sentences = preprocess(content)

	#creating word_to_idx dictionary
	for sentence in sentences:
		for word in sentence:
			if word not in word_to_idx:
				word_to_idx[word]=idx
				idx+=1
	#storing 
	dim2=(len(word_to_idx.keys()))

	idf_score=np.zeros(dim2,dtype=np.float64)
	matrix=np.zeros((len(sentences),dim2),dtype=np.float64)
	
	
	for i in range(len(sentences)):

		word_sent=set()

		for word in sentences[i]: #calculate how many times a word appears in a sentence
			matrix[i][word_to_idx[word]]+=1
			word_sent.add(word)

		for word in word_sent:
			idf_score[word_to_idx[word]]+=1 #calculate in how many sentence a word appears

	# print(idf_score)
	idf_score=np.log(float(len(sentences))/idf_score) #calculate idf score

	# print(matrix)

	for i in range(matrix.shape[0]):

		matrix[i]/=float(np.sum(matrix[i]))#normalise
		matrix[i]=np.dot(matrix[i],idf_score) #compute tf-idf score for each word in each sentence

	return matrix


def lsa_summarizer(content):
	#Gong and Liu's approach
	summ_set=set()

	sentences = []
	for line in sent_tokenize(content):
		sentences.append(line)
	reqd_size=int(0.3*len(sentences))

	matrix=tf_idf_transform(content)
	

	u,s,v=np.linalg.svd(matrix)
	i=0
	while len(summ_set)<reqd_size and i<u.shape[1]:
		idx=0
		val=u[0][i]

		for j in range(len(sentences)):
			if u[j][i]>val:
				val=u[j][i]
				idx=j
		summ_set.add(idx)
		i+=1


	summary = ""
	for sent in summ_set:
		summary += sentences[sent]+" "
	return summary

# def summarizer(name,f):
# 	text = ""
# 	abstract = 0
# 	stemmer = PorterStemmer()
# 	for sentence in f.readlines():
# 		sentence=sentence.rstrip('\n')
# 		#print(sentence)
# 		if abstract and len(sentence) >0:
# 			text+=sentence + " "
# 		elif stemmer.stem(sentence.lower()) == stemmer.stem(name) and abstract==0:
# 			abstract=1
# 		if len(sentence)>0 and sentence == sentence.upper() and abstract==1 and \
# 			stemmer.stem(sentence.lower())!=stemmer.stem(name):
# 			break
# 	return lsa_summarizer(text)

def summarize(paper_ids, f):
	summary = [] 

	file_list = json.load(open("./src/gist.json"))
	for file in file_list:
		if file['id'].split('.')[0] in paper_ids:
			summary.append(lsa_summarizer(file['abstract']))

	for line in summary:
		f.write(line)
		f.write("\n\n")


# file = '4.txt'#'A00-1001.txt'
# path = './dataset/citation/'#'./dataset/2014/papers_text/'

# text = """This work presents a tagging approach to Chinese unknown word identification based on lexicalized hidden Markov models (LHMMs). In this work, Chinese unknown word identification is represented as a tagging task on a sequence of known words by introducing word-formation patterns and part-of-speech. Based on the lexicalized HMMs, a statistical tagger is further developed to assign each known word an appropriate tag that indicates its pattern in forming a word and the part-of-speech of the formed word. The experimental results on the Peking University corpus indicate that the use of lexicalization technique and the introduction of part-of-speech are helpful to unknown word identification. The experiment on the SIGHAN-PK open test data also shows that our system can achieve state-of-art performance."""

# f = open(path+file,'r')
# # output = summarizer('abstract',f)
# output = lsa_summarizer(text)
# f.close()
# f = open('output.txt','w')
# f.write(output)
# f.close()
