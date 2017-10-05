import gensim
from collections import defaultdict
import pickle
import os
import operator
import numpy as np
import scipy
import csv
import pandas as pd

trained_model = gensim.models.Word2Vec.load('trained_model_word2vec_fullmodel')

# Testing .......
top_words_loaded = pickle.load( open( "top_50_words.pkl", "rb" ) )
#
# topic_vectors = {}
#
# for key,values in top_words_loaded.items():
#     print(key)
#     print(values)
#     topic_matrix = np.empty((0,400), int)
#
#     for v in values:
#         try:
#             topic_matrix = np.append(topic_matrix,np.reshape(np.array(trained_model.wv[v]),(1,400)),axis = 0)
#         except Exception as e:
#             pass
#     print(topic_matrix.shape)
#     topic_vectors[key] = np.sum(topic_matrix,axis= 0) / topic_matrix.shape[0]
#
#
#
# file1 = open("topics_vectors_dict.pkl", "wb")
# pickle.dump(topic_vectors, file1, pickle.HIGHEST_PROTOCOL)
# file1.close()


topic_vectors = pickle.load(open("topics_vectors_dict.pkl", "rb"))

# Model testing
# Get similarity for all words and for all topics ...
#
# # Testing .......
# predictions_dict = defaultdict(list)
# #dir
# file_number =  0
# for fname in os.listdir('Clean_TestFiles'):
#     # file
#     file_number +=1
#     with open(os.path.join('Clean_TestFiles', fname)) as f:
#         # data
#         print("Processing file:---------------", fname, '   *******************   ',file_number)
#         try:
#             content = f.readlines()
#             if len(content) != 0:
#                 # list of words
#                 test_file = content[0].split()
#                 similarity_dict = {}
#                 # for every topic
#                 for tp in top_words_loaded.keys():
#                     similarity = 0
#                     wds_count = 0
#                     for wds in test_file:
#                         # For every word in that topic
#                             try:
#                                 similarity = similarity + (1 - scipy.spatial.distance.cosine(np.array(trained_model.wv[wds]), topic_vectors[tp]))
#                                 wds_count +=1
#                             except Exception as e:
#                                 pass
#                     if wds_count == 0:
#                         similarity_dict[tp] = 0
#                     else:
#                         similarity_dict[tp] = similarity / wds_count
#                 print(similarity_dict)
#                 sx = sorted(similarity_dict.items(), key=operator.itemgetter(1), reverse=True)
#                 predicted_topics = sx[:15]
#                 predictions_dict[fname] = predicted_topics
#                 print(predictions_dict[fname])
#
#         except (UnicodeError, UnicodeDecodeError) as e:
#             print("Unicdoe error occured for file: --------------------------------", fname)
#
# file1 = open('avg_model_predictions_dict.pkl', "wb")
# pickle.dump(predictions_dict, file1, pickle.HIGHEST_PROTOCOL)
# file1.close()


predictions_dict = pickle.load(open("avg_model_predictions_dict.pkl", "rb"))
# Get accuracy numbers ...

# Code to read actual labels of the test file
inputReader = csv.reader(open('indexfiles/Testdata_topics.csv', encoding='ISO-8859-1'), delimiter=',', quotechar='"')
test_labels = pd.DataFrame()
for row in inputReader:
    lt = []
    lt.append(row)
    test_labels = test_labels.append(lt)
tcols = test_labels.iloc[0]
test_labels.columns = tcols
test_labels = test_labels[test_labels['Sno'] != 'Sno']

ignore_topics = ["","AND", "BANG", "BIG", "CONDUCTING", "CULTURES", "DARK", "DEMO", "FELLOWS", "FOREIGN",
                 "GARDEN", "IN", "LIVE", "PRESENTATION", "SOUTH", "STREET", "SUBMARINE", "TED", "TEDX", "WORD",
                 "TED BOOKS","TED BRAIN TRUST","TED FELLOWS","TED PRIZE","TEDYOUTH"]

test_topics_dict = defaultdict(list)

for r in range(test_labels.shape[0]):
    row = test_labels.iloc[[r]]
    fname = row['Filename'][0]
    topics = row.loc[:,'Topic1':'Topic10'].iloc[0].tolist()
    clean_topics = [tp.upper() for tp in topics if tp.upper() not in ignore_topics]
    test_topics_dict[fname] = clean_topics[:5]

file1 = open('testfiles_topics_dict.pkl', "wb")
pickle.dump(test_topics_dict, file1, pickle.HIGHEST_PROTOCOL)
file1.close()

total_tp = 0
for key,values in test_topics_dict.items():
    actual = values
    predicted = predictions_dict[key]
    tp = list(set(actual) & set(predicted))
    print('---------------------',len(tp))
    print(key, actual, predicted)
    total_tp += len(tp)

Accuracy = total_tp / (len(test_topics_dict.keys()) * 5)

print("ACCURACY IS:",Accuracy)