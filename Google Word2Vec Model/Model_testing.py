import gensim
from collections import defaultdict
import pickle
import os
import operator
import time
import pandas as pd
import csv


trained_model = gensim.models.Word2Vec.load('trained_model_word2vec_fullmodel')

# Testing .......
top_words_loaded = pickle.load( open( "top_50_words.pkl", "rb" ) )

predictions_dict = defaultdict(list)
#dir
file_number =  0
for fname in os.listdir('Clean_TestFiles'):
    # file
    file_number += 1
    st = time.time()
    with open(os.path.join('Clean_TestFiles', fname)) as f:
        # data
        print("Processing file:---------------", fname)
        print('File number:', file_number)
        if file_number > 10:
            try:
                content = f.readlines()
                if len(content) != 0:
                    # list of words
                    test_file = content[0].split()
                    similarity_dict = {}
                    # for every topic
                    for tp in top_words_loaded.keys():
                        similarity = 0
                        wd_counts = 1
                        for wds in test_file:
                            # For every word in that topic
                            for t_word in top_words_loaded[tp]:
                                try:
                                    similarity = similarity + trained_model.wv.similarity(wds, t_word)
                                    wd_counts += 1
                                except Exception as e:
                                    pass
                        similarity_dict[tp] = similarity / wd_counts

                    sx = sorted(similarity_dict.items(), key=operator.itemgetter(1), reverse=True)
                    predicted_topics = sx[:15]
                    predictions_dict[fname] = predicted_topics
                    print(predictions_dict[fname])

            except (UnicodeError, UnicodeDecodeError) as e:
                print("Unicdoe error occured for file: --------------------------------", fname)
        print("--- %s seconds ---" % (time.time() - st))
    if file_number == 50:
        break

file1 = open('predictions_dict_50.pkl', "wb")
pickle.dump(predictions_dict, file1, pickle.HIGHEST_PROTOCOL)
file1.close()



# Get Actual class labels .....
# Topics needed to be ignored for processing
ignore_topics = ["","AND", "BANG", "BIG", "CONDUCTING", "CULTURES", "DARK", "DEMO", "FELLOWS", "FOREIGN",
                 "GARDEN", "IN", "LIVE", "PRESENTATION", "SOUTH", "STREET", "SUBMARINE", "TED", "TEDX", "WORD",
                 "TED BOOKS","TED BRAIN TRUST","TED FELLOWS","TED PRIZE","TEDYOUTH",'nan']

predictions_dict = pickle.load(open('predictions_dict_50.pkl','rb'))

test_topics = pd.read_csv("indexfiles/Testdata_Topics.csv")
total_tp = 0
total_cnt = 0

for tname,pred_tp in predictions_dict.items():
    print("Filename:",tname)
    predictions = [x[0] for x in pred_tp]
    # print('predicted topics:', predictions)
    tt = test_topics.loc[test_topics['Filename'] == tname]

    tx = list(tt[(list(tt.loc[:, 'Topic1':'Topic10']))].iloc[0])

    # print("Test topics are:",tx)
    clean_test_topics = [str(t).upper() for t in tx if t not in ignore_topics]
    if len(clean_test_topics) > 5:
        clean_test_topics = clean_test_topics[:5]

    # print("Test clean topics are:",clean_test_topics)

    true_positives = list(set(clean_test_topics).intersection(set(predictions)))

    print("True positives:", true_positives)

    total_tp += len(true_positives)
    total_cnt += 5
    print("Correct topics:", true_positives)


print("Accuracy: ",total_tp / total_cnt)

