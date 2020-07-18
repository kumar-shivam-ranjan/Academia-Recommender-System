import json
import os
from math import *
import sys

import matplotlib.pylab as plt
from dataset_detect import *
from distribution import *
from paper_result import *
from summarizer import *


def active_dist(topic):
	pass

	## Commented because not needed

	# active_dict = active_distri()
	# # for common graph
	# fig = plt.figure()
	# plt.xlabel('Years', fontsize=10)
	# plt.ylabel('paper count', fontsize=10)
	# plt.xticks(rotation=90)

	# lists = sorted(active_dict[topic[0][1]].items())
	# x,y = zip(*lists)
	# plt.plot(x,y,label=topic[0][1])

	# lists = sorted(active_dict[topic[1][1]].items())
	# x,y = zip(*lists)
	# plt.plot(x,y,label=topic[1][1])

	# lists = sorted(active_dict[topic[2][1]].items())
	# x,y = zip(*lists)
	# plt.plot(x,y,label=topic[2][1])

	# plt.legend()
	# plt.show()

	# fig.suptitle('common_topic', fontsize=20)
	# fig.savefig('./modules/specific/' + 'common_topic.png')


def extract_data():

	top_papers = []

	f = open('./src/AAN/acl-metadata.txt','rb')
	lines=f.readlines()
	papers=[]
	paper=[]
	for line in lines:
		try:
			line = line.decode()
			if line=='\n' or line=='*\n':
				papers.append(paper)
				
				paper=[]
			else:
				try:
					paper.append(line.split('=')[1].rstrip('}\n').lstrip(' {'))
				except:
					pass
					# print(line.split('='))
		except:
			pass
	return papers

def top_authors_and_conferences(top_papers,paper_with_scores):

	data=extract_data()
	author_score={}
	conference_score={}
	for paper in data:
		if (len(paper))==0:
			continue
		if paper[0] in paper_with_scores:
			for authors_list in paper[1].split(','):
				for author in authors_list.split(';'):
					author_name=author.strip()
					if len(author_name) == 0:
						continue
					try:
						if author_name not in author_score:
							author_score[author_name]=paper_with_scores[paper[0]]/(1+log(2018-int(paper[4])+1))
						else:
							author_score[author_name]+=paper_with_scores[paper[0]]/(1+log(2018-int(paper[4])+1))
					except IndexError:
						if author_name not in author_score:
							author_score[author_name]=paper_with_scores[paper[0]]/(1+log(2018-int(paper[3])+1))
						else:
							author_score[author_name]+=paper_with_scores[paper[0]]/(1+log(2018-int(paper[3])+1))
					except:
						pass

	for paper in data:
		if (len(paper))==0:
			continue
		try:
			if paper[0] in top_papers:
				conf_name=paper[3].strip()
				if len(conf_name) == 0:
					continue
				if conf_name not in conference_score:
					conference_score[conf_name]=paper_with_scores[paper[0]]/(1+log(2018-int(paper[4])+1))
				else:
					conference_score[conf_name]+=paper_with_scores[paper[0]]/(1+log(2018-int(paper[4])+1))
		except IndexError:
			if paper[0] in top_papers:
				conf_name=paper[2].strip()
				if len(conf_name) == 0:
					continue
				if conf_name not in conference_score:
					conference_score[conf_name]=paper_with_scores[paper[0]]/(1+log(2018-int(paper[3])+1))
				else:
					conference_score[conf_name]+=paper_with_scores[paper[0]]/(1+log(2018-int(paper[3])+1))
		except:
			pass

	author_score_list=[]
	conf_score_list=[]

	for key, value in author_score.items():
	    temp = [key,value]
	    author_score_list.append(temp)

	for key, value in conference_score.items():
	    temp = [key,value]
	    conf_score_list.append(temp)

	author_score_list.sort(key=lambda x:x[1],reverse=True)
	conf_score_list.sort(key=lambda x:x[1],reverse=True)

	top_authors=[]
	top_conferences=[]

	num_auth = -1
	num_conf = -1
	avg_auth = 0.0
	for author in author_score_list:
		avg_auth += author[1]
	avg_auth /= len(author_score_list)

	summ = 0.0
	for idx, author in enumerate(author_score_list):
		if author[1] < avg_auth:
			num_auth = idx
			break

	avg_conf = 0.0
	for conf in conf_score_list:
		avg_conf += conf[1]
	avg_conf /= len(conf_score_list)

	summ = 0.0
	for idx, conf in enumerate(conf_score_list):
		if conf[1] < avg_conf:
			num_conf = idx
			break
	# print(author_score_list,conf_score_list)

	for i in author_score_list[:num_auth]:
		top_authors.append(i)
	for i in conf_score_list[:num_conf]:
		top_conferences.append(i)

	return top_authors,top_conferences

def top_topics(topic_matrix,idx_to_topic,top_paper,idx_to_paperid,to):
	
	topic_distri = {}
	topic_list = []
	# print(top_paper) 
	# print(idx_to_paperid)

	for row in range(topic_matrix.shape[0]):
		if idx_to_paperid[row].rstrip(".txt") in top_paper:	
			for topic in idx_to_topic:
				if idx_to_topic[topic] in topic_distri:
					topic_distri[idx_to_topic[topic]] += topic_matrix[row,topic]
				else:
					topic_distri[idx_to_topic[topic]] = topic_matrix[row,topic]

	for topic in topic_distri:
		topic_list.append((topic_distri[topic],topic))
	topic_list.sort(reverse=True)
	return topic_distri, topic_list[:to]


def top_result(title,abstract,f):

	to_print = 10

	bound = 60

	idx_to_topic, topic_matrix, idx_to_paperid, top_paper = top_papers(title,abstract)
	# print("No. of paper shortlisted after networks analysis : " + str(len(top_paper)))

	avg = 0.0
	paper_with_scores = dict()
	for paper in top_paper:
		paper_with_scores[paper[1].rstrip('.txt')] = paper[0]
		avg += paper[0]
	avg /= len(paper_with_scores)

	summ = 0.0
	for idx, paper in enumerate(top_paper):
		if paper[0] < avg:
			bound = idx
			break

	top_paper = top_paper[:bound]
	# print("No. of paper shortlisted after Content analysis : " + str(len(top_paper)))



	topicwise = dict()
	confwise = dict()
	yearwise = dict()
	authorwise = dict()

	fil = open('./src/topic_paper.txt','r')
	for line in fil.readlines():
		topicwise[line.split(',')[0]] = line.split(',')[1]
	# print(topicwise)

	data = extract_data()

	for paper in data:
		if len(paper) == 0:
			continue
		if len(paper) == 4:
			yearwise[paper[0]] = paper[3]
			authorwise[paper[0]] = []
			for i in paper[1].split(';'):
				for j in i.split(','):
					authorwise[paper[0]].append(j)
		else:
			yearwise[paper[0]] = paper[4]
			confwise[paper[0]] = paper[3]
			authorwise[paper[0]] = []
			for i in paper[1].split(';'):
				for j in i.split(','):
					authorwise[paper[0]].append(j)



	topicwise_paper = dict()
	confwise_paper = dict()
	authorwise_paper = dict()
	yearwise_paper = dict()

	# print(top_paper)
	for paper in top_paper:
		topic = topicwise[paper[1].split('.')[0]]
		if topic not in topicwise_paper:
			topicwise_paper[topic] = 1.0
		else:
			topicwise_paper[topic] += 1.0

		if paper[1].split('.')[0] in confwise:
			conf = confwise[paper[1].split('.')[0]]
			if conf in confwise_paper:
				confwise_paper[conf] +=1
			else:
				confwise_paper[conf] = 1

		if paper[1].split('.')[0] in yearwise:
			year = yearwise[paper[1].split('.')[0]]
			if year in yearwise_paper:
				yearwise_paper[year] +=1
			else:
				yearwise_paper[year] = 1

		if paper[1].split('.')[0] in authorwise:
			auth = authorwise[paper[1].split('.')[0]]
			for author in auth:
				if author in authorwise_paper:
					authorwise_paper[author] +=1
				else:
					authorwise_paper[author] = 1

	# top_paper = top_papers(title,abstract)[:60]
	top_paper, top_papers_title = [i[1].rstrip('.txt') for i in top_paper], [i[2] for i in top_paper]

	top_authors, top_conf = top_authors_and_conferences(top_paper,paper_with_scores)	

	i = 0
	custom = {}
	for author in top_authors:
		if author[0] in authorwise_paper:
			custom[author[0]] = authorwise_paper[author[0]]
			i+=1
		if i == 10:
			break


	i = 0
	custom = {}
	for conf in top_conf:
		if conf[0] in confwise_paper:
			custom[conf[0]] = confwise_paper[conf[0]]
			i+= 1
		if i == 10:
			break

	_, top_topic_list = top_topics(topic_matrix,idx_to_topic,top_paper,idx_to_paperid,10)

	topic_list = active_area(top_paper,paper_with_scores)
	

	active_dist(topic_list)

	query_result = {}
	query_result['title'] = title
	query_result['abstract'] = abstract
	query_result['top_papers'] = []

	for idx, paper in enumerate(top_papers_title[:to_print]):
		query_result['top_papers'].append(paper + "( " + str(top_paper[idx]) + " ) :" + str(paper_with_scores[top_paper[idx]]))

	query_result['top_authors'] = []

	for idx, author in enumerate(top_authors[:to_print]):
		query_result['top_authors'].append( author[0] + " : " + str(author[1]))
	
	query_result['top_confrences'] = []

	for idx, conf in enumerate(top_conf[:to_print]):
		query_result['top_confrences'].append( conf[0] + " : " + str(conf[1]))	
	
	query_result['active_areas'] = []

	for idx, topic in enumerate(topic_list[:to_print]):
		query_result['active_areas'].append( topic[1][:-1] + " : " + str(topic[0]))

	query_result['top_tags'] = []

	for idx, topic in enumerate(top_topic_list[:to_print]):
		query_result['top_tags'].append( topic[1] + " : " + str(topic[0]))
	
	json.dump(query_result,f)


	# lists = sorted(topicwise_paper.items()) # sorted by key, return a list of tuples
	# x, y = zip(*lists)
	# fig = plt.figure()
	# plt.xticks(rotation=90)
	# plt.xlabel('Topics', fontsize=10)
	# plt.ylabel('paper count', fontsize=10)
	# plt.plot(x, y)
	# plt.show()
	# fig.suptitle('topicwise-paper', fontsize=20)
	# fig.savefig('./modules/specific/' + 'topicwise-paper.png')


	return top_paper, top_papers_title



if not os.path.exists("results"):
	os.makedirs("results")


result_token = ""
if len(sys.argv) == 2:
	result_token = sys.argv[1]

########################################################################################################
#	int code starts here																			   #
########################################################################################################

"""
	This part is for batch input from input.json file
"""

# fil = open("input.json","r")
# papers = json.load(fil)
# fil.close()

# for idx, paper in enumerate(papers):
# 	path1 = "results/result " + str(idx+1) + "/overview.txt"
# 	path2 = "results/result " + str(idx+1) + "/summary.txt"
# 	if not os.path.exists("results/result " + str(idx+1)):
# 		os.makeirs("results/result " + str(idx+1))
# 	# print(paper)
# 	fil = open(path1,"w")
# 	summ = open(path2,"w")
# 	paper_ids = top_result(paper["title"],paper["abstract"],fil)
# 	summarize(paper_ids,summ)
# 	summ.close()
# 	fil.close()
# 	print("[ DONE ]\tresult {}".format(idx+1))


"""
	This part is for one user input
"""

title = "Chinese unknown word identification as known word tagging"
abstract = "This work presents a tagging approach to Chinese unknown word identification based on lexicalized hidden Markov models (LHMMs). In this work, Chinese unknown word identification is represented as a tagging task on a sequence of known words by introducing word-formation patterns and part-of-speech. Based on the lexicalized HMMs, a statistical tagger is further developed to assign each known word an appropriate tag that indicates its pattern in forming a word and the part-of-speech of the formed word. The experimental results on the Peking University corpus indicate that the use of lexicalization technique and the introduction of part-of-speech are helpful to unknown word identification. The experiment on the SIGHAN-PK open test data also shows that our system can achieve state-of-art performance."

# print(extract_data()[0])
# title = "Feature identification of program source code using regular expression"
# abstract = "A software application is a collection of various features that are developed to meet the need of particular purposes. To reduce time to develop and to increase software quality, developers reuse similar features from another software. Before reusing the features, developers need to know what are features in the software. The lack or absence of complete documentation may hinder the process of understanding the features. However the application usually comes with the source code. Reading the source code maybe the only option if the documentation is not found. In this paper, we propose a model to reverse engineering a source code to find information about features in software and its dependency. To find features in the source code, we use regular expressions (regex) to find important elements and their dependencies. A call graph is then generated to help understanding these elements. The model has been implemented and have been validated to several case studies. Finding the features in source code depends entirely on the language of the source code. Our research confirms that customizing the pattern in regex easier than scanning and parsing the language syntax to get the features."

# title = "Semantics and logic of object calculi"
# abstract = "The main contribution of this paper is a formal characterization of recursive object specifications based on a denotational untyped semantics of the object calculus and the discussion of existence of those (recursive) specifications. The semantics is then applied to prove soundness of a programming logic for the object calculus and to suggest possible extensions. For the purposes of this discussion we use an informal logic of predomains in order to avoid any commitment to a particular syntax of specification logic."


inp_file = open("single_input.json","r")
papers = json.load(inp_file)
inp_file.close()

path_result = "result/" + result_token + ".json" 
# path2 = "result/summary.txt"

if not os.path.exists("result"):
	os.makedirs("result")

result_file = open(path_result,"w")
# summ = open(path2,"w")
for idx, paper in enumerate(papers):
	title = paper["title"]
	abstract = paper["abstract"]

paper_ids, titles = top_result(title,abstract,result_file)

# bound_for_summary = 30
# # start = time.clock()
# summary = summarizer(title,abstract,paper_ids[:bound_for_summary])
# print("[ DONE ]\tSummarization\ttime taken : {}".format(time.clock()-start))

# # start = time.clock()
# dataset_involved = detect(5)
# print("[ DONE ]\tDataset Detection Done\ttime taken : {}".format(time.clock()-start))

# write_dataset(fil,dataset_involved)

# text = ""
# for idx, part in enumerate(titles[:bound_for_summary]):
# 	text += "#####\t" + part + "\n\n"
# 	idx = paper_ids[idx]
# 	summary[idx] = summary[idx].replace("\n\n", "")
# 	text += summary[idx].rstrip() + "....\n\n*************\n\n"
# summ.write(text)
# summ.close()

result_file.close()
