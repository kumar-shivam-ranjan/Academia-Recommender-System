import json
from paper_result import *

def detect(top_count=3):
    datasets = open('./src/datasetlist.txt')
    useful_datasets = []
    for dataset in datasets.readlines():
        _, _, _, combined_score = top_papers(dataset,dataset)
        score = 0.0
        for rate in combined_score:
            score += rate[0]
        useful_datasets.append((score,dataset))

    useful_datasets.sort()
    return useful_datasets[:top_count]


def write_dataset(fil, dataset_involved):
    fil.write("\n\n")
    fil.write("Dataset found are:\n")
    for _,dataset in enumerate(dataset_involved):
        fil.write("\t{}. {} : {}\n".format(_+1,dataset[1],dataset[0]))