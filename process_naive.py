# process_naive.py
# Jiaheng Hu
# Spring 2017
# CS251

import data
import classifiers
import sys

# execute task 2
def process(traind,trainc, testd, testc):
	filename="wrclass.txt"
	
	print "reading data"
	
	trdata = data.Data(traind)
	trc = data.Data(trainc)
	tedata = data.Data(testd)
	tec = data.Data(testc)
	
	A = trdata.get_data( trdata.get_headers() ).T
	traincats = trc.get_data( [trc.get_headers()[0]] ).T
	
	print "building bayes"
	
	bayes = classifiers.NaiveBayes(dataObj=trdata, headers=trdata.get_headers(), categories=traincats)
	
	print bayes
	cats, labels = bayes.classify(A)
	
	conf = bayes.confusion_matrix(traincats,cats)
	print bayes.confusion_matrix_str(conf)
	
	B = tedata.get_data( tedata.get_headers() ).T
	testcats = tec.get_data( [tec.get_headers()[0]] ).T
	cats, labels = bayes.classify(B)
	
	conf = bayes.confusion_matrix(testcats,cats)
	print bayes.confusion_matrix_str(conf)
	
	bayes.write(filename)
	
	#tedata.addColumn("Category","numeric",testcats.T.A[0])
	
	
	
	#tedata.write(filename)

if __name__ == '__main__':
	process(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])	