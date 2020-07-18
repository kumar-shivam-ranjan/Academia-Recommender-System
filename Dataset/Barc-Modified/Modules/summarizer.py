from sklearn.feature_extraction.text import TfidfVectorizer
import json
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

def preprocess(text):
    """
    For stemming and removing stop words
    """
    result = ""
    stemmer = SnowballStemmer('english')
    for word in word_tokenize(text):
        if word not in stopwords.words('english'):
            result += stemmer.stem(word)+" "
    return result.rstrip()

def tf_idf(words, paper_list):

    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'), vocabulary=words)
    matrix = vectorizer.fit_transform(paper_list)

    return matrix.todense(), vectorizer.get_feature_names()

def summarizer(title, abstract, to_select,top=3):

    f = json.load(open("./src/gist.json","r"))
    selected = []
    orgi_selected = []
    paper_to_idx = {}

    for item in f:
        if item['id'].split('.')[0] in to_select:
            selected.append(preprocess(item['abstract']))
            orgi_selected.append(item['abstract'])
            paper_to_idx[item['abstract']] = item['id'].split('.')[0]

    words = []
    words.extend(word_tokenize(preprocess(title)))
    words.extend(word_tokenize(preprocess(abstract)))
    words = list(set(words))
    # print(words)
    # print(selected)

    matrix, names = tf_idf(words,selected)
    # print(names)
    # print(matrix,matrix.shape)

    summary = []
    summ_dict = dict()

    for idx, item in enumerate(orgi_selected):
        sentences = sent_tokenize(item)
        scores = []
        for sent in sentences:
            s = 0.0
            for word in word_tokenize(sent):
                if preprocess(word) in names:
                    w_idx = names.index(preprocess(word))
                    s += matrix[idx,w_idx]
            scores.append((s,sent))
        scores.sort(reverse=True)
        scores = scores[:top]
        text = ""
        for items in scores:
            text += items[1] + " "
        summary.append(text)
        summ_dict[paper_to_idx[item]] = text
    # print(paper_to_idx)

    return summ_dict

# print(summarizer("Chinese unknown word identification as known word tagging","""This work presents a tagging approach to Chinese unknown word identification based on lexicalized hidden Markov models (LHMMs). In this work, Chinese unknown word identification is represented as a tagging task on a sequence of known words by introducing word-formation patterns and part-of-speech. Based on the lexicalized HMMs, a statistical tagger is further developed to assign each known word an appropriate tag that indicates its pattern in forming a word and the part-of-speech of the formed word. The experimental results on the Peking University corpus indicate that the use of lexicalization technique and the introduction of part-of-speech are helpful to unknown word identification. The experiment on the SIGHAN-PK open test data also shows that our system can achieve state-of-art performance.""",
#     ["P03-2039", "W03-1728"])[0])

