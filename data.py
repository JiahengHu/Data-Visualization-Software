# data.py
# Jiaheng Hu
# Spring 2017
# CS251

import csv
import time
from datetime import datetime
import numpy as np
import sys
import analysis


class Data:

	def __init__(self, filename = None):
		# create and initialize fields for the class
		self.filename=filename
						
		if filename != None:
			self.read(filename)
			
	def read(self,	filename):
		self.raw_headers = []
		self.raw_types = []
		self.raw_data =[]
		self.header2raw = {}
		
		self.matrix_headers = []
		self.matrix_data = np.matrix([])
		self.header2matrix = {}
		
		self.enum_dict=[]
		
		fp=file(filename,'rU+')
		
		reader=csv.reader(fp, delimiter=',', quotechar='|')
		self.raw_headers=reader.next()
		self.raw_types=reader.next()
		
		for row in reader:
			self.raw_data.append(row)
		

		
		for i in range(len(self.raw_headers)):
			self.header2raw[self.raw_headers[i]] = i
		
		matrix=[]	
		
		for i in range (self.get_raw_num_columns()):
			
			#extension 1
			#convert the data into numeric if the data type is enum
			if self.raw_types[i].strip()== 'enum':
				row=[]
				for j in range (self.get_raw_num_rows()):
					row.append(self.raw_data[j][i])
				dict=self.turn_enumerated(row)					
				self.enum_dict.append(dict)
				
				#loop through that column and change all the data into numeric
				for j in range (self.get_raw_num_rows()):
					self.raw_data[j][i]=dict[self.raw_data[j][i]]
				
				#set the type to numeric
				self.raw_types[i]='numeric'
			
			
			#extension 2
			#convert the data into numeric if the data type is date
			if self.raw_types[i].strip()== 'date':
				for j in range (self.get_raw_num_rows()):
				
					#extension 3
					try:
						#convert the string to date type
						dobj=datetime.strptime(self.raw_data[j][i],'%m/%d/%y')
					except:
						print "4 digit year"	
					try:	
						dobj=datetime.strptime(self.raw_data[j][i],'%m/%d/%Y')
					except:
						print "2 digit year"	
					#convert the date to float type
					nobj=time.mktime(dobj.timetuple())
					self.raw_data[j][i]=nobj
				
				
				self.raw_types[i]='numeric'
			
		
			#put the data into matrix if the data type is numeric
			if self.raw_types[i].strip()== 'numeric':
				
				#attach the header to matrix header
				self.matrix_headers.append(self.raw_headers[i])
				
				row=[]
				for j in range (self.get_raw_num_rows()):
					row.append(float(self.raw_data[j][i]))
				matrix.append(row)
							
				
		self.matrix_data=np.matrix(matrix)			
		
		for i in range(len(self.matrix_headers)):
			self.header2matrix[self.matrix_headers[i]] = i			
							
		fp.close()	
		
		#self.addColumn('new column','numeric',[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0])
	
	#extension 1
	#return a dictionary of a given column of enum data	
	def turn_enumerated(self,column):
		dictionary={}
		counter=0
		for i in range(len(column)):
			if not dictionary.has_key(column[i]):
				dictionary[column[i]]=counter
				counter+=1		
		return dictionary		
	
	#extension 5
	#add a column of data to the Data object. It will require a header, a type, and the correct number of points.
	def addColumn(self,header,type, data):
		
		
		self.raw_headers.append(header)
		self.raw_types.append(type)
		self.header2raw[header]=len(self.header2raw)
		i=0
		for item in self.raw_data:
			item.append(data[i])
			i+=1
		
		if type.strip()=="numeric":
			self.header2matrix[header]=len(self.header2matrix)
			new_column = np.array(np.matrix( data ))
			old=np.array(self.matrix_data)
			
			
			self.matrix_data=np.vstack((old,new_column))
			self.matrix_headers.append(header)
			
	
	#merge two sets of data		
	def merge_data(self,data):
		col=data.get_num_columns()
		
		for i in range (col):
			self.addColumn(data.get_headers()[i],"numeric",data.get_column(i))
				
	
	def get_headers(self): #list of headers of columns with numeric data	
		return self.matrix_headers
		
	def get_num_columns(self): #returns the number of columns of numeric data	
		return len(self.matrix_headers)
		
	def get_column(self,col):#take a col index and returns a column of numeric data	
		col=self.matrix_data[col,:].tolist()
		if len(col)==1:
					col=col[0]
		return col
		
	def get_row(self, row): #take a row index and returns a row of numeric data	
		row=self.matrix_data[:,row].T.tolist()
		if len(row)==1:
					row=row[0]
		return row
					
	def get_value(self, row, col): #takes a row index (int) and column header (string) and returns the data in the numeric matrix.	
		return self.matrix_data[self.header2matrix[col],row].tolist()
	
	def get_data(self, headers): #At a minimum, this should take a list of columns headers and return a matrix with the data for all rows but just the specified columns.	
		matrix=[]	
		
		for i in range (len(headers)):
			if headers[i]==None:
				row=[]
				for k in range (self.matrix_data.shape[1]):
					row.append(0)
			else:	
				row=self.matrix_data[self.header2matrix[headers[i]],:].tolist()
				if len(row)==1:
					row=row[0]
				#deal with the numpy's strange property of having different way of tolist	
			matrix.append(row)
		return 	np.matrix(matrix)
	
			
	#returns a list of all of the headers.
	def get_raw_headers(self):
		return self.raw_headers
	
	#returns a list of all of the types.
	def get_raw_types(self):
		return self.raw_types
	
	#returns the number of columns in the raw data set	
	def get_raw_num_columns(self):
		return len(self.raw_headers)
	
	#returns the number of rows in the data set.	
	def get_raw_num_rows(self):
		return len(self.raw_data)
			
	#returns a row of data (the type is list) given a row index (int).	
	def get_raw_row(self, number): 			
		return self.raw_data[number]
	
	#takes a row index (an int) and column header (a string) and returns the raw data at that location.
	def get_raw_value(self, row, header):
		return str(self.raw_data[row][self.raw_headers.index(header)])
	
	def clone(self):
		data=Data()
		data.raw_headers=list(self.raw_headers)
		data.raw_types=list(self.raw_types)
		data.raw_data=list(self.raw_data)
		data.header2raw=dict(self.header2raw)
		
		data.matrix_headers=list(self.matrix_headers)
		data.matrix_data=self.matrix_data.copy()
		data.header2matrix=dict(self.header2matrix)
		
		data.enum_dict=list(self.enum_dict)
		
		data.raw_headers=list(self.raw_headers)
		data.raw_types=list(self.raw_types)
		
		return data
	
	def write(self, filename, headers=None):
		
		
		fp=file(filename,'rU+')		
		if headers is None:
			headers = self.get_headers()
		data = self.get_data(headers)	
		
		for i in headers:
			fp.write(i+",")
		fp.write("\n")
		
		for i in range(len(headers)):
			fp.write("numeric,")
		fp.write("\n")		
		
		for k in range(self.get_raw_num_rows()):
			for i in range(len(headers)):
				fp.write(str(data[i,k])+",")
			fp.write("\n")			
		
# 	def printResult(self):
# 		print self.raw_data		

class PCAData(Data):
	def __init__(self,oriHeaders, projectedData,eigenvalues, eigenvectors, mdv):
		Data.__init__( self )
		self.eigenvalues=eigenvalues
		self.eigenvectors=eigenvectors
		self.mdv=mdv
		self.oriHeaders=oriHeaders
		self.matrix_data=projectedData.T
		
		self.raw_headers = []
		self.raw_types = []
		self.raw_data =[]
		self.header2raw = {}
		self.enum_dict=[]
		
		self.matrix_headers = []
		self.header2matrix = {}
		
		for i in range (len(self.oriHeaders)):
			self.raw_headers.append("P"+str(i))
			self.matrix_headers.append("P"+str(i))
			self.raw_types.append("numeric")
		
		for i in range(len(self.matrix_headers)):
			self.header2matrix[self.matrix_headers[i]] = i	
		
		for i in range(len(self.raw_headers)):
			self.header2raw[self.raw_headers[i]] = i
		
		for i in range(np.shape(self.matrix_data)[1]):
			self.raw_data.append(self.matrix_data[:,i])		
			
	
	def get_eigenvalues(self):
	#returns a copy of the eigenvalues as a single-row numpy matrix.
		return 	self.eigenvalues.copy()
	
	def get_eigenvectors(self):
	#returns a copy of the eigenvectors as a numpy matrix with the eigenvectors as rows.
		return self.eigenvectors.copy()
	
	def get_data_means(self):
	#returns the means for each column in the original data as a single row numpy matrix.
		return self.mdv.copy()
	
	def get_data_headers(self):
	#returns a copy of the list of the headers from the original data used to generate the projected data.	
		return list(self.oriHeaders)
		

	
	
	
	