import gensim, logging
import nltk
import os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Implement Word2vec from Gensim ... save all the trained models ...
# Generate sentences ....
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, fname)) as f:
                content = f.readlines()
                if len(content) !=0:
                    sent = nltk.sent_tokenize(content[0])
                    sent_list = [nltk.word_tokenize(x) for x in sent]
                    for s in sent_list:
                        yield s

sentences = MySentences('C:/Users/jaide/PycharmProjects/TedNew/talk_sentences')  # a memory-friendly iterator

model = gensim.models.Word2Vec(sentences, size=400, window=10, sg=1, alpha= 0.01, min_alpha= 0.0001, min_count=3,
                               negative=10, iter=200 ,workers=4)
model.save('C:/Users/jaide/PycharmProjects/TedNew/trained_model_word2vec_400_10_3_10_200')

