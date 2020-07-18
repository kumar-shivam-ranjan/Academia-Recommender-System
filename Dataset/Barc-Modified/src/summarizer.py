import textract 
import nltk
from nltk.corpus import stopwords
from tika import parser
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import PorterStemmer
import math
from stop_words import get_stop_words
from gensim import models,corpora

# list containing names of all the pdf files 

l=['4.pdf','5.pdf','6.pdf','06970192.pdf','autocitation.pdf',
'bethard_2010_cikm_literature_search.pdf','db10680a9f29413319561f21134557907b9b.pdf',
'frp0261-ren.pdf','p361-liu.pdf','p371-huang.pdf','p957-he.pdf','p990-tang.pdf',
'p2017-lu.pdf','PAKDD09-Tang-Zhang-citesug (1).pdf']

keywords_set=set()
word_count={}
papers={}
total_count_of_papers = 0
total_count_of_sent = 0
sent_count={}

"""# for LDA 
dictionary = corpora.Dictionary()"""

# for each file

for file in l:

    """# stemmer used in LDA
    lda_stem = PorterStemmer()"""

    total_count_of_papers+=1
    
    # commented because of problem in textract 
    filename = file.rstrip('.pdf')+'.txt'
    #print(filename)
    #f=open(filename,'w',encoding='utf8')
    #print(f)
    #f.write(textract.process(file,encoding='utf8').decode())
    #f.write(parser.from_file(file).decode())
    #f.close()
    f=open(filename,'r')
    keyword=0
    content=f.readlines()
    for sentence in content:
        total_count_of_sent+=1
        sentence=sentence.rstrip('\n')
        if keyword:
            keywords=sentence.split(',')
            uniq_word = set()
            for keyword in keywords:
                keyword = keyword.split(';')
                for key in keyword:
                    word = key.split(' ')
                    for a in word:
                        a = a.rstrip(' ')
                        a = a.lstrip(' ')
                        keywords_set.add(a.lower())
                        if a not in word_count:
                            word_count[a.lower()]=1
                        else:
                            word_count[a.lower()]+=1
                        if file not in papers:
                            papers[file]={}
                        if a.lower() not in papers[file]:
                            papers[file][a.lower()]=1
                        uniq_word.add(a)
            for i,j in enumerate(uniq_word):
                if j not in sent_count:
                    sent_count[j]=1.0
                else:
                    sent_count[j]+=1.0
            break

        if sentence.lower()=='keywords':
            keyword=1
    f.close()

# tf-idf calculation 

tf_values={}

for word in word_count:
    """word_present=0.0
    for paper in papers:
        if word in papers[paper]:
            word_present += 1.0"""
    if word in sent_count and total_count_of_sent != sent_count[word]:
        tf_values[word] = word_count[word] * (math.log(total_count_of_sent/sent_count[word]))


output = open('output.txt','w')


# abstract summarization of 4.pdf
def summarizer(name,file):
    filename = file.rstrip('.pdf')+'.txt'
    f=open(filename,'r')
    abstract=0
    text = ""
    stemmer = PorterStemmer()

    # for abstract extraction
    for sentence in f.readlines():
        sentence=sentence.rstrip('\n')
        if abstract and len(sentence) >0:
            text+=sentence+"\n"
        elif stemmer.stem(sentence.lower()) == stemmer.stem(name) and abstract==0:
            abstract=1
        if len(sentence)>0 and sentence == sentence.upper() and abstract==1 and \
            stemmer.stem(sentence.lower())!=stemmer.stem(name):
            break
    content = sent_tokenize(text)
    content.pop()

    scores = []
    avg_score = 0.0
    for sent in content:
        score=0.0
        for word in sent.split():
            if word.lower() in tf_values:
                score+=tf_values[word.lower()]
        scores.append(score)
        #print("for",sent,"score :",score)
        avg_score+=score
    #print(tf_values["Citation".lower()])
    try:
        avg_score/=len(content)
    except:
        print("file can't used ")
        return
    #print(avg_score)
    summary=""
    for i,j in enumerate(scores):
        if j>=avg_score:
            summary+=content[i]
    final_summary="By TF-IDF\n"
    final_summary+=name.upper()+" "+"Summary: \n"+" "+summary+"\n"
    final_summary+="\tOriginal "+name+" : "+str(len(text))+" chars\n"
    final_summary+="\tReduced Size : "+str(len(summary))+" chars\n"
    final_summary+="\tcompression ratio : "+str((len(summary))/(len(text)))+"\n\n"
    output.write(final_summary)

    # code for LDA 

    data = []
    lda_stem = PorterStemmer()
    for sent in content:
        words = []
        for word in word_tokenize(sent):
            if word not in get_stop_words('en') and word not in stopwords.words("english") and word != '.':
                words.append(lda_stem.stem(word))
        data.append(words)
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(sent) for sent in data]
    
    # LDA model intialization 

    topic_used = 3 # no of topic to summarize

    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=topic_used, id2word = dictionary, passes=100)
    
    prob_sum_for_each_topic = [0.0 for i in range(topic_used)]
    data_desc = ldamodel.get_document_topics(corpus)
    print(data_desc)
    for data in data_desc:
        print(data)
        for topic_data in data:
            prob_sum_for_each_topic[topic_data[0]] += topic_data[1]
            print(topic_data[1])
    
    important_topic = prob_sum_for_each_topic.index(max(prob_sum_for_each_topic))
    threshold = prob_sum_for_each_topic[important_topic]/len(data_desc)

    lda_summary=""

    for index,word_data in enumerate(data_desc):
        if word_data[important_topic][1] > threshold:
            lda_summary+=content[index]

    """for index,sent in enumerate(content):
        print(data_desc[important_topic][index][1])
        if data_desc[important_topic][index][1] > threshold:
            lda_summary+= content[index]"""

    final_summary_lda="By LDA\n"
    final_summary_lda+=name.upper()+" "+"Summary: \n"+" "+lda_summary+"\n"
    final_summary_lda+="\tOriginal "+name+" : "+str(len(text))+" chars\n"
    final_summary_lda+="\tReduced Size : "+str(len(lda_summary))+" chars\n"
    final_summary_lda+="\tcompression ratio : "+str((len(lda_summary))/(len(text)))+"\n\n"
    output.write(final_summary_lda)

    f.close()

file = '4.pdf' # 4.pdf frp0261-ren.pdf 6.pdf 06970192.pdf autocitation.pdf p2017-lu.pdf
summarizer('abstract',file)
summarizer('introduction',file)
summarizer('conclusion',file)
output.close()
