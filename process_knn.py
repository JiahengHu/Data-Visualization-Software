# process_knn.py
# Jiaheng Hu
# Spring 2017
# CS251

import data
import classifiers
import sys

# execute task 2
def process(traind,trainc, testd, testc):
	filename="new_result.csv"
	num=6
	#number of exemplar to use
	
	neigh=3
	#number of neighbor
	
	
	print "reading data"
	
	trdata = data.Data(traind)
	trc = data.Data(trainc)
	tedata = data.Data(testd)
	tec = data.Data(testc)
	
	A = trdata.get_data( trdata.get_headers() ).T
	traincats = trc.get_data( [trc.get_headers()[0]] ).T
	
	print "building knn"
	
	knn = classifiers.KNN(dataObj=trdata, headers=trdata.get_headers(), categories=traincats, K=num)
	
	
	cats, labels = knn.classify(A,K=neigh)
	
	conf = knn.confusion_matrix(traincats,cats)
	print knn.confusion_matrix_str(conf)
	
	B = tedata.get_data( tedata.get_headers() ).T
	testcats = tec.get_data( [tec.get_headers()[0]] ).T
	cats, labels = knn.classify(B, K=neigh)
	conf = knn.confusion_matrix(testcats,cats)
	print knn.confusion_matrix_str(conf)
	
	#tedata.addColumn("Category","numeric",testcats.T.A[0])
	
	#tedata.write(filename)

if __name__ == '__main__':
	process(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])	