import os,csv
import pandas as pd
from collections import defaultdict
import re
from textblob import TextBlob as tb
import time
import math
import pickle
import operator
import nltk

# Get the topics index file ....
inputReader = csv.reader(open('indexfiles/Traindata_Topics.csv', encoding='ISO-8859-1'), delimiter=',', quotechar='"')

# DataFrame to store the index files that contains the file names and topic names for each file ...
topicsdata = pd.DataFrame()
for row in inputReader:
	row_list = []
	row_list.append(row)
	topicsdata = topicsdata.append(row_list)
cols = topicsdata.iloc[0]
topicsdata.columns = cols
topicsdata = topicsdata[topicsdata['Sno'] != 'Sno']

print(topicsdata.columns)

# Get Top 5 topics topics from every file
alltopics = topicsdata.loc[:, 'Topic1':'Topic10'].values.tolist()
topiclist = []
for items in alltopics:
    listing = [lis.upper() for lis in items]
    topiclist.append(listing)

# Topics needed to be ignored for processing
ignore_topics = ["","AND", "BANG", "BIG", "CONDUCTING", "CULTURES", "DARK", "DEMO", "FELLOWS", "FOREIGN",
                 "GARDEN", "IN", "LIVE", "PRESENTATION", "SOUTH", "STREET", "SUBMARINE", "TED", "TEDX", "WORD",
                 "TED BOOKS","TED BRAIN TRUST","TED FELLOWS","TED PRIZE","TEDYOUTH"]

# Filter the top 5 topics from the top 10 topics ignoring the unwnated topics
filtered_list = []
for items in topiclist:
    toremove = set(items) & set(ignore_topics)
    templist = [r for r in items if r not in toremove]
    templist = templist[0:5]
    filtered_list.append(templist)

# Find all unique topics ...
uni_topic = set(x for l in filtered_list for x in l)
uni_topic = sorted(uni_topic)
print(uni_topic)
print("Total Unique Topics",len(uni_topic))

# All training file names
train_file_names = topicsdata['Filename'].tolist()

# Collect all the files contributing towards each topic ...
topic_files = defaultdict(list)

for f in uni_topic:
    current_files = []
    for tp_ind in range(len(filtered_list)):
        if f in filtered_list[tp_ind]:
            current_files.append(train_file_names[tp_ind])
    topic_files[f] = current_files

# Term frequency of the word
def tf(word, blob,blob_len):
    return blob.words.count(word) / blob_len

# Total number of files that contain the word
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

# Inverse document frquency of the word
def idf(word, bloblist,bloblist_len):
    return math.log(bloblist_len / (1 + n_containing(word, bloblist)))

# Tfidf function
def tfidf(word, blob, bloblist,blob_len,bloblist_len):
    return tf(word, blob,blob_len) * idf(word, bloblist,bloblist_len)


# Generate blobs for each file
# Below file contains key as topic name, value is a dictionary of words as a key adn the TFIDF value as the value
topics_dict = defaultdict(list)

for k,v in topic_files.items():
    word_tfidf_dict = defaultdict(list)
    topic_name = k
    t_files = v

    # Clean up the blob to clear any words less than 4 letters ....
    print("Topic name is:",topic_name)
    print("number of Topic files:", len(t_files))
    bloblist = []
    allwords = ''
    for f in t_files:
        with open('Clean_TrainFiles/'+f, 'r') as myfile:
            data = myfile.read().replace('\n', '').replace("'", '')
            data1 = re.sub(r'\b\w{1,4}\b', '', data)
            allwords = allwords + ' ' + data1
            document = tb('"""' + data1 + '"""')
            bloblist.append(document)

    mainblob = tb('"""' + allwords + '"""')
    blob_len = len(mainblob.words)
    bloblist_len = len(bloblist)
    # Get only unique words from all words....
    blbwords = []
    uni_words = ''
    for word in mainblob.words:
        blbwords.append(word)

    blbwords = sorted(set(blbwords))
    for items in blbwords:
        uni_words = uni_words + ' ' + items
    uni_words = tb(uni_words)

    current_dict = {word: tfidf(word,mainblob,bloblist,blob_len,bloblist_len) for word in uni_words.words}

    topics_dict[topic_name] = current_dict

file1 = open("topics_dictionary.pkl", "wb")
pickle.dump(topics_dict, file1, pickle.HIGHEST_PROTOCOL)
file1.close()

topics_dict_loaded = pickle.load( open( "topics_dictionary.pkl", "rb" ) )

# Get top words for every topis by sorting the dictionary items in the topics_dict file
top_words_dict = defaultdict(list)

for key, value in topics_dict_loaded.items():
    print("Topic is:",key)
    sorted_x = sorted(value.items(), key=operator.itemgetter(1), reverse=True)

    if len(sorted_x) > 100:
        for i in range(100):
            top_words_dict[key].append(sorted_x[i][0])
    else:
        for i in range(len(sorted_x)):
            top_words_dict[key].append(sorted_x[i][0])

file1 = open("top_100_words.pkl", "wb")
pickle.dump(top_words_dict, file1, pickle.HIGHEST_PROTOCOL)
file1.close()