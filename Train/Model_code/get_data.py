import string
import pandas as pd
from underthesea import word_tokenize, classify

data = pd.read_csv('../../Data/data_copy.csv')

def preprocess(data):
    listpunctuation = string.punctuation.replace('_', '').replace('.','').replace(',','')
    for i in listpunctuation:
        data = data.replace(i, ' ')
    return data

def split(paragraph):
    sent_list = paragraph.split('. ')
    for sent in sent_list:
        sent = sent.strip()
        if sent.endswith('.'):
            sent = sent[:-1]
    return sent_list
types = ['the_gioi']
# for i in range(1,20):
for item in data['content']:
    para = preprocess(item)
    sent_list = split(item)
    parag = ''
    for sent in sent_list:
        sent = word_tokenize(sent, format="text")
        parag += sent+' '
    a = classify(parag) 
    if a not in types:
        types.append(a)
print(types)