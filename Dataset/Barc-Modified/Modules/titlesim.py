from sensim import *
from cosine import *
from normalize import *
from wordnet import *
from graph_shortlist import *


# print("Hello Researcher X, Please Enter a title : ")
# title =input()
def titlesim(title, check = []):
	f=open('./src/AAN/paper_ids.txt','r')


	list_of_papers = f.readlines()
	list_of_titles = {}
	min_score = 1000
	max_score = -1

	included_paper = shortlist()

	for paper in list_of_papers:
		paper_title = paper.split('\t')[1]
		paper_id = paper.split('\t')[0]
		if paper_id in included_paper:
			if len(check)==0 or paper_id in check:
				try:
					score = sentence_similarity(title,paper_title)
					if len(check) == 0:
						score += cosine_similarity(title,paper_title)
						score/=2
					if score >= max_score:
						max_score = score
					if score <= min_score:
						min_score = score
					list_of_titles[paper.split('\t')[0]+".txt"]  = [paper_title,score]
				except ZeroDivisionError:
					pass

	# To normalize title similarity scores
	list_of_titles = title_normalize(list_of_titles,min_score,max_score)

	return list_of_titles

# title = "citation recommendation without author supervision"
# titlesim(title)