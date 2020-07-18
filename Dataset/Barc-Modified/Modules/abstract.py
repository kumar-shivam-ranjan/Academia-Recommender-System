import os
import json
from nltk.stem.snowball import SnowballStemmer
import re

name = 'abstract'
filename = 'gist.json'
endname = 'introduction'

def maker(path):
	full =[]
	coutner = 1
	for file in os.listdir(path):
		each = {}
		each['id'] = file
		text = ""
		f = open(path+file,'r')
		stemmer = SnowballStemmer('english')
		start = 0
		for line in f.readlines():
			orgi = line
			line = line.strip('\n')
			line = line.replace(" ","")
			line = re.sub('\d','',line)
			if start == 0 and stemmer.stem(line.lower()) == stemmer.stem(name):
				start =1
				text += orgi + "\n"
			elif start == 1 and stemmer.stem(line.lower()) == stemmer.stem(endname):
				break
			elif start == 1:
				text += orgi + "\n"
		if len(text) !=0:
			coutner+=1;
			each[name] = text
			full.append(each)
	full.sort(key = lambda x:x['id'])
	with open(filename,'w') as out:
		json.dump(full,out,indent=4)

maker('./papers_text/')



