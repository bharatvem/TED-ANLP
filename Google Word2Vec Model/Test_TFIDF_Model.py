import pandas as pd
import numpy as np
import os
import csv
import math
from collections import defaultdict
import math
from textblob import TextBlob as tb
from collections import defaultdict
import re
import pickle
import os.path
import time
from collections import OrderedDict
from operator import itemgetter

# Get Train index File .....
# ------------------------------------------------------------------------------------------------------
os.chdir("C:/Users/jaide/PycharmProjects/TedNew/indexfiles")
inputReader = csv.reader(open('Traindata_Topics.csv', encoding='ISO-8859-1'), delimiter=',', quotechar='"')
topicsdata = pd.DataFrame()
for row in inputReader:
    list = []
    list.append(row)
    topicsdata = topicsdata.append(list)
cols = topicsdata.iloc[0]
topicsdata.columns = cols
topicsdata = topicsdata[topicsdata['Sno'] != 'Sno']

alltopics = topicsdata.loc[:, 'Topic1':'Topic10'].values.tolist()
topiclist = []
for items in alltopics:
    listing = [lis.upper() for lis in items]
    topiclist.append(listing)

ignore_topics = ["","AND", "BANG", "BIG", "CONDUCTING", "CULTURES", "DARK", "DEMO", "FELLOWS", "FOREIGN",
                 "GARDEN", "IN", "LIVE", "PRESENTATION", "SOUTH", "STREET", "SUBMARINE", "TED", "TEDX", "WORD",
                 "TED BOOKS","TED BRAIN TRUST","TED FELLOWS","TED PRIZE","TEDYOUTH"]

filtered_list = []
for items in topiclist:
    toremove = set(items) & set(ignore_topics)
    templist = [r for r in items if r not in toremove]
    templist = templist[0:5] # get top 5 topics for each file
    filtered_list.append(templist)

uni_topic = set(x for l in filtered_list for x in l)
uni_topic = sorted(uni_topic)
print(len(uni_topic))
# ------------------------------------------------------------------------------------------------------

# Read the Pickle File to see the output bag of words...
completeName = os.path.join('C:/Users/jaide/PycharmProjects/TedNew/Pickle_Results',"Allwords_ModelwithRank.pkl")
file1 = open(completeName, "rb")
Trainfile = pickle.load(file1)
file1.close()

completeName = os.path.join("C:/Users/jaide/PycharmProjects/TedNew/Pickle_Results","FilesPerTopic.pkl")
file1 = open(completeName, "rb")
files_dict = pickle.load(file1)
file1.close()

# Generate model for as many files as you need ....
TrainModel = {}
words_per_file = 75
for tp in uni_topic:
    filecount = files_dict[tp]
    dict_values = Trainfile[tp]
    print(tp,filecount)
    dict_values = dict_values[0:(filecount*words_per_file)]
    TrainModel[tp] = dict_values

# Export to csv section -----------------
word_cloud = pd.DataFrame(columns=['word','Tvalue','rank'])
for items in TrainModel['CANCER']:
    row = pd.DataFrame([items], columns=['word','Tvalue','rank'])
    print(row)
    word_cloud = word_cloud.append(row, ignore_index=True)

word_cloud.to_csv('wordcloud_CANCER.csv')


# Code to test an external files ...

# Code to read actual labels of the test file
os.chdir('C:/Users/jaide/PycharmProjects/TedNew/indexfiles')
inputReader = csv.reader(open('Testdata_topics.csv', encoding='ISO-8859-1'), delimiter=',', quotechar='"')
test_labels = pd.DataFrame()
for row in inputReader:
    list = []
    list.append(row)
    test_labels = test_labels.append(list)
tcols = test_labels.iloc[0]
test_labels.columns = tcols
test_labels = test_labels[test_labels['Sno'] != 'Sno']


# # Code to run all the test files...
# os.chdir('C:/Users/jaide/PycharmProjects/TedNew/Clean_TestFiles')
# prediction_results = defaultdict()
# all_prediction_results = defaultdict()
# accuracylist = []
#
# # Iterate for every file in the test file repository...
# tfiles = 0
# for tfiles in range(0,test_labels.shape[0]):
#     ratings = {}
#     name = test_labels.iloc[tfiles]['Filename']
#     print(name)
#     with open(name, 'r') as myfile:
#         data = myfile.read().replace('\n', '')
#         data1 = re.sub(r'\b\w{1,4}\b', '', data)
#     query = re.sub("[^\w]", " ", data1).split()
#
#     if len(query)>200:
#         for tpv in uni_topic:
#             traindf = {}
#             val = TrainModel[tpv]
#
#             for items in val:
#                 traindf[items[0]] = [items[1],items[2]]
#
#             words = [x[0] for x in TrainModel[tpv]]
#             test = set(words) & set(query)
#
#             rating = 0
#             for wd in test:
#                 rating = rating + traindf[wd][0]   #/ traindf[wd][1]
#             ratings[tpv]=rating/files_dict[tpv]
#         d = OrderedDict(sorted(ratings.items(), key=itemgetter(1),reverse=True))
#
#         # Get real labels of the test file
#         lbl = test_labels.loc[test_labels['Filename']==name, 'Topic1':].values.tolist()
#         lbl = [l.upper() for l in lbl[0] if l!='']
#         labels = [r for r in lbl if (r not in ignore_topics and r in uni_topic)]
#
#         # head = 35
#         head = 2*len(labels)
#         tail = 0
#         predictions=[]
#         allpred = d.keys()
#         for key,values in d.items():
#             if tail<head:
#                 predictions.append(key)
#                 tail = tail+1
#             else:
#                 break
#
#
#         accuracy = len(set(predictions) & set(labels))/len(labels)
#         print(accuracy)
#         accuracylist.append(accuracy)
#         prediction_results[name] = [labels,predictions,accuracy]
#         all_prediction_results[name] = [labels,allpred]
#
# accuracy_sum = 0
# for key,values in prediction_results.items():
#     accuracy_sum = accuracy_sum + values[2]
#
# overall_accuracy = accuracy_sum/len(prediction_results)
# print('Overall Accuracy is:',overall_accuracy)
# completeName = os.path.join('C:/Users/jaide/PycharmProjects/TedNew/indexfiles',"Top35Model_prediction_results.pkl")
# file1 = open(completeName, "wb")
# pickle.dump(prediction_results, file1, pickle.HIGHEST_PROTOCOL)
# file1.close()
#
# file1 = open(completeName, "rb")
# flist = pickle.load(file1)
# file1.close()


# Create code for Spearman's rank correlation coefficient .....

# Code to run all the test files...
os.chdir('C:/Users/jaide/PycharmProjects/TedNew/Clean_TestFiles')
prediction_results = defaultdict()
all_prediction_results = defaultdict()

# Iterate for every file in the test file repository...
tfiles = 0
total_correlation = 0
for tfiles in range(0,test_labels.shape[0]):
    ratings = {}
    name = test_labels.iloc[tfiles]['Filename']
    # name = 'dambisa_moyo_economic_growth_has_stalled_let_s_fix_it.txt'
    print(name)
    with open(name, 'r') as myfile:
        data = myfile.read().replace('\n', '')
        data1 = re.sub(r'\b\w{1,4}\b', '', data)
    query = re.sub("[^\w]", " ", data1).split()

    if len(query)>200:
        for tpv in uni_topic:
            traindf = {}
            val = TrainModel[tpv]

            for items in val:
                traindf[items[0]] = [items[1],items[2]]

            words = [x[0] for x in TrainModel[tpv]]
            test = set(words) & set(query)

            rating = 0
            for wd in test:
                rating = rating + traindf[wd][0]     #/ traindf[wd][1]
            ratings[tpv]=rating/files_dict[tpv]

        d = OrderedDict(sorted(ratings.items(), key=itemgetter(1),reverse=True))

        # Get real labels of the test file
        lbl = test_labels.loc[test_labels['Filename']==name, 'Topic1':].values.tolist()
        lbl = [l.upper() for l in lbl[0] if l!='']
        labels = [r for r in lbl if (r not in ignore_topics and r in uni_topic)]

        allpred = d.keys()
        predictions=[]
        for key,values in d.items():
            predictions.append(key)



        # --------Spearman's rank correlation coefficient------------------
        tp = [predictions.index(lbl) for lbl in labels]
        tp.sort()
        tp = [predictions[x] for x in tp]

        distance = 0
        l=0
        for l in range(0,len(labels)):
            distance += abs(l-tp.index(labels[l]))
        distance = math.pow(distance,2)
        p = 1 - ((6 * distance)+1) / (1 + (len(labels) * (math.pow(len(labels),2) - 1) ))
        print(p)
        total_correlation += p

overall_correlation = total_correlation/test_labels.shape[0]
print('Overall Rank correlation is:',overall_correlation)

