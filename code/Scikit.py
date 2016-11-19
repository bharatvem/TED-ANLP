# http://stackoverflow.com/questions/27889873/clustering-text-documents-using-scikit-learn-kmeans-in-python
#Update variable path ="path = "D:\INDIANA\ADV_NLP\Project\TED-ANLP\Ted-DataCollection-Transcript\TranscriptFiles\clean"
# to path of Training.txt and Test.txt files.
 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import glob, pickle, collections
def test_data(filename, clusters):
	text = open(filename, mode = "r", encoding = "ISO-8859-1")
	data = text.read().split()
	text.close()
	max_cluster =  0
	max_score = 0
	data_dict = collections.defaultdict(lambda: 0)
	for word in data:
		data_dict[word] +1
	#print (data_dict)	
	result = collections.defaultdict(lambda: 0)
	for c in clusters:
		keywords = clusters[c]
		score = 0
		for k in keywords:
			#print (k)
			if k in data_dict:
				score +=1
		#print (score, max_score)
		result[c] = float(score /len(keywords)		)* 100
		if score > max_score:
			max_score = score
			max_cluster = c
	print(filename.split('\\')[-1])	
	#print()	
	print ("Closeness of file to clusters ")
	for k in result:
		print (k," ",result[k]," %")				
	print()
def main(file_names, clusters):
	vectorizer = TfidfVectorizer(stop_words='english')
	data_list = []
	for i in file_names:
		#print ("HEREEEEEEEEEE", i)
		text = open(i, mode = "r", encoding = "ISO-8859-1")
		data = text.read()
		text.close()
		#print (data)
		data_list.append(data)		
	X = vectorizer.fit_transform(data_list)

	true_k = 4
	model = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=10)
	model.fit(X)
	#print(file_names)
	print("Top terms per cluster:")
	order_centroids = model.cluster_centers_.argsort()[:, ::-1]
	terms = vectorizer.get_feature_names()
	file_details = collections.defaultdict(list)
	for i in range(len(model.labels_)):
		c = model.labels_[i]
		file_details[c].append(file_names[i].split('\\')[-1])
	#print (model.labels_)
	#for c in file_details:
	#	print (c," ", file_details[c])
	#	print()		
	##print()
	#print()
	for i in range(true_k):
		#print ("Cluster %d:" % i,)
		
		for ind in order_centroids[i, :15]:
			#print (' %s' % terms[ind],)
			clusters[i].append(terms[ind])
		#print ()
	print (clusters)	

if __name__ ==  "__main__":
	file_names = []
	clusters = collections.defaultdict(list)
	path = "D:\INDIANA\ADV_NLP\Project\TED-ANLP\Ted-DataCollection-Transcript\TranscriptFiles\clean"
	training_files = open("Training.txt", mode="r", encoding ="utf-8")
	files = training_files.readlines()
	training_files.close()
	visited = []
	for line in files:
		if line not in visited:
		#print (line.rstrip('\n'))
			new_path = path +"\\"+line.rstrip('\n')
		#print ("newwwwwww", new_path)
	#for x in glob.glob(path+"\\Training\\*.txt"):
			#print ("hereeeeeeeee", x)
			file_names.append(new_path)
	main(file_names, clusters)    
	#ofp = open("Model.dat", mode='wb')
	#pickle.dump(clusters, ofp)
	#ofp.close()
	test_file = open("Test.txt",  mode="r", encoding ="utf-8" )
	files = test_file.readlines()
	test_file.close()
	for line in files:
		#print (line)
	#for x in glob.glob(path+"\\Test\\*.txt"):	
		test_data(path+"\\"+line.rstrip('\n'), clusters)
