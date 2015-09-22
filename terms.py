from termcolor import colored
from  nltk import stem, word_tokenize
from nltk.corpus import stopwords
import string
import unicodedata
import math
import os
import sys
from vector_mod import vector_mod_dict


PATH = ""
TOKENS = ""
INDICES = ""
SCORES = ""

ranks = []


def results():
	ranks = sorted(ranks,key=lambda tup: tup[1],reverse = True)
	i = 0
	for x in ranks:
		i = i + 1
		print x[0]
		if i%10==0:
			f = raw_input("press y for more")
			if f == "y" or f == "Y":
				continue
			else:
				break


def create_query_vector(tokens):
	vector = []
	sorted_list = os.listdir(INDICES).sort()
	for index in sorted_list:
		if ".pyc" in index or "init" in index:
			continue
		exec("from indices." + index[:-3] + " import ii")
		df = len(ii)
		tf = 0
		for word in tokens:
			if word == ii:
				tf = tf + 1
		tf = math.log(1+tf,2)
		vector.append(tf*df)
	mod = 0
	for num in vector:
		mod = mod + num*num
	mod = math.sqrt(mod)
	return vector, mod


def search(query_vector,query_mod):
	for score_file in os.listdir(SCORES):
		exec("from scores." + score_file[:-3] + "vect")
		mod_vector  = vector_mod_dict[score_file[:-3]]
		dotproduct = 0
		for i in xrange(0,len(vect)):
			dotproduct = vect[i]*query_vector[i]
		angle = math.acos(dotproduct/(mod_vector*query_mod))
		ranks.append((score_file,angle))

def main():
	while True:
		query = raw_input("Enter Your Query Here or Press Q to Exit\n$")
	    porter = stem.porter.PorterStemmer()
	    if query == "Q" or query == "q":
	    	print "Thank You"
	    	sys.exit()
		r = unicodedata.normalize('NFKD', f.read()).encode('ascii', 'ignore')
        r = r.translate(None, string.punctuation)
        t = word_tokenize(r)

        t = [porter.stem(tok).lower() for tok in t]
        t = [tok for tok in t if tok not in stopwords.words('english')]
        query_vector, query_mod = create_query_vector(t)
        search(query_vector,query_mod)
        results()
        rank = []

if __name__ == "__main__":
	main()