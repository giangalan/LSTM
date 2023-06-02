import string
import pandas as pd
from underthesea import word_tokenize, classify

data = pd.read_csv('../../Data/data_colab.csv')

def preprocess(data):
    listpunctuation = string.punctuation.replace('_', '').replace('.','').replace(',','')
    for i in listpunctuation:
        data = data.replace(i, ' ')
    return data

def clean(paragraph):
    sent_list = paragraph.split('.')
    paragraph = ''
    for sent in sent_list:
        sent = sent.strip()
        sent = word_tokenize(sent, format="text")
        if sent.endswith('.'):
            sent = sent[:-1]
        paragraph += sent+' '
    return paragraph
# for i in range(1,20):
para = preprocess(data['content'][3])
para = clean(para)
classe = classify(para)
print(classe)