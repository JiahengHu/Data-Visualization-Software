# analysis.py
# Jiaheng Hu
# Spring 2017
# CS251

import data
import numpy as np
import sys
import scipy.stats
import scipy.cluster.vq as vq
import random
import math



def data_range(headers,data): 
#returns a list of 2-element lists with the minimum and maximum values for each column.
	llist=[]
	for i in range (len(headers)):
		list=[]
		matrix=data.get_data([headers[i]])
		list.append(np.max(matrix))
		list.append(np.min(matrix))
		llist.append(list)
	return llist
	
def mean(headers,data): 
#Takes in a list of column headers and the Data object and returns a list of the mean values for each column		
	llist=[]
	for i in range (len(headers)):
		matrix=data.get_data([headers[i]])
		llist.append(np.mean(matrix))
	return llist
	
def stdev( headers,data): 
# returns a list of the standard deviation for each specified column.	
	llist=[]
	for i in range (len(headers)):
		matrix=data.get_data([headers[i]])
		llist.append(np.std(matrix))
	return llist
	
def normalize_columns_separately(headers,data): 
#returns a matrix with each column normalized so its minimum value is mapped to zero and its maximum value is mapped to 1.
	dRange=data_range(headers,data)
	list=[]
	for i in range (len(headers)):		
		matrix=data.get_data([headers[i]])
		matrix-=dRange[i][1]
		matrix/=(dRange[i][0]-dRange[i][1]) 
		list.append(matrix.tolist()[0]) 
	return np.matrix(list)
	
def normalize_columns_together(headers,data): 
#returns a matrix with each entry normalized so that the minimum value (of all the data in this set of columns) is mapped to zero and its maximum value is mapped to 1. 
	matrix=data.get_data(headers)
	max=np.max(matrix)
	min=np.min(matrix)
	matrix-=min
	matrix/=max-min
	return matrix

#extension 6
#return a list of sum of each column	
def sum(headers,data): 
	llist=[]
	for i in range (len(headers)):
		matrix=data.get_data([headers[i]])
		llist.append(matrix.sum())
	return llist

def linear_regression(d, ind, dep):
  # assign to y the column of data for the dependent variable
	y=d.get_data([dep])
  # assign to A the columns of data for the independent variables
	A=d.get_data(ind)
  #	   It's best if both y and A are numpy matrices
  # add a column of 1's to A to represent the constant term in the 
  #	   regression equation.	 Remember, this is just y = mx + b (even 
  #	   if m and x are vectors).
	homo=[]
	for i in range (len(A.tolist()[0])):
		homo.append(1.0)
	old = np.array(A)		
	A=np.vstack((old,homo))
	
  # assign to AAinv the result of calling numpy.linalg.inv( np.dot(A.T, A))
	AAinv=np.linalg.inv( np.dot(A, A.T))
  #	   The matrix A.T * A is the covariancde matrix of the independent
  #	   data, and we will use it for computing the standard error of the 
  #	   linear regression fit below.
	
	x=np.linalg.lstsq( A.T , y.T )
  # assign to x the result of calling numpy.linalg.lstsq( A, y )
  #	   This solves the equation y = Ab, where A is a matrix of the 
  #	   independent data, b is the set of unknowns as a column vector, 
  #	   and y is the dependent column of data.  The return value x 
  #	   contains the solution for b.
	
	b=x[0]
	N=np.shape(y)[1]
	C=np.shape(b)[0]
	df_e=N-C
	df_r=C-1
  # assign to b the first element of x.
  #	   This is the solution that provides the best fit regression
  # assign to N the number of data points (rows in y)
  # assign to C the number of coefficients (rows in b)
  # assign to df_e the value N-C, 
  #	   This is the number of degrees of freedom of the error
  # assign to df_r the value C-1
  #	   This is the number of degrees of freedom of the model fit
  #	   It means if you have C-1 of the values of b you can find the last one.
	
	error = y.T - np.dot(A.T, b)
  # assign to error, the error of the model prediction.	 Do this by 
  #	   taking the difference between the value to be predicted and
  #	   the prediction. These are the vertical differences between the
  #	   regression line and the data.
  #	   y - numpy.dot(A, b)
	
	sse = np.dot(error.T, error) / df_e
  # assign to sse, the sum squared error, which is the sum of the
  #	   squares of the errors computed in the prior step, divided by the
  #	   number of degrees of freedom of the error.  The result is a 1x1 matrix.
  #	   numpy.dot(error.T, error) / df_e
	
	stderr = np.sqrt( np.diagonal( sse[0, 0] * AAinv ) )
  # assign to stderr, the standard error, which is the square root
  #	   of the diagonals of the sum-squared error multiplied by the
  #	   inverse covariance matrix of the data. This will be a Cx1 vector.
  #	   numpy.sqrt( numpy.diagonal( sse[0, 0] * AAinv ) )
	
	t = b.T / stderr
  # assign to t, the t-statistic for each independent variable by dividing 
  #	   each coefficient of the fit by the standard error.
  #	   t = b.T / stderr
	
	p = 2*(1 - scipy.stats.t.cdf(abs(t), df_e))
  # assign to p, the probability of the coefficient indicating a
  #	   random relationship (slope = 0). To do this we use the 
  #	   cumulative distribution function of the student-t distribution.	
  #	   Multiply by 2 to get the 2-sided tail.
  #	   2*(1 - scipy.stats.t.cdf(abs(t), df_e))
	
	r2 = 1 - error.var() / y.T.var()
  # assign to r2, the r^2 coefficient indicating the quality of the fit.
  #	   1 - error.var() / y.var()

  # Return the values of the fit (b), the sum-squared error, the
  #		R^2 fit quality, the t-statistic, and the probability of a
  #		random relationship.
	return b.A, sse.A[0][0], r2, t.A[0], p[0]	
	
# take in a list of column headers and return a PCAData object with the source column headers, 
# projected data, eigenvalues, eigenvectors, and source data means within it.
def pca(d,headers,normalize=True):
	if normalize:
		A=normalize_columns_separately(headers,d).T
	else:
		A=d.get_data(headers).T 
		
  # assign to m the mean values of the columns of A
	m=A.mean(axis=0)
	
  # assign to D the difference matrix A - m
	D=A-m
  # assign to U, S, V the result of running np.svd on D, with full_matrices=False
	U, S, V = np.linalg.svd(D, full_matrices=False)
	
	N=np.shape(A)[0]
	
  # the eigenvalues of cov(A) are the squares of the singular values (S matrix)
  #	  divided by the degrees of freedom (N-1). The values are sorted.
	eigenvalues=S*S/(N-1)
	
  # project the data onto the eigenvectors. Treat V as a transformation 
  #	  matrix and right-multiply it by D transpose. The eigenvectors of A 
  #	  are the rows of V. The eigenvectors match the order of the eigenvalues.
	pdata=(V*D.T).T
	
  # create and return a PCA data object with the headers, projected data, 
  # eigenvectors, eigenvalues, and mean vector.
	result=data.PCAData(headers, pdata, eigenvalues,V,	m)
	return result

def kmeans_numpy( d, headers, K, whiten = True):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	Computes and returns the codebook, codes, and representation error.
	'''
	
	# assign to A the result of getting the data from your Data object
	A=d.get_data(headers).T
	
	# assign to W the result of calling vq.whiten on A
	W=vq.whiten(A)
	
	# assign to codebook, bookerror the result of calling vq.kmeans with W and K
	codebook, bookerror = vq.kmeans(W,K)
	
	# assign to codes, error the result of calling vq.vq with W and the codebook
	codes, error = vq.vq(W, codebook)
	
	# return codebook, codes, and error		
	return codebook, codes, error	

#take in the data, the number of clusters K, and an optional set of categories (cluster labels for each data point) 
#and return a numpy matrix with K rows, each one repesenting a cluster mean.
def kmeans_init(data, K, categories=''):
	F = data.shape[1]
	mean = []
	if categories is not '':
		for n in range(K):
			size = 0
			sum = [0]*F
			for i in range( data.shape[0]):
				if categories[i,0] == n:
					size+=1
					for j in range(F):
						sum[j] += data [i,j]
			for item in sum:
				mean.append(item/float(size))
				
	else:
		r = random.sample(range(data.shape[0]), K)
		mean=np.asmatrix(np.zeros((K,F)))
		i=0
		for item in r:
			mean[i,:]=data[item,:]
			i+=1
	return np.matrix(mean).reshape(K,F)
  

'''take in the data and cluster means and return a list or matrix (your choice) 
of ID values and distances. The IDs should be the index of the closest cluster mean to the data point. '''

def kmeans_classify(data, means,norm):
	IDlist=[]
	dlist=[]
	if norm == 0:
		for	 i in range(data.shape[0]):
			minDistance = np.inf
			ID = -1
			for k in range(means.shape[0]):
				distance=0
				for j in range(data.shape[1]):		
					if distance < abs(data[i,j]-means[k,j]):
						distance = abs(data[i,j]-means[k,j])
				if distance< minDistance:
					minDistance=distance
					ID=k
			IDlist.append(ID)
			dlist.append(minDistance)
		return np.matrix(IDlist).reshape(data.shape[0],1),np.matrix(dlist).reshape(1,data.shape[0])	
	
	if norm == 2:
		for	 i in range(data.shape[0]):
			minDistance = np.inf
			ID = -1
			for k in range(means.shape[0]):
				distance=0
				for j in range(data.shape[1]):			
					distance+=(data[i,j]-means[k,j])*(data[i,j]-means[k,j])
				distance=math.sqrt(distance)
				if distance< minDistance:
					minDistance=distance
					ID=k
			IDlist.append(ID)
			dlist.append(minDistance)
		return np.matrix(IDlist).reshape(data.shape[0],1),np.matrix(dlist).reshape(1,data.shape[0])
	
	for	 i in range(data.shape[0]):
		minDistance = np.inf
		ID = -1
		for k in range(means.shape[0]):
			distance=0
			for j in range(data.shape[1]):			
				distance+=abs((data[i,j]-means[k,j]))**norm
			distance=pow(distance,1.0/norm)
			if distance< minDistance:
				minDistance=distance
				ID=k
		IDlist.append(ID)
		dlist.append(minDistance)
	
	return np.matrix(IDlist).reshape(data.shape[0],1),np.matrix(dlist).reshape(1,data.shape[0])

def kmeans_algorithm(A, means, norm):
	# set up some useful constants
	MIN_CHANGE = 1e-7
	MAX_ITERATIONS = 100
	D = means.shape[1]
	K = means.shape[0]
	N = A.shape[0]
	
	
	# iterate no more than MAX_ITERATIONS
	for i in range(MAX_ITERATIONS):
		# calculate the codes
		codes, errors = kmeans_classify( A, means, norm )

		# calculate the new means
		newmeans = np.zeros_like( means )
		counts = np.zeros( (K, 1) )
		for j in range(N):
			newmeans[codes[j,0],:] += A[j,:]
			counts[codes[j,0],0] += 1.0

		# finish calculating the means, taking into account possible zero counts
		for j in range(K):
			if counts[j,0] > 0.0:
				newmeans[j,:] /= counts[j, 0]
			else:
				newmeans[j,:] = A[random.randint(0,A.shape[0]-1),:]

		# test if the change is small enough
		diff = np.sum(np.square(means - newmeans))
		means = newmeans
		if diff < MIN_CHANGE:
			break

	# call classify with the final means
	codes, errors = kmeans_classify( A, means, norm )

	# return the means, codes, and errors
	return (means, codes, errors)

def kmeans(d, headers, K, whiten=True, categories = '', norm=2):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	Computes and returns the codebook, codes and representation errors. 
	If given an Nx1 matrix of categories, it uses the category labels 
	to calculate the initial cluster means.
	'''
	if isinstance(d, np.ndarray):
		A=d
	
	# assign to A the result getting the data given the headers
	else:
		A=d.get_data(headers).T
	
	# if whiten is True
	  # assign to W the result of calling vq.whiten on the data
	if whiten == True:
		W = vq.whiten(A)
	  
	# else
	  # assign to W the matrix A
	else:
		W = A 
	
	# assign to codebook the result of calling kmeans_init with W, K, and categories
	codebook = kmeans_init(W, K, categories)
	
	# assign to codebook, codes, errors, the result of calling kmeans_algorithm with W and codebook		   
	codebook, codes, errors = kmeans_algorithm( W ,codebook, norm)
	
	# return the codebook, codes, and representation error
	return codebook, codes, errors

def kmeans2( d, headers, K, whiten = True):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	Computes and returns the codebook, codes, and representation error.
	'''
	if isinstance(d, np.ndarray):
		A=d
	
	# assign to A the result getting the data given the headers
	else:
		A=d.get_data(headers).T
	
	# assign to W the result of calling vq.whiten on A
	W=vq.whiten(A)
	
	# assign to codebook, bookerror the result of calling vq.kmeans2 with W and K
	codebook, bookerror = vq.kmeans2(W,K)
	
	# assign to codes, error the result of calling vq.vq with W and the codebook
	codes, error = vq.vq(W, codebook)
	
	# return codebook, codes, and error		
	return codebook, codes, error		

	
if __name__ == '__main__':
	d = data.Data( sys.argv[1] )
	headers = d.get_headers()
	print linear_regression( d, [headers[0],headers[1]],headers[10])
	