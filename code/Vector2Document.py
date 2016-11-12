import collections, operator, sys
word_vectors = {"lifestyle" : {"consciousness": 10,"brain" :10,"body" :15,"mind" :20, "feel" : 10},\
				"technology" :{"computer" : 10, "internet":10, "revolution":10}  }
def read_data(filename):
	#print (filename)
	data_dict = collections.defaultdict(lambda: 0)
	file = open(filename, mode = 'r', encoding='ISO-8859-1')
	for line in file:
		words = line.lower().split()
		for i in words:
			data_dict [i] += 1
	#return check_similarity(sorted(data_dict.items(), key = operator.itemgetter(1), reverse = True ))
	return check_similarity (data_dict)
def check_similarity(data_dict):
	#print (data_dict)
	result = ""
	count_max = -sys.maxsize	
	for i in word_vectors:
		keywords = word_vectors [i]
		count = 0
		for k in keywords:
			#print (k)
			if k in data_dict:
				#print (keywords[k], data_dict[k])
				count += keywords[k] - data_dict[k]
		#print (count, count_max)		
		if count >count_max:
			result = i
			count_max = count
	#print (result)
	return result			
print (read_data("amy_cuddy_your_body_language_shapes_who_you_are.txt"))
print (read_data("pranav_mistry_the_thrilling_potential_of_sixthsense_technology.txt"))
