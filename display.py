# Tk display app
# Written by Bruce Maxwell and Jiaheng Hu
#
# CS 251
# Spring 2015

import Tkinter as tk
import tkFont as tkf
from Tkinter import *
import tkFileDialog
import os
import math
import random
import view
import numpy as np
import data
import sys
import analysis
import scipy.stats
import classifiers

class Dialog(Toplevel):
	#This class is the skeleton class of creating dialog
	def __init__(self, parent, title = None):

		Toplevel.__init__(self, parent)
		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent

		self.result = "cancel"

		body = Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)

		self.buttonbox()

		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)
		

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = Frame(self)

		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override
		
class AxisDialog(Dialog):
	#This class creates a data-axis distribution dialog
	def __init__(self, parent,	headers, title = None):
		self.headers = headers
		Dialog.__init__( self, parent, title )
		

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="X axis:").grid(row=0)
		Label(master, text="Y axis:").grid(row=1)
		Label(master, text="Z axis:").grid(row=2)
		Label(master, text="Size:").grid(row=0,column=2)
		Label(master, text="Color:").grid(row=1,column=2)
		Label(master, text="Stat:").grid(row=2,column=2)
		
		
		self.xbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.xbox.insert(i,self.headers[i].strip())
		self.xbox.grid(row=0,column=1)
		
		self.ybox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.ybox.insert(i,self.headers[i].strip())
		self.ybox.grid(row=1,column=1)
		
		self.zbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.zbox.insert(i,self.headers[i].strip())
		self.zbox.grid(row=2,column=1)
		
		self.size = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.size.insert(i,self.headers[i].strip())
		self.size.grid(row=0,column=3)
		
		self.color = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.color.insert(i,self.headers[i].strip())
		self.color.grid(row=1,column=3)
		
		'''extension 8'''
		self.stat = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.stat.insert(i,self.headers[i].strip())
		self.stat.grid(row=2,column=3)

	def apply(self):
		
		self.result=[]
		if len(self.xbox.curselection()) !=0:
			self.result.append(self.xbox.curselection()[0])
		else:
			self.result.append(None)	
			
		if len(self.ybox.curselection()) !=0:
			self.result.append(self.ybox.curselection()[0]) 
		else:
			self.result.append(None)		
		
		if len(self.zbox.curselection()) !=0:
			self.result.append(self.zbox.curselection()[0]) 
		else:
			self.result.append(None)	
		
		if len(self.size.curselection()) !=0:
			self.result.append(self.size.curselection()[0]) 
		else:
			self.result.append(None)	
		
		if len(self.color.curselection()) !=0:
			self.result.append(self.color.curselection()[0]) 
		else:
			self.result.append(None)	
		
		if len(self.stat.curselection()) !=0:
			self.result.append(self.stat.curselection()[0]) 
		else:
			self.result.append(None)	

class PlotClusterDialog(Dialog):
	#This class creates a data-axis distribution dialog
	def __init__(self, parent,	headers, title = None):
		self.headers = headers
		Dialog.__init__( self, parent, title )
		

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="X axis:").grid(row=0)
		Label(master, text="Y axis:").grid(row=1)
		Label(master, text="Z axis:").grid(row=0,column=2)
		Label(master, text="Size:").grid(row=1,column=2)
		
		
		self.xbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)-1):
			self.xbox.insert(i,self.headers[i].strip())
		self.xbox.grid(row=0,column=1)
		
		self.ybox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)-1):
			self.ybox.insert(i,self.headers[i].strip())
		self.ybox.grid(row=1,column=1)
		
		self.zbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)-1):
			self.zbox.insert(i,self.headers[i].strip())
		self.zbox.grid(row=0,column=3)
		
		self.size = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)-1):
			self.size.insert(i,self.headers[i].strip())
		self.size.grid(row=1,column=3)
		
		self.var = tk.IntVar()
		check = Checkbutton(master, text="Use Preselected Colors", variable=self.var)
		check.grid(row=3,column=1,columnspan=2)

	def apply(self):
		
		self.result=[]
		if len(self.xbox.curselection()) !=0:
			self.result.append(self.xbox.curselection()[0])
		else:
			self.result.append(None)	
			
		if len(self.ybox.curselection()) !=0:
			self.result.append(self.ybox.curselection()[0]) 
		else:
			self.result.append(None)		
		
		if len(self.zbox.curselection()) !=0:
			self.result.append(self.zbox.curselection()[0]) 
		else:
			self.result.append(None)	
		
		if len(self.size.curselection()) !=0:
			self.result.append(self.size.curselection()[0]) 
		else:
			self.result.append(None)	
			
		self.var=self.var.get()		
		
		
	
class ShapeDialog(Dialog):
	#this class creates a shape dialog
	def __init__(self, parent, title = None):
		Dialog.__init__( self, parent, title )

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="Shape").grid(row=0)
		
		
		self.xbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		self.xbox.insert(1,"Circle")
		self.xbox.insert(2,"Rectangle")
		self.xbox.insert(3,"Arc")
		self.xbox.grid(row=0,column=1)

		
	
	def apply(self):
		self.result=(self.xbox.curselection()[0])			

class InputDialog(Dialog):
	#this class creates a shape dialog
	def __init__(self, parent, title = None):
		Dialog.__init__( self, parent, title )

	def body(self, master):
	# create dialog body.  return widget that should have
		
		Label(master, text="Name").grid(row=0)
		self.e1 = Entry(master)
		self.e1.grid(row=1)

		
	
	def apply(self):
		self.result=self.e1.get()	
	
class LinearDialog(Dialog):
	#This class creates a data-axis distribution dialog
	def __init__(self, parent,	headers, title = None):
		self.headers = headers
		Dialog.__init__( self, parent, title )
		

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="X axis:").grid(row=0)
		Label(master, text="Y axis:").grid(row=1)
		Label(master, text="Size:").grid(row=0,column=2)
		Label(master, text="Color:").grid(row=1,column=2)
		
		
		self.xbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.xbox.insert(i,self.headers[i].strip())
		self.xbox.grid(row=0,column=1)
		
		self.xbox.select_set(0)
		self.xbox.event_generate("<<ListboxSelect>>")
		
		self.ybox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.ybox.insert(i,self.headers[i].strip())
		self.ybox.grid(row=1,column=1)
		
		self.ybox.select_set(0)
		self.ybox.event_generate("<<ListboxSelect>>")
		
		
		self.size = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.size.insert(i,self.headers[i].strip())
		self.size.grid(row=0,column=3)
		
		self.color = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.color.insert(i,self.headers[i].strip())
		self.color.grid(row=1,column=3)
		

	def apply(self):
		
		self.result=[]
		self.result.append(self.xbox.curselection()[0])

		self.result.append(self.ybox.curselection()[0]) 
		
		
		if len(self.size.curselection()) !=0:
			self.result.append(self.size.curselection()[0]) 
		else:
			self.result.append(None)	
		
		if len(self.color.curselection()) !=0:
			self.result.append(self.color.curselection()[0]) 
		else:
			self.result.append(None)	

class PCAwindow(Dialog):
	#this class creates a PCA window
	def __init__(self, parent, data, title = None):
		self.data=data
		Dialog.__init__( self, parent, title )
		

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="E-vec", borderwidth=3).grid(row=0,column=0)
		for i in range(len(self.data.get_headers())):
			Label(master, text=self.data.get_headers()[i], borderwidth=3).grid(row=i+1,column=0)
		
		Label(master, text="E-val", borderwidth=3).grid(row=0,column=1)
		sum=0
		for i in range(len(self.data.get_eigenvalues())):
			Label(master, text=str(round(self.data.get_eigenvalues()[i],4)), borderwidth=3).grid(row=i+1,column=1)	
			sum += self.data.get_eigenvalues()[i]
		
		Label(master, text="Cumulative", borderwidth=3).grid(row=0,column=2)
		Cumusum=0
		for i in range(len(self.data.get_eigenvalues())):
			Cumusum+=self.data.get_eigenvalues()[i]/sum
			Label(master, text=str(round(Cumusum,4)), borderwidth=3).grid(row=i+1,column=2)	
		
		for i in range(len(self.data.get_data_headers())):
			Label(master, text=self.data.get_data_headers()[i], borderwidth=3).grid(row=0,column=i+3)	
		evec=self.data.get_eigenvectors()
		for i in range (len(evec)):
			for j in range(len(self.data.get_eigenvectors())):
				Label(master, text=str(round(evec.item(i,j),4)), borderwidth=3).grid(row=i+1,column=j+3)	
		
		
class MultiLinearDialog(Dialog):
	#This class creates a data-axis distribution dialog
	def __init__(self, parent,	headers, title = None):
		self.headers = headers
		Dialog.__init__( self, parent, title )
		

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="X axis:").grid(row=0)
		Label(master, text="Y axis:").grid(row=1)
		Label(master, text="Z axis:").grid(row=2)
		Label(master, text="Size:").grid(row=0,column=2)
		Label(master, text="Color:").grid(row=1,column=2)
		
		
		self.xbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.xbox.insert(i,self.headers[i].strip())
		self.xbox.grid(row=0,column=1)
		
		self.xbox.select_set(0)
		self.xbox.event_generate("<<ListboxSelect>>")
		
		self.ybox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.ybox.insert(i,self.headers[i].strip())
		self.ybox.grid(row=1,column=1)
		
		self.ybox.select_set(0)
		self.ybox.event_generate("<<ListboxSelect>>")
		
		self.zbox = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.zbox.insert(i,self.headers[i].strip())
		self.zbox.grid(row=2,column=1)
		
		self.zbox.select_set(0)
		self.zbox.event_generate("<<ListboxSelect>>")
		
		self.size = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.size.insert(i,self.headers[i].strip())
		self.size.grid(row=0,column=3)
		
		self.color = Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		for i in range (len(self.headers)):
			self.color.insert(i,self.headers[i].strip())
		self.color.grid(row=1,column=3)
		

	def apply(self):
		
		self.result=[]
		self.result.append(self.xbox.curselection()[0])

		self.result.append(self.ybox.curselection()[0]) 
		
		self.result.append(self.zbox.curselection()[0]) 
		
		if len(self.size.curselection()) !=0:
			self.result.append(self.size.curselection()[0]) 
		else:
			self.result.append(None)	
		
		if len(self.color.curselection()) !=0:
			self.result.append(self.color.curselection()[0]) 
		else:
			self.result.append(None)		
			
class PCADialog(Dialog):
	#this class creates a shape dialog
	def __init__(self, parent,	headers, title = None):
		self.headers = headers
		Dialog.__init__( self, parent, title )

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="PCA").grid(row=0)
		
		
		self.xbox = Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
		for i in range (len(self.headers)):
			self.xbox.insert(i,self.headers[i].strip())
		self.xbox.grid(row=0,column=1)
		self.var = tk.IntVar()
		check = Checkbutton(master, text="Normalize", variable=self.var)
		check.grid(row=2,column=1)

		
	
	def apply(self):
		self.result=self.xbox.curselection()
		self.var=self.var.get()	
		
class ClusterDialog(Dialog):
	#this class creates a shape dialog
	def __init__(self, parent,	headers, title = None):
		self.headers = headers
		Dialog.__init__( self, parent, title )

	def body(self, master):
	# create dialog body.  return widget that should have
	
		Label(master, text="Cluster").grid(row=0)
		
		
		self.xbox = Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
		for i in range (len(self.headers)):
			self.xbox.insert(i,self.headers[i].strip())
		self.xbox.grid(row=0,column=1)	
		
		Label(master, text="Number of Clusters").grid(row=1)
		self.e1 = Entry(master)
		self.e1.grid(row=1,column=1)	
		
		Label(master, text="Norm (default is 2):").grid(row=2)
		self.e2 = Entry(master)
		self.e2.grid(row=2,column=1)	
		
			
		
	
	def apply(self):
		self.result=self.xbox.curselection()
		try:
			num=int(self.e1.get())
		except:
			num=-1
		self.num=num	
		try:
			norm=int(self.e2.get())
		except:
			norm=2
		self.norm=norm	
			
class DisplayApp:
# create a class to build and manage the display
	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()
		# make a new View object
		self.view = view.View()
		# width and height of the window
		self.initDx = width
		self.initDy = height
		
		self.original=None
		
		#the shape of the data point, preset to circle
		self.shape=0
		
		self.degree=(0,0)
		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title("Touch Your Data")

		# set the maximum size of the window for resizing
		self.root.maxsize( 1600, 900 )

		# setup the menus
		self.buildMenus()

		# build the controls
		self.buildControls()

		# build the Canvas
		self.buildCanvas()

		# bring the window to the front
		self.root.lift()

		# - do idle events here to get actual canvas size
		self.root.update_idletasks()

		# now we can ask the size of the canvas
		print self.canvas.winfo_geometry()

		# set up the key bindings
		self.setBindings()

		# set up the application state
		self.objects = [] # list of data objects that will be drawn in the canvas
		
		
		self.baseClick = None # used to keep track of mouse movement
		
		self.colorObj=[]
		
		self.axes = np. matrix([[0, 0, 0, 1], [1, 0, 0, 1], [0, 0, 0, 1], [0, 1, 0, 1],
								[0, 0, 0, 1], [0, 0, 1, 1]])

		self.line = []
		self.buildAxes()
		#self.buildPoints()
		self.data=None
		self.oriData=None
		
		self.size = []
		self.text=[]
		
		'''fields regarding linear regression'''
		self.linear = []
		self.endPoints = None
		self.MultiendPoints = None
		self.Multilinear = []
		
		self.regText=[]
		
		self.axisLabel=[]
		
		self.previousAnalysis=[]
		self.count = -1
		
		self.filename="test.txt"
		self.PCAfilename="test.csv"
		
		'''fields regarding PCA'''
		self.PCAlist = []
		
		'''fields regarding cluster'''
		self.clusterList = []
		self.codebook = []
		self.codeLabel = []
		
		self.classifier = None
		
	#enable the user to select which columns of data to plot on which axes and then builds the data.
	def handlePlotData(self, Original=True):
		if(Original):
			if self.oriData == None:
				print "please enter data"
				return 
			self.data=self.oriData.clone()
			
		if self.data == None:
			print "please enter data"
			return 
		headers=self.data.get_headers()
		self.result=self.handleChooseAxes()
		if self.result == "cancel":
			print "selection cancelled"
			return 
		self.clearData()	
			
		selection=[]
		for i in range (3):
			if self.result[i]!=None:
				selection.append(headers[self.result[i]])
			else: 
				selection.append(None)
		
				
		self.buildPoints(selection) 
		self.buildStat()
	
	
	def handlePlotMixed(self):
		if self.oriData == None:
			print "please enter data"
			return 
		self.data=self.oriData.clone()
			
		PCAdata=self.data
		headers=PCAdata.get_headers()
		DDialog=PCADialog(self.canvas,headers,"Choose Column")
		PCAselection=DDialog.result	
		
		#If the user selects Cancel, the process should terminate 
		#and the existing display should not change.
		if PCAselection == "cancel" or PCAselection == None:
			print "selection cancelled"
			return 
			
		selection=[]
		for i in range (len(PCAselection)):
			selection.append(headers[PCAselection[i]])
		
		if DDialog.var==1:
			PCAdata = analysis.pca(PCAdata,selection)
				
		else :
			PCAdata = analysis.pca(PCAdata,selection,normalize=False)	
		
		self.data.merge_data(PCAdata)
		self.handlePlotData(Original=False)		
			
		
	#Let user choose the PCA they want to represent		
	def handlePCA(self):
		# Create a dialog class that lets the user select an independent (x) variable 
		# 	and a dependent (y) variable.
		fn = tkFileDialog.askopenfilename( parent=self.root,
		title='Choose a data file', initialdir='.' )
		PCAdata=data.Data( fn )
		if PCAdata == None:
			print "please enter data"
			return 
		headers=PCAdata.get_headers()
		DDialog=PCADialog(self.canvas,headers,"Choose Column")
		PCAselection=DDialog.result	
		
		#If the user selects Cancel, the process should terminate 
		#and the existing display should not change.
		if PCAselection == "cancel" or PCAselection == None:
			print "selection cancelled"
			return 
			
		selection=[]
		for i in range (len(PCAselection)):
			selection.append(headers[PCAselection[i]])
		
		if DDialog.var==1:
			PCAdata = analysis.pca(PCAdata,selection)
		else :
			PCAdata = analysis.pca(PCAdata,selection,normalize=False)
				
		self.PCAlist.append(PCAdata)
		
		inputbox = InputDialog(self.canvas)
		
		if inputbox.result=="cancel":
			self.pcalistbox.insert(tk.END, "Not Named")	 
		
		else: 
			self.pcalistbox.insert(tk.END, inputbox.result)	
		
	def handlePlotPCA(self):
		#plot PCA data
		if not self.pcalistbox.curselection():
			print "Please select a PCA data to plot"
			return
		self.data=self.PCAlist[self.pcalistbox.curselection()[0]]
		self.handlePlotData(Original=False)		
			
	def handleSeeAnalysis(self):
		if not self.pcalistbox.curselection():
			return
		data = 	self.PCAlist[self.pcalistbox.curselection()[0]]	
		PCAwindow(self.canvas,data)
		return 
	
	
	
	def handleWritePCA(self):
		#plot PCA data
		if not self.pcalistbox.curselection():
			return
		data=self.PCAlist[self.pcalistbox.curselection()[0]]
		
		fp=file(self.PCAfilename,'rU+')
		fp.write("E-vec, E-val, Cumulative, ")
		for i in range(len(data.get_data_headers())):
			fp.write(data.get_data_headers()[i]+", ")
		fp.write("\n")	
		
		sum=0
		for i in range(len(data.get_eigenvalues())):
			sum += data.get_eigenvalues()[i]
		
		Cumusum=0	
		for i in range(len(data.get_eigenvalues())):
			fp.write(data.get_headers()[i]+", ")
			fp.write(str(round(data.get_eigenvalues()[i],4))+", ")
			Cumusum+=data.get_eigenvalues()[i]/sum
			fp.write(str(round(Cumusum,4))+", ")
			for j in range(len(data.get_eigenvectors())):
				fp.write(str(round(data.get_eigenvectors().item(i,j),4))+", ")
			fp.write("\n")			
		fp.close()
	
	
	
	
	#let the user select the variables to fit and then display the linear regression of them on the main screen.
	def handleMultiLinearRegression(self):
	
		# Create a dialog class that lets the user select an independent (x) variable 
		# 	and a dependent (y) variable.
		if self.data == None:
			print "please enter data"
			return 
		headers=self.data.get_headers()
		self.MultiLinearResult=self.handleMultiLinear()
		
		#If the user selects Cancel, the process should terminate 
		#and the existing display should not change.
		if self.MultiLinearResult == "cancel":
			print "selection cancelled"
			return 
						
		selection=[]
		for i in range (3):
			if self.MultiLinearResult[i]!=None:
				selection.append(headers[self.MultiLinearResult[i]])
			else: 
				selection.append(None)
		
		
		# '''Clear the existing points from the window'''
		self.clearData()
		
		# '''Clear any existing data fits or models from the window.'''
		self.Multilinear = []
		self.endPoints = None
			
		self.reset()
		
		self.updateAxes()
		
		self.buildMultiLinearRegression(selection)
	
	def buildMultiLinearRegression(self,headers):
		matrix=analysis.normalize_columns_separately(headers,self.data).A
		
		homo=[]
		for i in range (len(matrix.tolist()[0])):
			homo.append(1.0)
		
		old = np.array(matrix)		
		matrix=np.vstack((old,homo))
		self.matrix = matrix
		matrix=self.matrix.copy()		
		matrix=self.view.build() * matrix
		self.Paheaders=headers
		#relate the size to the data
		self.size=[]
		if self.MultiLinearResult[3]!=None:
			smatrix=np.matrix(self.data.get_column(self.MultiLinearResult[2]))
			max=np.max(smatrix[0,:])
			min=np.min(smatrix[0,:])
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()[0]
			
			for i in range (len(slist)):
				self.size.append(3*math.sqrt(slist[i])+2)
		else:
			slist=self.data.get_column(0)
			for i in range (len(slist)):
				self.size.append(2)		
		
		#relate the color to the data
		self.color=[]
		if self.MultiLinearResult[4]!=None:
			smatrix=np.matrix(self.data.get_column(self.MultiLinearResult[3]))
			max=np.max(smatrix[0,:])
			min=np.min(smatrix[0,:])
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()[0]
			
			for i in range (len(slist)):
				co=slist[i]*250
				self.color.append('#%02x%02x%02x'%(int(250-co),int(250-co),int(co)))
				
			#paint the legend
			co=250
			x=self.initDx-250
			y=50
			dx=15
			erro=(max-min)/float(5)			
			for i in range (6):
				pt = self.canvas.create_rectangle( x-dx-50, y-dx, x+dx-35, y+dx,
											  fill='#%02x%02x%02x'%(int(250-co),int(250-co),int(co)), outline='' )
				self.colorObj.append(self.canvas.create_text(x,y,text=str(max),anchor=tk.SW))							  
				co-=50
				y+=50	
				max-=erro	
				self.colorObj.append(pt)									  				
				
		
		else:
			slist=self.data.get_column(0)
			for i in range (len(slist)):
				self.color.append("black")		
		
		if self.shape==0:	
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_oval( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)			
				
		elif self.shape==1:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_rectangle( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt) 
				
		elif self.shape==2:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_arc( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)
		
		'''Use the analysis.linear_regression function to calculate the 
			linear regression of the independent and dependent variables.'''
		b, sse, r2, t, p = analysis.linear_regression(self.data, [headers[0],headers[2]],headers[1])
		
		drange = analysis.data_range(headers,self.data)
		xmin=drange[0][1]
		xmax=drange[0][0]
		ymin=drange[1][1]
		ymax=drange[1][0]
		zmin=drange[2][1]
		zmax=drange[2][0]
		end1=[0.0,((xmin * b[0] + zmin*b[1]+b[2]) - ymin)/(ymax - ymin),0.0,1]
		end2=[1.0,((xmax * b[0] + zmin*b[1]+b[2]) - ymin)/(ymax - ymin),0.0,1]
		end3=[0.0,((xmin * b[0] + zmax*b[1]+b[2]) - ymin)/(ymax - ymin),1.0,1]
		end4=[1.0,((xmax * b[0] + zmax*b[1]+b[2]) - ymin)/(ymax - ymin),1.0,1]
		
		self.MultiendPoints = np. matrix([end1,end2,end3,end4])
		vtm=self.view.build()
		pts = (vtm * self.MultiendPoints.T).T
		#create three new line objects, one for each axis.
		self.Multilinear=[]
		self.Multilinear.append(self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1],fill="red"))
		self.Multilinear.append(self.canvas.create_line(pts[1,0],pts[1,1],pts[3,0],pts[3,1],fill="red"))
		self.Multilinear.append(self.canvas.create_line(pts[0,0],pts[0,1],pts[2,0],pts[2,1],fill="red"))
		self.Multilinear.append(self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1],fill="red"))
		self.regText=[]
		self.regText.append(self.canvas.create_text(900,450,text="m0: "+str(b[0][0])))	
		self.regText.append(self.canvas.create_text(900,500,text="m1: "+str(b[1][0])))		
		self.regText.append(self.canvas.create_text(900,550,text="intercept: "+str(b[2][0]))	)
		self.regText.append(self.canvas.create_text(900,600,text="r^2: "+str(r2)))	
		
		'''extension 2'''
		vtm=self.view.build()
		pts = (vtm * self.axes.T).T
		
		drange = analysis.data_range(headers,self.data)
		xmin=drange[0][1]
		xmax=drange[0][0]
		ymin=drange[1][1]
		ymax=drange[1][0]
		zmin=drange[2][1]
		zmax=drange[2][0]
		self.axisLabel=[]
# 		self.axisLabel.append(self.canvas.create_text(pts[1,0],pts[1,1],text=str(xmax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[3,0],pts[3,1],text=str(ymax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[5,0],pts[5,1],text=str(zmax),anchor=tk.NE))
		self.axisLabel.append(self.canvas.create_text((pts[1,0]+pts[0,0])/2,(pts[1,1]+pts[0,1])/2,text=headers[0],anchor=tk.SW))	
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,2)[0],self.getPosition(pts,0.5,2)[1],text=headers[1],anchor=tk.SW))
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,4)[0],self.getPosition(pts,0.5,4)[1],text=headers[2],anchor=tk.SW))
		
		for i in range (10):
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,0)[0],self.getPosition(pts,1.0/10*i,0)[1],text=round(xmin+(xmax-xmin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,2)[0],self.getPosition(pts,1.0/10*i,2)[1],text=round(ymin+(ymax-ymin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,4)[0],self.getPosition(pts,1.0/10*i,4)[1],text=round(zmin+(zmax-zmin)*i/10.0,1),anchor=tk.NE))	
		
		self.previousAnalysis.append([headers[0],headers[2],headers[1],b , sse, r2, t, p])		
		self.count+=1	
	
	def handleLinearRegression(self):
	
		'''Create a dialog class that lets the user select an independent (x) variable 
			and a dependent (y) variable.'''
		if self.data == None:
			print "please enter data"
			return 
		headers=self.data.get_headers()
		self.LinearResult=self.handleLinear()
	
		'''If the user selects Cancel, the process should terminate 
			and the existing display should not change.'''
		if self.LinearResult == "cancel":
			print "selection cancelled"
			return 
					
		selection=[]
		for i in range (2):
			if self.LinearResult[i]!=None:
				selection.append(headers[self.LinearResult[i]])
			else: 
				selection.append(None)
	
	
		'''Clear the existing points from the window'''
		self.clearData()
	
		'''Clear any existing data fits or models from the window.'''
		self.linear = []
		self.endPoints = None
		
		self.reset()
	
		self.updateAxes()
	
		self.buildLinearRegression(selection)
	
	#plot the data in the cluster box
	def handlePlotCluster(self):
		if not self.clusterbox.curselection():
			print "Please select a cluster to plot"
			return
			
		self.data=self.clusterList[self.clusterbox.curselection()[0]]
		
		#this act as plot data
		headers=self.data.get_headers()
		DDialog=PlotClusterDialog(self.canvas,self.data.get_headers(),"Choose Axis")
		self.result=DDialog.result
		if self.result == "cancel":
			print "selection cancelled"
			return 
		self.clearData()	
			
		selection=[]
		for i in range (3):
			if self.result[i]!=None:
				selection.append(headers[self.result[i]])
			else: 
				selection.append(None)
		
		for item in self.colorObj:
			self.canvas.delete(item)
		self.colorObj=[]
		
		for item in self.objects:
			self.canvas.delete(item)
		self.objects=[]
		
		self.matrix=self.data.get_data(selection) 
		homo=[]
		for i in range (len(self.matrix.tolist()[0])):
			homo.append(1.0)
		old = np.array(self.matrix)		
		self.matrix=np.vstack((old,homo))
		
		for i in range (len(selection)):	
			max=np.max(self.matrix[i,:])
			min=np.min(self.matrix[i,:])
			self.matrix[i,:]-=min
			if(max-min!=0):
				self.matrix[i,:]/=(max-min)
				
		matrix=self.matrix.copy()		
		matrix=self.view.build() * matrix
		
		
		#relate the size to the data
		self.size=[]
		if self.result[3]!=None:
			smatrix=np.matrix(self.data.get_column(self.result[3]))
			max=np.max(smatrix[0,:])
			min=np.min(smatrix[0,:])
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()
			if(len(slist)==1):
				slist=slist[0]
			
			for i in range (len(slist)):
				self.size.append(3*math.sqrt(slist[i])+2)
		else:
			slist=self.data.get_column(0)
			for i in range (len(slist)):
				self.size.append(2)		
		
		#relate the color to the data
		self.color=[]
		smatrix=np.matrix(self.data.get_column(self.data.get_num_columns()-1))
		max=int(np.max(smatrix[0,:]))
		min=int(np.min(smatrix[0,:]))
		
		
		#if not preselected, use smooth
		if DDialog.var == 0:
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()[0]
			
			for i in range (len(slist)):
				co=slist[i]*250
				self.color.append('#%02x%02x%02x'%(int(250-co),int(250-co),int(co)))
			
			'''extension'''
			#paint the legend
			co=0
			x=self.initDx-450
			y=50
			dx=15
			erro=1
			difference = float(max-min)	
			for i in range (max-min+1):
				pt = self.canvas.create_rectangle( x-dx-50, y-dx, x+dx-35, y+dx,
											  fill='#%02x%02x%02x'%(int(250-co),int(250-co),int(co)), outline='' )
				self.colorObj.append(self.canvas.create_text(x-150,y+5,text="cluster "+str(i)+": ",anchor=tk.SW))	
									  
				co+=250/difference
				y+=50	
				max-=erro	
				self.colorObj.append(pt)									  				
				
		# else, use preselected color
		else:
			colorset = ['blue','green','red','cyan','magenta','yellow','black']
			slist=smatrix.tolist()[0]
			
			for i in range (len(slist)):
				self.color.append(colorset[int(slist[i]%7)])
			
			#paint the legend
			x=self.initDx-450
			y=50
			dx=15
			for i in range (max-min+1):
				pt = self.canvas.create_rectangle( x-dx-50, y-dx, x+dx-35, y+dx,
											  fill=colorset[i%7])
				self.colorObj.append(self.canvas.create_text(x-150,y+5,text="cluster "+str(i)+": ",anchor=tk.SW))		
				y+=50	
				self.colorObj.append(pt)	
		
		
				

		if self.shape==0:	
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_oval( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)			
				
		elif self.shape==1:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_rectangle( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt) 
				
		elif self.shape==2:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_arc( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)		
		
		vtm=self.view.build()
		pts = (vtm * self.axes.T).T
		
		drange = analysis.data_range(selection,self.data)
		xmin=drange[0][1]
		xmax=drange[0][0]
		ymin=drange[1][1]
		ymax=drange[1][0]
		zmin=drange[2][1]
		zmax=drange[2][0]
		
		
		self.axisLabel=[]
# 		self.axisLabel.append(self.canvas.create_text(pts[1,0],pts[1,1],text=str(xmax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[3,0],pts[3,1],text=str(ymax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[5,0],pts[5,1],text=str(zmax),anchor=tk.NE))
		self.axisLabel.append(self.canvas.create_text((pts[1,0]+pts[0,0])/2,(pts[1,1]+pts[0,1])/2,text=selection[0],anchor=tk.SW))	
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,2)[0],self.getPosition(pts,0.5,2)[1],text=selection[1],anchor=tk.SW))
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,4)[0],self.getPosition(pts,0.5,4)[1],text=selection[2],anchor=tk.SW))
		
		for k in range (10):
			i=k+1
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,0)[0],self.getPosition(pts,1.0/10*i,0)[1],text=round(xmin+(xmax-xmin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,2)[0],self.getPosition(pts,1.0/10*i,2)[1],text=round(ymin+(ymax-ymin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,4)[0],self.getPosition(pts,1.0/10*i,4)[1],text=round(zmin+(zmax-zmin)*i/10.0,1),anchor=tk.NE))			
		self.Paheaders=selection
		
		'''print the mean point'''
		
		codebook=self.codebook[self.clusterbox.curselection()[0]]
		
		y=50
		for k in range (codebook.shape[0]):
			x=self.initDx-450
			for i in range(codebook.shape[1]):
				self.codeLabel.append(self.canvas.create_text(x,y,text=str(round(codebook[k,i],2))+" ",anchor=tk.SW))
				x+=35
			y+=50	
	
	#put a data in the cluster box
	def handleCluster(self):
		if self.data == None:
			print "please enter data"
			return 
		data=self.data.clone()
		
		headers=data.get_headers()
		
		DDialog=ClusterDialog(self.canvas,headers,"Choose Column")
		result=DDialog.result
		
		#If the user selects Cancel, the process should terminate 
		#and the existing display should not change.
		if result == "cancel" or result == None:
			print "selection cancelled"
			return 
		
		
		
		selection=[]
		for i in range (len(result)):
			selection.append(headers[result[i]])
		
		K=DDialog.num
		if K<0:
			print "wrong number"
			return
		codebook, codes, errors=analysis.kmeans(data, selection, K, norm = DDialog.norm)
		data.addColumn("ID","numeric",codes.T.A[0])
		
		self.clusterList.append(data)
		self.codebook.append(codebook)
			
		inputbox = InputDialog(self.canvas)
		
		if inputbox.result=="cancel":
			self.clusterbox.insert(tk.END, "Not Named")	 
		
		else: 
			self.clusterbox.insert(tk.END, inputbox.result)	
		
			
	
	def buildLinearRegression(self,headers):
		self.Paheaders=headers
		matrix=analysis.normalize_columns_separately(headers,self.data).A
		
		matrix=np.vstack((matrix,np.zeros(len(matrix.tolist()[0]))))
		
		homo=[]
		for i in range (len(matrix.tolist()[0])):
			homo.append(1.0)
		
		old = np.array(matrix)		
		matrix=np.vstack((old,homo))
		self.matrix = matrix
		matrix=self.matrix.copy()		
		matrix=self.view.build() * matrix
		
		#relate the size to the data
		self.size=[]
		if self.LinearResult[2]!=None:
			smatrix=np.matrix(self.data.get_column(self.LinearResult[2]))
			max=np.max(smatrix[0,:])
			min=np.min(smatrix[0,:])
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()[0]
			
			for i in range (len(slist)):
				self.size.append(3*math.sqrt(slist[i])+2)
		else:
			slist=self.data.get_column(0)
			for i in range (len(slist)):
				self.size.append(2)		
		
		#relate the color to the data
		self.color=[]
		if self.LinearResult[3]!=None:
			smatrix=np.matrix(self.data.get_column(self.LinearResult[3]))
			max=np.max(smatrix[0,:])
			min=np.min(smatrix[0,:])
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()[0]
			
			for i in range (len(slist)):
				co=slist[i]*250
				self.color.append('#%02x%02x%02x'%(int(250-co),int(250-co),int(co)))
				
			#paint the legend
			co=250
			x=self.initDx-250
			y=50
			dx=15
			erro=(max-min)/float(5)			
			for i in range (6):
				pt = self.canvas.create_rectangle( x-dx-50, y-dx, x+dx-35, y+dx,
											  fill='#%02x%02x%02x'%(int(250-co),int(250-co),int(co)), outline='' )
				self.colorObj.append(self.canvas.create_text(x,y,text=str(max),anchor=tk.SW))							  
				co-=50
				y+=50	
				max-=erro	
				self.colorObj.append(pt)									  				
				
		
		else:
			slist=self.data.get_column(0)
			for i in range (len(slist)):
				self.color.append("black")		
		
		if self.shape==0:	
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_oval( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)			
				
		elif self.shape==1:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_rectangle( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt) 
				
		elif self.shape==2:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_arc( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)
		
		'''Use the scipy.stats.linregress (import scipy.stats) function to calculate the 
			linear regression of the independent and dependent variables.		'''
		slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(self.data.get_data(headers).A)
		
		drange = analysis.data_range(headers,self.data)
		xmin=drange[0][1]
		xmax=drange[0][0]
		ymin=drange[1][1]
		ymax=drange[1][0]
			
		
		if len(self.Paheaders)==2:
			self.Paheaders.append(None)
		
		self.endPoints = np. matrix([[0.0, ((xmin * slope + intercept) - ymin)/(ymax - ymin),0.0,1],
							[1.0,((xmax * slope + intercept) - ymin)/(ymax - ymin),0.0,1]])
		vtm=self.view.build()
		pts = (vtm * self.endPoints.T).T
		#create three new line objects, one for each axis.
		self.linear=[]
		self.linear.append(self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1],fill="red"))
		self.regText=[]
		self.regText.append(self.canvas.create_text(900,500,text="slope: "+str(slope)))		
		self.regText.append(self.canvas.create_text(900,550,text="intercept: "+str(intercept))	)
		self.regText.append(self.canvas.create_text(900,600,text="r^2: "+str(r_value*r_value)))		
		vtm=self.view.build()
		pts = (vtm * self.axes.T).T
		
		drange = analysis.data_range(headers,self.data)
		xmin=drange[0][1]
		xmax=drange[0][0]
		ymin=drange[1][1]
		ymax=drange[1][0]
		zmin=drange[2][1]
		zmax=drange[2][0]
		'''extension 2'''
		self.axisLabel=[]
# 		self.axisLabel.append(self.canvas.create_text(pts[1,0],pts[1,1],text=str(xmax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[3,0],pts[3,1],text=str(ymax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[5,0],pts[5,1],text=str(zmax),anchor=tk.NE))
		self.axisLabel.append(self.canvas.create_text((pts[1,0]+pts[0,0])/2,(pts[1,1]+pts[0,1])/2,text=headers[0],anchor=tk.SW))	
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,2)[0],self.getPosition(pts,0.5,2)[1],text=headers[1],anchor=tk.SW))
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,4)[0],self.getPosition(pts,0.5,4)[1],text=headers[2],anchor=tk.SW))
		
		for i in range (10):
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,0)[0],self.getPosition(pts,1.0/10*i,0)[1],text=round(xmin+(xmax-xmin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,2)[0],self.getPosition(pts,1.0/10*i,2)[1],text=round(ymin+(ymax-ymin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,4)[0],self.getPosition(pts,1.0/10*i,4)[1],text=round(zmin+(zmax-zmin)*i/10.0,1),anchor=tk.NE))	
		
		self.previousAnalysis.append(["Linear",headers[0],headers[1],slope, intercept, r_value, p_value, std_err])		
		self.count+=1			
			
	#Make use of your anlaysis functions and let the user view data properties like 
	#the mean, standard deviaion, and range of selected columns.
	def buildStat(self):
		for item in self.text:
			self.canvas.delete(item)
		self.text=[]
		if self.result[5]==None:
			return
		else:
			mean  = float(analysis.mean([self.data.get_headers()[self.result[5]]],self.data)[0])	
			range = analysis.data_range([self.data.get_headers()[self.result[5]]],self.data)[0]	
			stdev = float(analysis.stdev([self.data.get_headers()[self.result[5]]],self.data)[0])	
			self.text.append(self.canvas.create_text(800,50,text="mean: "+str(round(mean,2))))
			self.text.append(self.canvas.create_text(800,100,text="range: ["+str(round(range[1],2))+", "+str(round(range[0],2))+ "]"))
			self.text.append(self.canvas.create_text(800,150,text="stdev: "+str(round(stdev,2))))
	
	# use the tkFileDialog module to let the user select the csv file they want to open.	
	def handleOpen(self, event = None):
		fn = tkFileDialog.askopenfilename( parent=self.root,
		title='Choose a data file', initialdir='.' )
		self.data = data.Data( fn )
		self.oriData=self.data.clone()
	
	#build a classifier using the data inputed by the user
	def buildClassifier(self):
		traind = tkFileDialog.askopenfilename( parent=self.root,
		title='Choose training file', initialdir='.' )
		trainc = tkFileDialog.askopenfilename( parent=self.root,
		title='Choose training category file', initialdir='.' )
		
		trdata = data.Data(traind)
		trc = data.Data(trainc)
	
		A = trdata.get_data( trdata.get_headers() ).T
		traincats = trc.get_data( [trc.get_headers()[0]] ).T
	
		self.classifier = classifiers.NaiveBayes(dataObj=trdata, headers=trdata.get_headers(), categories=traincats)
	
	#classify self.data and store it in the cluster box
	def classify(self):
		if self.classifier is None:
			return
		if self.data is None:
			return	
		A=self.data.get_data(self.data.get_headers()).T
		cats, labels = self.classifier.classify(A)
		self.data.addColumn("ID","numeric",cats.T.A[0])
		
		self.clusterList.append(self.data.clone())
		self.codebook.append(cats)
			
		inputbox = InputDialog(self.canvas)
		
		if inputbox.result=="cancel":
			self.clusterbox.insert(tk.END, "Not Named")	 
		
		else: 
			self.clusterbox.insert(tk.END, inputbox.result)	
		
		
		
	#take in a list of headers, delete any existing canvas objects representing data, 
	#and then create a build a new set of data points.
	def buildPoints(self,headers):
		#Delete any existing canvas objects used for plotting data.	
		for item in self.colorObj:
			self.canvas.delete(item)
		self.colorObj=[]
		
		for item in self.objects:
			self.canvas.delete(item)
		self.objects=[]
		
		self.matrix=self.data.get_data(headers) 
		homo=[]
		for i in range (len(self.matrix.tolist()[0])):
			homo.append(1.0)
		old = np.array(self.matrix)		
		self.matrix=np.vstack((old,homo))
		
		for i in range (len(headers)):	
			max=np.max(self.matrix[i,:])
			min=np.min(self.matrix[i,:])
			self.matrix[i,:]-=min
			if(max-min!=0):
				self.matrix[i,:]/=(max-min)
				
		matrix=self.matrix.copy()		
		matrix=self.view.build() * matrix
		
		
		#relate the size to the data
		self.size=[]
		if self.result[3]!=None:
			smatrix=np.matrix(self.data.get_column(self.result[3]))
			max=np.max(smatrix[0,:])
			min=np.min(smatrix[0,:])
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()
			if(len(slist)==1):
				slist=slist[0]
			
			for i in range (len(slist)):
				self.size.append(3*math.sqrt(slist[i])+2)
		else:
			slist=self.data.get_column(0)
			for i in range (len(slist)):
				self.size.append(2)		
		
		#relate the color to the data
		self.color=[]
		if self.result[4]!=None:
			smatrix=np.matrix(self.data.get_column(self.result[4]))
			max=np.max(smatrix[0,:])
			min=np.min(smatrix[0,:])
			smatrix[0,:]-=min
			if(max-min!=0):
				smatrix[0,:]/=(max-min)
			slist=smatrix.tolist()[0]
			
			for i in range (len(slist)):
				co=slist[i]*250
				self.color.append('#%02x%02x%02x'%(int(250-co),int(250-co),int(co)))
			
			'''extension 7'''
			#paint the legend
			co=250
			x=self.initDx-450
			y=50
			dx=15
			erro=(max-min)/float(5)			
			for i in range (6):
				pt = self.canvas.create_rectangle( x-dx-50, y-dx, x+dx-35, y+dx,
											  fill='#%02x%02x%02x'%(int(250-co),int(250-co),int(co)), outline='' )
				self.colorObj.append(self.canvas.create_text(x,y,text=str(max),anchor=tk.SW))							  
				co-=50
				y+=50	
				max-=erro	
				self.colorObj.append(pt)									  				
				
		
		else:
			slist=self.data.get_column(0)
			for i in range (len(slist)):
				self.color.append("black")	
		
		
		
				

		if self.shape==0:	
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_oval( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)			
				
		elif self.shape==1:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_rectangle( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt) 
				
		elif self.shape==2:
			for i in range (len(self.matrix.T)):
				pt = self.canvas.create_arc( matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], 
											  matrix[0,i]+self.size[i], matrix[1,i]+self.size[i],
											  fill=self.color[i], outline='' )		
				self.objects.append(pt)		
		
		vtm=self.view.build()
		pts = (vtm * self.axes.T).T
		
		drange = analysis.data_range(headers,self.data)
		xmin=drange[0][1]
		xmax=drange[0][0]
		ymin=drange[1][1]
		ymax=drange[1][0]
		zmin=drange[2][1]
		zmax=drange[2][0]
		'''extension 2'''
		self.axisLabel=[]
# 		self.axisLabel.append(self.canvas.create_text(pts[1,0],pts[1,1],text=str(xmax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[3,0],pts[3,1],text=str(ymax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[5,0],pts[5,1],text=str(zmax),anchor=tk.NE))
		self.axisLabel.append(self.canvas.create_text((pts[1,0]+pts[0,0])/2,(pts[1,1]+pts[0,1])/2,text=headers[0],anchor=tk.SW))	
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,2)[0],self.getPosition(pts,0.5,2)[1],text=headers[1],anchor=tk.SW))
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,4)[0],self.getPosition(pts,0.5,4)[1],text=headers[2],anchor=tk.SW))
		
		for k in range (10):
			i=k+1
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,0)[0],self.getPosition(pts,1.0/10*i,0)[1],text=round(xmin+(xmax-xmin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,2)[0],self.getPosition(pts,1.0/10*i,2)[1],text=round(ymin+(ymax-ymin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,4)[0],self.getPosition(pts,1.0/10*i,4)[1],text=round(zmin+(zmax-zmin)*i/10.0,1),anchor=tk.NE))			
		self.Paheaders=headers
					
	#helper function for extension 2							  
	#return the position of the point on the i line									  
	def getPosition(self, pts, proportion, i):
		xp=pts[i+1,0]-(pts[i+1,0]-pts[i,0])*(1-proportion)
		yp=pts[i+1,1]-(pts[i+1,1]-pts[i,1])*(1-proportion)
		return int(xp),int(yp)
	
	#build a new VTM, use the VTM to transform the matrix of data points, then update the 
	#coordinates of each data point using the canvas.coords function.
	def updatePoints(self):
		
		if len(self.objects)==0:
			return
		matrix=self.view.build() * self.matrix
		for i in range(len(self.objects)):
			self.canvas.coords( self.objects[i], 
						matrix[0,i]-self.size[i], matrix[1,i]-self.size[i], matrix[0,i]+self.size[i], matrix[1,i]+self.size[i] )
		for item in self.axisLabel:
			self.canvas.delete(item)	
		
		self.axisLabel=[]	
		
		headers=self.Paheaders
		vtm=self.view.build()
		pts = (vtm * self.axes.T).T
		
		drange = analysis.data_range(headers,self.data)
		xmin=drange[0][1]
		xmax=drange[0][0]
		ymin=drange[1][1]
		ymax=drange[1][0]
		zmin=drange[2][1]
		zmax=drange[2][0]
		'''extension 2'''
# 		self.axisLabel.append(self.canvas.create_text(pts[1,0],pts[1,1],text=str(xmax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[3,0],pts[3,1],text=str(ymax),anchor=tk.NE))
# 		self.axisLabel.append(self.canvas.create_text(pts[5,0],pts[5,1],text=str(zmax),anchor=tk.NE))
		self.axisLabel.append(self.canvas.create_text((pts[1,0]+pts[0,0])/2,(pts[1,1]+pts[0,1])/2,text=headers[0],anchor=tk.SW))	
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,2)[0],self.getPosition(pts,0.5,2)[1],text=headers[1],anchor=tk.SW))
		self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,0.5,4)[0],self.getPosition(pts,0.5,4)[1],text=headers[2],anchor=tk.SW))
		
		for k in range (10):
			i=k+1
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,0)[0],self.getPosition(pts,1.0/10*i,0)[1],text=round(xmin+(xmax-xmin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,2)[0],self.getPosition(pts,1.0/10*i,2)[1],text=round(ymin+(ymax-ymin)*i/10.0,1),anchor=tk.NE))
			self.axisLabel.append(self.canvas.create_text(self.getPosition(pts,1.0/10*i,4)[0],self.getPosition(pts,1.0/10*i,4)[1],text=round(zmin+(zmax-zmin)*i/10.0,1),anchor=tk.NE))			
						
		
		
	def buildAxes(self):
		vtm=self.view.build()
		pts = (vtm * self.axes.T).T
		#create three new line objects, one for each axis.
		self.line.append(self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1]))
		self.line.append(self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1]))
		self.line.append(self.canvas.create_line(pts[4,0],pts[4,1],pts[5,0],pts[5,1]))
		
		'''extension 6'''
		self.letter=[]
		self.letter.append(self.canvas.create_text(pts[1,0],pts[1,1],text="X",anchor=tk.SW))
		self.letter.append(self.canvas.create_text(pts[3,0],pts[3,1],text="Y",anchor=tk.SW))
		self.letter.append(self.canvas.create_text(pts[5,0],pts[5,1],text="Z",anchor=tk.SW))
		
		
	def updateAxes(self):	
		for object in self.letter:
			self.canvas.delete(object)
		self.canvas.delete(self.line[0])
		self.canvas.delete(self.line[1])
		self.canvas.delete(self.line[2])
		vtm=self.view.build()
		pts = (vtm * self.axes.T).T
		self.line[0]=self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1])
		self.line[1]=self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1])
		self.line[2]=self.canvas.create_line(pts[4,0],pts[4,1],pts[5,0],pts[5,1])
		self.letter=[]
		self.letter.append(self.canvas.create_text(pts[1,0],pts[1,1],text="X",anchor=tk.SW))
		self.letter.append(self.canvas.create_text(pts[3,0],pts[3,1],text="Y",anchor=tk.SW))
		self.letter.append(self.canvas.create_text(pts[5,0],pts[5,1],text="Z",anchor=tk.SW))
	
	def updateFits(self):
		if not self.linear:
			return
		for object in self.linear:
			self.canvas.delete(object)
		vtm=self.view.build()
		pts = (vtm * self.endPoints.T).T	
		self.linear=[]
		self.linear.append(self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1],fill="red"))
	
	def updateMultiFits(self):
		if not self.Multilinear:
			return
		for object in self.Multilinear:
			self.canvas.delete(object)
		vtm=self.view.build()
		pts = (vtm * self.MultiendPoints.T).T	
		self.Multilinear=[]
		self.Multilinear.append(self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1],fill="red"))
		self.Multilinear.append(self.canvas.create_line(pts[1,0],pts[1,1],pts[3,0],pts[3,1],fill="red"))
		self.Multilinear.append(self.canvas.create_line(pts[0,0],pts[0,1],pts[2,0],pts[2,1],fill="red"))
		self.Multilinear.append(self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1],fill="red"))
	

	#reset the view to the default view		
	def reset(self, event=None):
		self.view.reset()
		self.degree=(0,0)
		self.extent=[1,1]
		self.updateAxes()
		self.updateFits()
		self.updateMultiFits()
		self.labell.config(text="Scale:" + str(round(1.0/self.view.extent[0],2))+"	Orientation: "+str(round(self.degree[0],2))+", "+str(round(self.degree[1],2)))
		
		# call updatePoints()
		self.updatePoints()
		print "reset"
	
	'''extension'''
	def savePlot(self):
		#save the plot to a file
		self.canvas.postscript( file = 'photo.ps', colormode = 'color' )
	
	
	#reset the view to yz plane		
	def resetYZ(self, event=None):
		self.view.vrp=np.matrix([1, 0.5, 0.5])
		self.view.vpn=np.matrix([1, 0, 0])
		self.view.vup=np.matrix([0, 0, 1])
		self.view.u=np.matrix([[0, 1, 0]])
		self.degree=(0,0)
		self.extent=[1,1]
		self.updateAxes()
		self.updateFits()
		self.updateMultiFits()
		self.labell.config(text="Scale:" + str(round(1.0/self.view.extent[0],2))+"	Orientation: "+str(round(self.degree[0],2))+", "+str(round(self.degree[1],2)))
		
		# call updatePoints()
		self.updatePoints()
	
	#reset the view to xz plane 
	def resetZX(self, event=None):
		self.view.vrp=np.matrix([0.5, 1, 0.5])
		self.view.vpn=np.matrix([0, 1, 0])
		self.view.vup=np.matrix([1, 0, 0])
		self.view.u=np.matrix([[0, 0, 1]])
		self.degree=(0,0)
		self.extent=[1,1]
		self.updateAxes()
		self.updateFits()
		self.updateMultiFits()
		self.labell.config(text="Scale:" + str(round(1.0/self.view.extent[0],2))+"	Orientation: "+str(round(self.degree[0],2))+", "+str(round(self.degree[1],2)))
		
		# call updatePoints()
		self.updatePoints()
	
	def clearData(self, event=None):
		#clear the canvas
		for item in self.codeLabel:
			self.canvas.delete(item)
		for item in self.linear:
			self.canvas.delete(item)
		self.endPoints=None
		for item in self.Multilinear:
			self.canvas.delete(item)
		self.MultiendPoints=None
		for item in self.regText:
			self.canvas.delete(item)
		for item in self.text:
			self.canvas.delete(item)
		for item in self.objects:
			self.canvas.delete(item)
		for item in self.colorObj:
			self.canvas.delete(item)	
		for item in self.axisLabel:
			self.canvas.delete(item)		
		self.objects=[]
		self.colorObj=[]
		self.linear=[]
		self.Multilinear=[]
		self.axisLabel=[]
		self.codeLabel=[]
	
	

	def buildMenus(self):
		
		# create a new menu
		menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = menu)

		# create a variable to hold the individual menus
		menulist = []

		# create a file menu
		filemenu = tk.Menu( menu )
		menu.add_cascade( label = "File", menu = filemenu )
		menulist.append(filemenu)

		# create another menu for kicks
		cmdmenu = tk.Menu( menu )
		menu.add_cascade( label = "Command", menu = cmdmenu )
		menulist.append(cmdmenu)

		# menu text for the elements
		# the first sublist is the set of items for the file menu
		# the second sublist is the set of items for the option menu
		menutext = [ [ 'Open \xE2\x8C\x98-O', 'New \xE2\x8C\x98-N', 'Quit \xE2\x8C\x98-Q' ],
					 [ 'Set Shape', 'Linear Regression', 'Multiple Linear Regression' ,'PCA'] ]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
		menucmd = [ [self.handleOpen , self.clearData, self.handleQuit],
					[self.handleMenuCmd1, self.handleLinearRegression, self.handleMultiLinearRegression, self.handlePCA] ]
		
		
		# build the menu elements and callbacks
		for i in range( len( menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					menulist[i].add_separator()

	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		return

	# build a frame and put controls in it
	def buildControls(self):
################################################################# right frame ################################################################
		### Control ###
		# make a control frame on the right
		
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
		self.right=rightcntlframe
		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Control Panel", width=20 )
		label.grid(row=0,column=1)

		# make a menubutton
# 		self.colorOption = tk.StringVar( self.root )
# 		self.colorOption.set("black")
# 		colorMenu = tk.OptionMenu( rightcntlframe, self.colorOption, 
# 										"black", "blue", "red", "green" ) # can add a command to the menu
# 		colorMenu.grid(row=2,column=1,pady=10)
		
		
		# make a button in the frame
		# and tell it to call the handleButton method when it is pressed.
# 		button = tk.Button( rightcntlframe, text="Update Color", 
# 							   command=self.handleButton1 )
# 		button.grid(row=4,column=1,pady=10)	  # default side is top
		
		button = tk.Button( rightcntlframe, text="Reset", 
							   command=self.reset)
		button.grid(row=1,column=1,pady=5,ipadx=20)   # default side is top
		
		button = tk.Button( rightcntlframe, text="Plot Data", 
							   command=self.handlePlotData)
		button.grid(row=2,column=1,pady=5)	 # default side is top
		
		
		self.num=tk.Scale(rightcntlframe, from_=1,to=5,orient=tk.HORIZONTAL)
		self.num.grid(row=3,column=1)
		
		numlabel=tk.Label( rightcntlframe, text="speed", width=20 )
		numlabel.grid(row=4,column=1)
		
		# make a button in the frame
		# and tell it to call the handleButton method when it is pressed.
		button = tk.Button( rightcntlframe, text="Save plot", 
							   command=self.savePlot )
		button.grid(row=5,column=1,pady=5,ipadx=10)	  # default side is top
		
		# make a button in the frame
		# and tell it to call the handleButton method when it is pressed.
		button = tk.Button( rightcntlframe, text="Write to File", 
							   command=self.writeToFile )
		button.grid(row=6,column=1,pady=5)	  # default side is top
		
		self.PreAnal=tk.Scale(rightcntlframe, from_=1,to=10,orient=tk.HORIZONTAL)
		self.PreAnal.grid(row=7,column=1)
		
		plabel=tk.Label( rightcntlframe, text="Previous", width=20 )
		plabel.grid(row=8,column=1)
		
		
		
		button = tk.Button( rightcntlframe, text="Get Previous", 
							   command=self.handleGetPrevious)
		button.grid(row=9,column=1,pady=5)   # default side is top
	
################################################################# left frame ################################################################
		
		# make a control frame on the left
		leftframe = tk.Frame(self.root)
		leftframe.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.BOTH)
		# make a separator frame
		sepl = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sepl.pack( side=tk.LEFT, padx = 2, pady = 2, fill=tk.X)
		
		
		pcalabel=tk.Label( leftframe, text="PCA Analysis", width=20 )
		pcalabel.grid(row=1,column=2)
		self.pcalistbox = tk.Listbox(leftframe)
		self.pcalistbox.grid(row=2,column=2)
			
		button = tk.Button( leftframe, text="Plot PCA", 
							   command=self.handlePlotPCA)
		button.grid(row=3,column=2,pady=5)   # default side is top
		
		button = tk.Button( leftframe, text="Write PCA", 
							   command=self.handleWritePCA)
		button.grid(row=4,column=2,pady=5)   # default side is top
		
		button = tk.Button( leftframe, text="See Analysis", 
							   command=self.handleSeeAnalysis)
		button.grid(row=5,column=2,pady=5)   # default side is top
		
		button = tk.Button( leftframe, text="Plot Mixed", 
							   command=self.handlePlotMixed)
		button.grid(row=6,column=2,pady=5)   # default side is top
		
		button = tk.Button( leftframe, text="Input Cluster", 
							   command=self.handleCluster)
		button.grid(row=7,column=2,pady=5)   # default side is top
		
		clusterlabel=tk.Label( leftframe, text="Cluster Box", width=20 )
		clusterlabel.grid(row=8,column=2)
		self.clusterbox = tk.Listbox(leftframe)
		self.clusterbox.grid(row=9,column=2)
		
		button = tk.Button( leftframe, text="Plot Cluster", 
							   command=self.handlePlotCluster)
		button.grid(row=10,column=2,pady=5)   # default side is top
		
		button = tk.Button( leftframe, text="Build Classifier", 
							   command=self.buildClassifier)
		button.grid(row=11,column=2,pady=5)   # default side is top
		
		button = tk.Button( leftframe, text="Classify", 
							   command=self.classify)
		button.grid(row=12,column=2,pady=5)   # default side is top

################################################################# down frame ################################################################	
		
		# make a control frame on the bottom
		downframe = tk.Frame(self.root)
		downframe.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.BOTH)
		# make a separator frame
		sep = tk.Frame( self.root, height=2, width=self.initDx, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.BOTTOM, padx = 2, pady = 2, fill=tk.X)
		
		self.labell = tk.Label( downframe, text="", width=40 )
		self.labell.pack( side=tk.TOP, pady=5 )
		self.labell.config(text="Scale:" + str(round(1.0/self.view.extent[0],2))+"	Orientation: "+str(round(self.degree[0],2))+", "+str(round(self.degree[1],2)))
		return

	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Button-2>', self.handleMouseButton2 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<B3-Motion>', self.handleMouseButton3Motion )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Button-3>', self.handleMouseButton3 )
		self.canvas.bind( '<Configure>',self.resize)
		
		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-n>', self.clearData )
		self.root.bind( '<Command-z>', self.reset)
		self.root.bind( '<Command-x>', self.resetYZ)
		self.root.bind( '<Command-y>', self.resetZX)
		self.root.bind( '<Command-o>', self.handleOpen)

	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()
	
	def resize(self,event):
		w = self.canvas.winfo_width()
		h = self.canvas.winfo_height()
		shorter = min(w,h)
		if hasattr(self,'view'):
			self.view.update_screen([shorter-250,shorter-250])
			self.updatePoints()
			self.updateAxes()
			self.updateFits()
			self.updateMultiFits()
		

	def handleMouseButton1(self, event):		
		self.baseClick = (event.x, event.y)

	def handleMouseButton2(self, event):
		self.baseClick = (event.x, event.y)
		
		self.oriView=self.view.clone()
	
	#This will give user the previous analysis informations
	def handleGetPrevious(self):
		
		if(self.count<self.PreAnal.get()):
			return
			
		info=self.previousAnalysis[self.count-self.PreAnal.get()]


		if info[0]=="Linear":
			slabel=tk.Label( self.right, text="Linear regression of ", width=20 )
			slabel.grid(row=17,column=1)
			slabel=tk.Label( self.right, text=str(info[1])+" and " + info[2], width=20 )
			slabel.grid(row=18,column=1)
			slabel=tk.Label( self.right, text="slope = " + str(round(info[3],2)), width=20 )
			slabel.grid(row=19,column=1)
			slabel=tk.Label( self.right, text="intercept = " + str(round(info[4],2)), width=20 )
			slabel.grid(row=20,column=1)
			slabel=tk.Label( self.right, text="r_value = " + str(round(info[5],2)), width=20 )
			slabel.grid(row=21,column=1)
			slabel=tk.Label( self.right, text="p_value = " + str(round(info[6],2)), width=20 )
			slabel.grid(row=22,column=1)
			slabel=tk.Label( self.right, text="std_err = " + str(round(info[7],2)), width=20 )
			slabel.grid(row=23,column=1)
			slabel=tk.Label( self.right, text="", width=20 )
			slabel.grid(row=24,column=1)
			
		else:
			slabel=tk.Label( self.right, text="Multi-LR of "+info[0]+",", width=20 )
			slabel.grid(row=17,column=1)
			slabel=tk.Label( self.right, text=str(info[1])+" and " + info[2], width=20 )
			slabel.grid(row=18,column=1)
			slabel=tk.Label( self.right, text="m0 = " + str(round(info[3][0][0],2))+", m1 = "+str(round(info[3][1][0],2)), width=20 )
			slabel.grid(row=19,column=1)
			slabel=tk.Label( self.right, text="intercept = " + str(round(info[3][2][0],2)), width=20 )
			slabel.grid(row=20,column=1)
			slabel=tk.Label( self.right, text="sse = " + str(round(info[4],2)), width=20 )
			slabel.grid(row=21,column=1)
			slabel=tk.Label( self.right, text="r2 = " + str(round(info[5],2)), width=20 )
			slabel.grid(row=22,column=1)
			slabel=tk.Label( self.right, text="t = " + str(round(info[6][0],1))+" "+str(round(info[6][1],1))+" "+str(round(info[6][2],1)), width=20 )
			slabel.grid(row=23,column=1)
			slabel=tk.Label( self.right, text="p_value = " + str(round(info[7][0],1))+" "+str(round(info[7][1],1))+" "+str(round(info[7][2],1)), width=20 )
			slabel.grid(row=24,column=1)
	
	# This is called if the first mouse button is being moved
	def handleMouseButton1Motion(self, event):
		# calculate the difference
		diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
		
		# Divide the differential motion (dx, dy) by the screen size (view X, view Y)
		dx=float(diff[0])/self.view.screen[0]*self.num.get()
		dy=float(diff[1])/self.view.screen[1]*self.num.get()
		
		# Multiply the horizontal and vertical motion by the horizontal and vertical extents.
		dx*=self.view.extent[0]
		dy*=self.view.extent[1]

		# The VRP should be updated by delta0 * U + delta1 * VUP (this is a vector equation)
		self.view.vrp+=dx*self.view.u+dy*self.view.vup
		# call updateAxes()
		self.updateAxes()
		self.updateFits()
		self.updateMultiFits()
		
		# call updatePoints()
		self.updatePoints()
						
		# update base click
		self.baseClick = ( event.x, event.y )
	
	# This is called if the third mouse button is being clicked
	def handleMouseButton3(self, event):	
		self.baseClick = (event.x, event.y)
		self.extent=[]
		self.extent.append(self.view.extent[0])
		self.extent.append(self.view.extent[1])
		self.extent.append(self.view.extent[2])
		
	# This is called if the third mouse button is being moved
	def handleMouseButton3Motion(self, event):
		# calculate the difference in y axis
		dy=float(event.y - self.baseClick[1])/self.initDy
		
		scaler=(1+dy*self.num.get())
		scaler=max(0.1,scaler)
		scaler=min(3.0,scaler)
		#multiply the original extent by the factor and put it into the View object 
		self.view.extent[0]=scaler*self.extent[0]
		self.view.extent[1]=scaler*self.extent[1]
		# call updatePoints()
		self.updatePoints()
		self.updateAxes()
		self.updateFits()
		self.updateMultiFits()
		self.labell.config(text="Scale:" + str(round(1.0/self.view.extent[0],2))+"	Orientation: "+str(round(self.degree[0],2))+", "+str(round(self.degree[1],2)))
			
	# This is called if the second button of a real mouse has been pressed
	# and the mouse is moving. Or if the control key is held down while
	# a person moves their finger on the track pad.
	def handleMouseButton2Motion(self, event):
		dy = self.baseClick[1] - event.y 
		dx = self.baseClick[0] - event.x 
		delta0=float(dx) / 200 * math.pi*self.num.get()
		delta1=float(dy) / 200 * math.pi*self.num.get()
		self.degree=(delta0,delta1)
		
		self.view=self.oriView.clone()
		self.view.rotateVRC(-delta1, delta0)
		self.updateAxes()
		self.labell.config(text="Scale:" + str(round(1.0/self.view.extent[0],2))+"	Orientation: "+str(round(self.degree[0],2))+", "+str(round(self.degree[1],2)))
		self.updateFits()
		self.updateMultiFits()
		# call updatePoints()
		self.updatePoints()
	
	'''extension'''
	#write the statistical result to a file
	def writeToFile(self):
		if not self.previousAnalysis:
			return 
		info = self.previousAnalysis[self.count]
		fp=file(self.filename,'rU+')
		if info[0]=="Linear":
			fp.write("Linear regression of "+info[1]+" and " + info[2]+"\n")
			fp.write("slope = " + str(info[3])+"\n")
			fp.write("intercept = " + str(info[4])+"\n")
			fp.write("r_value = " + str(info[5])+"\n")
			fp.write("p_value = " + str(info[6])+"\n")
			fp.write("std_err = " + str(info[7])+"\n")
		else:
			fp.write("Linear regression of "+info[0]+", "+info[1]+" and " + info[2]+"\n")
			fp.write("m0 = " + str(info[3][0][0])+"\n")
			fp.write("m1 = " + str(info[3][1][0])+"\n")
			fp.write("intercept = " + str(info[3][2][0])+"\n")
			fp.write("sse = " + str(info[4])+"\n")
			fp.write("r2 = " + str(info[5])+"\n")
			fp.write("t = " + str(info[6])+"\n")
			fp.write("p = " + str(info[7])+"\n")	
		fp.close
		
	
	#Let user choose the axis they want to represent	
	def handleChooseAxes(self):
		DDialog=AxisDialog(self.canvas,self.data.get_headers(),"Choose Axis")
		return DDialog.result
	
	#Let user choose the axis they want to represent	
	def handleLinear(self):
		DDialog=LinearDialog(self.canvas,self.data.get_headers(),"Choose Axis")
		return DDialog.result
	
	#Let user choose the axis they want to represent	
	def handleMultiLinear(self):
		DDialog=MultiLinearDialog(self.canvas,self.data.get_headers(),"Choose Axis")
		return DDialog.result	

	
	def handleMenuCmd1(self):
		d=ShapeDialog(self.canvas,"Choose Shape")
		if(d.result !="cancel"):
			self.shape=d.result 
	
	
		
	def main(self):
		print 'Entering main loop'
		self.root.mainloop()


if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()


