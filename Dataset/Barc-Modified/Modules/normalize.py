import numpy as np


def title_normalize(list_of_titles,min_score,max_score):

	for paper in list_of_titles:
		list_of_titles[paper][1]-=min_score
		list_of_titles[paper][1]/=(max_score - min_score)

	return list_of_titles
	

def abs_normalize(topic_matrix):
	topic_matrix *= 100

	# min_score = np.amin(topic_matrix)

	# max_score = np.amax(topic_matrix)

	# topic_matrix -= min_score
	# topic_matrix /= (max_score - min_score)
	return topic_matrix

