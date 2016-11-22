
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import os
import csv
import math

os.chdir("C:/Users/jaide/PycharmProjects/Ted-DataCollection-Transcript")
# os.chdir('C:/Users/jaide/Desktop/Git Repositories/Natural Language Processing/Ted-DataCollection-Transcript/TranscriptFiles')
# code to read an prepare data frame for furture purpose
inputReader = csv.reader(open('topics.csv', encoding='ISO-8859-1'), delimiter=',',quotechar='"')
topicsdata = pd.DataFrame()
for row in inputReader:
    list = []
    list.append(row)
    topicsdata = topicsdata.append(list)
cols = topicsdata.iloc[0]
topicsdata.columns = cols
topicsdata = topicsdata[topicsdata['Sno']!='Sno']


# In[ ]:

# Get top 5 topics from every file
topics5data = topicsdata.loc[:,'Sno':'Topic5']
alltopics = topics5data.loc[:,'Topic1':'Topic5'].values
lt = np.unique(alltopics).tolist()
lt = [x.upper() for x in lt]
uni_topic = set(lt)
uni_topic = sorted(uni_topic)
del uni_topic[0]


# In[ ]:

# create sparse matrix row = file and col = topic
topicsparse = pd.DataFrame()
topicsparse = pd.DataFrame(np.zeros((len(alltopics),len(uni_topic))))
topicsparse.columns=uni_topic


# In[ ]:

j = 0
rows = len(alltopics)
for j in range(0,rows):
        for elem in alltopics[j]:
            if (elem != ''):
                topicsparse.iloc[j][elem.upper()]=1

            


# In[ ]:

files = topicsparse.loc[topicsparse['ADVENTURE']==1].index.tolist()
# Get files names for all the files of a given topic
filenames = []
for f in files:
    filenames.append(topics5data.iloc[f]['Filename'])

print(filenames)
testfile = filenames[-1]
del filenames[-1]
print(testfile)
print(filenames)


# In[ ]:

# Implementation TF, IDF, Tf * IDF
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


# In[ ]:

os.chdir("C:/Users/jaide/Desktop/Git Repositories/Natural Language Processing/Ted-DataCollection-Transcript/TranscriptFiles/clean")
os.getcwd()


# In[ ]:

bloblist = []
doclist = []
for names in filenames:
    with open(names, 'r') as myfile:
        data=myfile.read().replace('\n', '')
#         data1 = re.sub(r'\b\w{1,3}\b', '',data)
        document = tb('"""'+data.replace("'",'')+'"""')
        doclist.append(document)
        bloblist.append(document)
print(len(doclist))


# In[ ]:

bagofwords = ''
for i, blob in enumerate(bloblist):
#     print(i, blob)
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#     scores = {word: idf(word,bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:10]:
        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
#         print("Word: {}, IDF: {}".format(word, round(score, 5)))
        bagofwords = bagofwords + ' '+word
print(bagofwords)


# In[ ]:

testfile = 'lewis_pugh_swims_the_north_pole.txt'
with open(testfile, 'r') as myfile:
        data=myfile.read().replace('\n', '')
#         data1 = re.sub(r'\b\w{1,3}\b', '',data)
        document = '"""'+data.replace("'",'')+'"""'
print(testfile)
print(document)


# In[ ]:

wordlist = re.sub("[^\w]", " ",  bagofwords).split()
# print(wordlist)
query = re.sub("[^\w]", " ",  document).split()
# print(query)
# q = bagofwords
# w = document
test = set(wordlist) & set(query)
print(test)

