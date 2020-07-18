from abstractsim import *
import numpy as np
from paper_result import *

def year_distri():
    # For Year wise distribution of papers
    fil = open('./../src/acl-metadata.txt','rb')

    year_distri = {}
    for line in fil.readlines():
        try:
            line = line.decode()
            # print(line)
            if len(line.split()) != 0 and line.split()[0] == 'year':
                year_distri[line.split()[2][1:-1]] = 1 if line.split()[2][1:-1] not in year_distri else year_distri[line.split()[2][1:-1]]+1
        except:
            # print("year : {}".format(line))
            pass
    fil.close()
    return year_distri

def author_distri():
    # For Authorwise Paper distribution
    author_distri = {}
    mfil = open('./../src/author_ids.txt','r')
    author_ids = {}
    for author in mfil.readlines():
        ids, name = author.split("\t")
        author_ids[name] = ids

    fil = open('./../src/acl-metadata.txt','rb')
    for line in fil.readlines():
        try:
            line = line.decode().split()
            if len(line) != 0 and line[0] == 'author':
                line = line[2][1:-1].split(";")
                for auth in line:
                    author_distri[auth] = 1 if auth not in author_distri else author_distri[auth]+1
        except:
            pass
    return author_distri

def top_tags():
    # Topicwise paper distribution 
    idx_to_topic, _,topic_matrix = alterabstractsim(200)
    topic_distri = {}
    for idx in range(topic_matrix.shape[1]):
        topic_distri[idx_to_topic[idx]] = topic_matrix.sum(axis=0)[idx]
    return topic_distri

def active_distri():
    data = extract_data()
    fil = open('./src/topic_paper.txt','r')
    topic_distri = dict()
    
    paper_year = dict()
    for paper in data:
        if len(paper) > 0 :
            if len(paper) == 5:
                paper_year[paper[0]] = paper[4]
            else:
                paper_year[paper[0]] = paper[3]
                
    for line in fil.readlines():
        paper_id = line.split(',')[0]
        if paper_id not in paper_year:
            continue
        year = paper_year[paper_id]
        topic = line.split(',')[1]
        if topic not in topic_distri:
            topic_distri[topic] = dict()
        if year not in topic_distri[topic]:
            topic_distri[topic][year] = 1.0
        else:
            topic_distri[topic][year] += 1.0
    return topic_distri
