import re, math
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def preproccess(text):
    new_t = ""
    stemmer = SnowballStemmer('english', ignore_stopwords=True)
    lemma = WordNetLemmatizer()
    for word in text_to_vector(text):
        new_t += lemma.lemmatize(stemmer.stem(word)) + " "
        # new_t + stemmer.stem(word) + " "
    return new_t

def cosine_similarity(text1,text2):

    text1 = preproccess(text1)
    text2 = preproccess(text2)

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine = get_cosine(vector1, vector2)
    return cosine
    # print('Cosine:', cosine)
