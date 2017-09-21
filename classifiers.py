# Template by Bruce Maxwell
# Modified by Jiaheng Hu
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import analysis as an
import numpy as np
import math
import scipy

class Classifier:

	def __init__(self, type):
		'''The parent Classifier class stores only a single field: the type of
		the classifier.	 A string makes the most sense.

		'''
		self._type = type

	def type(self, newtype = None):
		'''Set or get the type with this function'''
		if newtype != None:
			self._type = newtype
		return self._type

	def confusion_matrix( self, truecats, classcats ):
		'''Takes in two Nx1 matrices of zero-index numeric categories and
		computes the confusion matrix. The rows represent true
		categories, and the columns represent the classifier output.'''
		
		unique=np.unique(truecats.A)
		conf = np.asmatrix(np.zeros((unique.shape[0],unique.shape[0])))
		for i in range(truecats.shape[0]):
			conf[int(classcats[i,0]),int(truecats[i,0])] += 1
		return conf

	def confusion_matrix_str( self, conf ):
		'''Takes in a confusion matrix and returns a string suitable for printing.'''
		s = '  Actual->'
		for i in range(conf.shape[1]):
			s+='  Cluster %d' % (i)
		s+="\n"
		for i in range(conf.shape[0]):	
			s += 'Cluster %d' % (i)
			for k in range(conf.shape[1]):	
				s += "%10d" % (conf[i,k])
			s +=	"\n"
		return s

	def __str__(self):
		'''Converts a classifier object to a string.  Prints out the type.'''
		return str(self._type)



class NaiveBayes(Classifier):
	'''NaiveBayes implements a simple NaiveBayes classifier using a
	Gaussian distribution as the pdf.

	'''

	def __init__(self, dataObj=None, headers=[], categories=None):
		'''Takes in a Data object with N points, a set of F headers, and a
		matrix of categories, one category label for each data point.'''

		# call the parent init with the type
		Classifier.__init__(self, 'Naive Bayes Classifier')
		
		# store the headers used for classification
		self.headers = headers
		
		# number of classes and number of features
		self.num_classes=None
		self.NumFeature=None
		# original class labels
		self.class_labels=None
		
		# unique data for the Naive Bayes: means, variances, scales
		self.means=None
		self.class_vars=None
		self.scales=None
		
		# if given data,
			# call the build function
		if dataObj is not None:
			self.build(dataObj.get_data(headers).T,categories)	

	def build( self, A, categories ):
		'''Builds the classifier give the data points in A and the categories'''
		
		# figure out how many categories there are and get the mapping (np.unique)
		unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
		self.num_classes=len(unique)
		self.NumFeature=A.shape[1]
		self.class_labels=unique
				
		# create the matrices for the means, vars, and scales
		self.class_means=np.asmatrix(np.zeros((self.num_classes,self.NumFeature)))
		self.class_vars=np.asmatrix(np.zeros((self.num_classes,self.NumFeature)))
		self.class_scales=np.asmatrix(np.zeros((self.num_classes,self.NumFeature)))
		

		# the output matrices will be categories (C) x features (F)
		# compute the means/vars/scales for each class
		# store any other necessary information: # of classes, # of features, original labels
		
		for i in range(self.num_classes):
			for j in range(self.NumFeature):
				self.class_means[i,j]=np.mean(A[(mapping==i),j])
				self.class_vars[i,j]=np.var(A[(mapping==i),j], ddof=1)
				self.class_scales[i,j]=1.0/math.sqrt(2*math.pi*self.class_vars[i,j])
		
		return

	def classify( self, A, return_likelihoods=False ):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_likelihoods
		is True, it also returns the NxC likelihood matrix.

		'''
		# error check to see if A has the same number of columns as
		# the class means
		if(A.shape[1]!=self.class_means.shape[1]):
			print "error"
			return
		
		# make a matrix that is N x C to store the probability of each
		# class for each data point
		
		P = np.asmatrix(np.zeros((A.shape[0],self.num_classes)))
		# a matrix of zeros that is N (rows of A) x C (number of classes)

		# calculate the probabilities by looping over the classes
		#  with numpy-fu you can do this in one line inside a for loop
		for i in range(self.num_classes):
			for j in range(A.shape[0]):
				a = self.class_vars[i,:]*2
				b = np.square(A[j,:] - self.class_means[i,:])
				P[j,i] = np.prod(np.multiply(self.class_scales[i,:], np.exp(-b/a)))
		
		# calculate the most likely class for each data point
		cats = np.argmax(P, axis=1) # take the argmax of P along axis 1

		# use the class ID as a lookup to generate the original labels
		labels = self.class_labels[cats]

		if return_likelihoods:
			return cats, labels, P

		return cats, labels

	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nNaive Bayes Classifier\n"
		for i in range(self.num_classes):
			s += 'Class %d --------------------\n' % (i)
			s += 'Mean	: ' + str(self.class_means[i,:]) + "\n"
			s += 'Var	: ' + str(self.class_vars[i,:]) + "\n"
			s += 'Scales: ' + str(self.class_scales[i,:]) + "\n"

		s += "\n"
		return s
		
	def write(self, filename):
		'''Writes the Bayes classifier to a file.'''
		# extension
		fp=file(filename,'rU+')	
		fp.write(self.__str__())
		fp.close()
		
		return

	def read(self, filename):
		'''Reads in the Bayes classifier from the file'''
		# extension
		return

	
class KNN(Classifier):

	def __init__(self, dataObj=None, headers=[], categories=None, K=None):
		'''Take in a Data object with N points, a set of F headers, and a
		matrix of categories, with one category label for each data point.'''

		# call the parent init with the type
		Classifier.__init__(self, 'KNN Classifier')
		
		# store the headers used for classification
		self.headers = headers
		
		# number of classes and number of features
		self.num_classes=None
		self.NumFeature=None
		# original class labels
		self.class_labels=None
		
		# unique data for the KNN classifier: list of exemplars (matrices)
		self.exemplars=[]
		
		# if given data,
			# call the build function
		if dataObj is not None:
			self.build(dataObj.get_data(headers).T,categories, K)	
			
			

	def build( self, A, categories, K = None ):
		'''Builds the classifier give the data points in A and the categories'''
	
		# figure out how many categories there are and get the mapping (np.unique)
		unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
		self.num_classes=len(unique)
		self.NumFeature=A.shape[1]
		
		
		self.class_labels=unique
		
				
		for i in range(self.num_classes):
			if K is None:
				self.exemplars.append(A[(mapping==i),:])
			else:	
				codebook, codes, errors=an.kmeans(A[(mapping==i),:],self.headers,K,whiten=False)
				'''extension2, using other method to get exemplars'''
				self.exemplars.append(codebook)
		
		# figure out how many categories there are and get the mapping (np.unique)
		# for each category i, build the set of exemplars
			# if K is None
				# append to exemplars a matrix with all of the rows of A where the category/mapping is i
			# else
				# run K-means on the rows of A where the category/mapping is i
				# append the codebook to the exemplars

		# store any other necessary information: # of classes, # of features, original labels

	def classify(self, A, K=3, return_distances=False):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_distances is
		True, it also returns the NxC distance matrix.

		The parameter K specifies how many neighbors to use in the
		distance computation. The default is three.'''
		
		
		# error check to see if A has the same number of columns as the class means
		if(A.shape[1]!=self.NumFeature):
			print "error, shape doesn't match"
			return
		
		
		# make a matrix that is N x C to store the distance to each class for each data point
		
		D = np.asmatrix(np.zeros((A.shape[0],self.num_classes))) # a matrix of zeros that is N (rows of A) x C (number of classes)
		

		# for each class i
			# make a temporary matrix that is N x M where M is the number of examplars (rows in exemplars[i])
			# calculate the distance from each point in A to each point in exemplar matrix i (for loop)
			# sort the distances by row
			# sum the first K columns
			# this is the distance to the first class
		for i in range (self.num_classes):
			matrix = np.asmatrix(np.zeros((A.shape[0],self.exemplars[i].shape[0])))
			for j in range (A.shape[0]):
				for k in range (self.exemplars[i].shape[0]):
					matrix[j,k]=scipy.spatial.distance.euclidean(A[j],self.exemplars[i][k])
					#np.sum(np.square((A[j,:]-self.exemplars[i][k,:]))) would also work
					'''extension, using other distance metrics'''
					
			matrix.sort(axis=1)
			D[:,i] = np.sum(matrix[:,:K], axis = 1)

		# calculate the most likely class for each data point
		cats = np.argmin(D, axis=1) # take the argmin of D along axis 1

		# use the class ID as a lookup to generate the original labels
		labels = self.class_labels[cats]

		if return_distances:
			return cats, labels, D

		return cats, labels


	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nKNN Classifier\n"
		for i in range(self.num_classes):
			s += 'Class %d --------------------\n' % (i)
			s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
			s += 'Mean of Exemplars	 :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

		s += "\n"
		return s


	def write(self, filename):
		'''Writes the KNN classifier to a file.'''
		# extension
		fp=file(filename,'rU+')	
		fp.write(self.__str__())
		fp.close()
		return

	def read(self, filename):
		'''Reads in the KNN classifier from the file'''
		# extension
		return
	

