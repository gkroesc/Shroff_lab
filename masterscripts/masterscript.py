'''
masterscript
'''
#_#_#_#_#_#_#_#__CLASSES__#_#_#_#_#_#_#_#

#_#_#_#_#_#_#_#__MISC__#_#_#_#_#_#_#_#


class Point(object):
	def __init__(self, x, y):
		self.x, self.y = x, y

class Rect(object):
	def __init__(self, x1, y1, x2, y2):
		minx, maxx = (x1,x2) if x1 < x2 else (x2,x1)
		miny, maxy = (y1,y2) if y1 < y2 else (y2,y1)
		self.min = Point(minx, miny)
		self.max = Point(maxx, maxy)

	width  = property(lambda self: self.max.x - self.min.x)
	height = property(lambda self: self.max.y - self.min.y)

#_#_#_#_#_#_#_#__PYTORCH__#_#_#_#_#_#_#_#

class CNNMain:


	def __init__(self,data,labels):
		self.data = data
		self.labels = labels

	'''

		Inside this CNet class, we can define what we want our convolutional neural network to look like!
		We will define the convolutional layers AND the linear layers here

		Inputs:


	'''

	class CNet(nn.Module):

		def __init__(self,n_channels,hidden_dimension,kernel_size,n_classes,pool):

			super(BIOF050_CNN_Final.CNet, self).__init__()

			### first convolution layer - You need to know # of channels/inputs and number of kernels (outputs)
			self.convolution1 = nn.Conv2d(n_channels,28,kernel_size=kernel_size)

			###2-D max pooling
			self.pool = nn.MaxPool2d(pool, pool)

			### second convolution layer - first term is number of kernels from last conv layer,
			### second is number of outputs

			self.convolution2 = nn.Conv2d(28,56,kernel_size=kernel_size)

			### 2-D maxpooling
			self.pool2 = nn.MaxPool2d(pool, pool)


			'''
			MLP layer - the 3584 represents the output of the final maxpooling (MaxPool2d)
			after being flattened - you will need to get this value for each dataset you use
			1400 = number of perspectives (features) that we start with when running find_MLP
			'''

			self.layer1 = nn.Linear(find_MLP_dim(28,kernel_size,56),1400)
			self.layer2 = nn.Linear(1400, 10)
			self.relu = nn.ReLU()
			#self.relu= nn.LeakyReLU()




		'''
		Now, we have to define the forward method, which takes a data point, or, in most cases, a batch, and
		feeds it through all the layers of our neural network until assigning it a layer

		nn.Convolution and nn.Linear take one array/tensor as an input, so we will input our data right into each layer, and then input the
		outputs of each layer into the next layer

		After each layer, we will apply nn.ReLU to transform our data into a nonlinear space

		Finally, after the data has been passed through the output layer, we will convert it into a probaboility
		distribution using the softmax function.

		This probabilty dsistribution will be used to assign a label to our
		data points and to figure out just how well our neural network did, as we learned earlier today

		'''

		def forward(self, batch):

			### first convolution
			batch = self.convolution1(batch)

			## activation
			batch = self.relu(batch)

			## we could have batch norm if we wanted to
			## we could add in dropouts

			### pooling
			batch = self.pool(batch)

			### second convolution
			batch = self.convolution2(batch)

			## activation
			batch = self.relu(batch)

			batch = self.pool2(batch)

			## flatten out each image to be in 1D using this view function
			batch = batch.view(batch.size(0), -1)

			### MLP layer
			batch = self.layer1(batch)
			batch = self.layer2(batch)

			### probability dist.
			return nn.functional.softmax(batch, dim=-1)






	def train_test(self,test_size,n_epochs,n_channels,hidden_dimensions,batch_size,kernel_size,pool,lr):

		### splitting the data into a training/testing set
		train_data,test_data,train_labels,test_labels = train_test_split(self.data,self.labels, test_size=test_size)

		## creating the batches using the batchify function
		train_batches,train_label_batches = batchify(train_data,train_labels,batch_size=batch_size)

		'''
		Here is where we define our neural network model - the Net class is inside BIOF050, so we have to call
		it accordingly
		We use the length of our first data point to set the length of our input data (they are all the same)
		The number of class is equal to the number of unique values (the set) of our training labels
		'''
		neural_network = BIOF050_CNN_Final.CNet(n_channels,hidden_dimensions,kernel_size,len(set(train_labels)),pool)

		'''
		Here, we use the torch.optim package to create our stochastic gradient descent function
		neural_network.parameters() reads internal information from our NN
		(don't worry about that - SGD just requires it)
		lr is the learning rate
		'''
		optimizer = optim.SGD(neural_network.parameters(), lr=lr)
		'''
		Here, we use the nn package to create our cross entropy loss function
		'''
		loss_function = nn.CrossEntropyLoss()
		'''
		The train function tells the neural network that it is about to be trained and that it
		will have to calculate the needed information for optimization
		This function should always be called before training
		'''
		neural_network.train()


		''' This loop moves through the data once for each epoch'''
		for i in range(n_epochs):

			### track the number we get correct
			correct = 0

			''' This loop moves through each batch and feeds into the neural network'''
			for ii in range(len(train_batches)):

				'''
				Clears previous gradients from the optimizer - the optimizer,
				in this case, does not need to know what happened last time
				'''
				optimizer.zero_grad()


				batch = train_batches[ii]
				labels = train_label_batches[ii]


				'''
				Puts our batch into the neural network after converting it to a tensor

				Pytorch wants numeric data to be floats, so we will convert to a float as well
				using np.float32

				Predictions: For each data point in our batch, we would get something that looks like:
				tensor([0.3,0.7]) where each number corresponds to the probability of a class
				'''
				predictions = neural_network(torch.tensor(np.asarray(batch).astype(np.float32)))


				'''
				We put our probabilities into the loss function to calculate the error for this batch

				'''
				loss = loss_function(predictions,torch.LongTensor(labels))

				'''
				loss.backward calculates the partial derivatives that we need to optimize
				'''
				loss.backward()


				'''
				optimizer step calculates the weight updates so the neural network can update the weights
				'''
				optimizer.step()


				'''
				We extract just the data from our predictions, not other stuff Pytorch includes in that object
				We can then use the argmax function to figure out which index corresponds to the highest probability.
				If it is the 0th index, and the label is zero, we add one to correct.
				If it is the 1st index, and the label is one, we add one to correct.
				'''
				for n,pred in enumerate(predictions.data):
					if labels[n] == torch.argmax(pred):
						correct += 1


			print("Accuracy for Epoch # " + str(i) + ": " + str(correct/len(train_data)))

		print()



		'''
		The eval function tells the neural network that it is about to be tested on blind test data
		and shouldn't change any of its internal parameters

		This function should always be called before eval
		'''
		neural_network.eval()

		test_correct = 0

		''' input our test data into the neural network'''
		predictions = neural_network(torch.tensor(np.asarray(test_data).astype(np.float32)))

		''' checks how many we got right - very simple!'''
		for n,pred in enumerate(predictions.data):
			if test_labels[n] == torch.argmax(pred):
					test_correct += 1

		print("Accuracy on test set: " + str(test_correct/len(test_data)))

		return neural_network

#_#_#_#_#_#_#_#__TKINTER__#_#_#_#_#_#_#_#
class ControllerWin(ttk.Frame): 


	import timeit
	import tkinter as tk
	from tkinter import ttk
	from tkcalendar import DateEntry
	from ttkthemes import ThemedStyle

	'''
	Main controller window called by main(). 
	Also contains multiple functions that affect other classes.
	Creates the notebook frame which the app is anchored in,
	grids three subclasses (arbitrarily named page 1-3).
	Pages are referenced in order of appearance. 
	Menubar created last, which gives options to save, refresh, or exit
	'''
	def __init__(self, parent):

		ttk.Frame.__init__(self, parent)
		self.parent = parent #parent is the root)
		self.rootWidth = int(self.parent.winfo_screenwidth()*0.85)
		self.rootHeight = int(self.parent.winfo_screenheight()*0.85)
		self.rootFontSize = 11
		self.rootFont = 'Roboto'
		self.bgColor = 'white'
		self.fgColor = 'black'
		self.themeColor = 'white'##FCDFFC'
		self.parent.geometry('{}x{}'.format(self.rootWidth, self.rootHeight))
		self.parent.resizable(0,0)
		self.style = ThemedStyle(self.parent)
		#self.style.set_theme('breeze')
		#self.style = ttk.Style(parent)
		self.style.theme_use('vista') # *xpnative, winnative, *vista, classic, clam, alt
		self.style.configure('TFrame')
		self.style.configure('TLabelFrame')
		self.style.configure('TButton', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TCheckbutton', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TCombobox', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TEntry', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TLabel', font = (self.rootFont, self.rootFontSize))
		self.style.configure('Header.TLabelframe.Label', font = (self.rootFont, self.rootFontSize+1, 'bold'))
		self.style.configure('Bold.TLabel', font = (self.rootFont, self.rootFontSize+1, 'bold'))
		self.style.configure('TMenuButton', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TNotebook', font = (self.rootFont, self.rootFontSize))
		self.style.configure('Horizontal.TScrollbar', font = (self.rootFont, self.rootFontSize))#, font=('Helvetica', 12))
		self.style.configure('Vertical.TScrollbar')#, font=('Helvetica', 12))#

		self.parent.grid_columnconfigure(0, weight=5)
		self.parent.grid_rowconfigure(0, weight=10)
		self.parent.grid_rowconfigure(1, weight = 1)




		self.notebook = ttk.Notebook(self.parent, height = int(self.rootHeight*0.7)) 
		self.notebook.grid(row = 0, column = 0, sticky='nesw', padx = 10, pady = 10)
		
		self.eventLogFrame = ttk.LabelFrame(self.parent, text = 'Event Log', style = 'Header.TLabelframe')
		self.eventLogFrame.grid(row = 1, column = 0, sticky='nesw', padx = 10, pady = 10)

		self.eventLog = tk.Text(self.eventLogFrame, height = 20) #Num lines
		self.eventLog.pack(expand = False, fill = 'x')



		self.viewPage = viewpage.Create(self.notebook, self)

class Create(ttk.Frame):
	'''
	Window created by controller window and anchored in notebook frame
	Purpose: Give user an interface to view and edit preveiously 
	added strains in the database. 
	Uses Pandas Table module, allowing for intuitive interaction with dataframe objects
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)

		self.parent = parent 
		self.controller = controller
		self.Page2Frame = ttk.Frame(self.parent)
		self.Page2Frame.grid()
		self.Page2Frame.grid_columnconfigure(0, weight=1)
		self.parent.add(self.Page2Frame, text = 'View database strains') #Add tab to NB

		self.dataWin = DataView(self.Page2Frame, self.controller)
#_#_#_#_#_#_#_#__FUNCTIONS__#_#_#_#_#_#_#_#

def distance3D(coord1, coord2):
	#AB = sqrt((x2-x1)^2+(y2-y1)^2+(z2-z1)^2)
	formx = (float(coord2[0]) - float(coord1[0]))**2
	formy = (float(coord2[1]) - float(coord1[1]))**2
	formz = (float(coord2[2]) - float(coord1[2]))**2
	dist = sqrt(formx+formy+formz)
	return dist

def drawCircle(draw, coord1, coord2, radius, color, outercolor): 
	from PIL import Image, ImageDraw, ImageFont

	x1 = coord1[0] -radius
	x2 = coord2[0] +radius
	y1 = coord1[1] -radius
	y2 = coord2[1] +radius

	draw.ellipse((y1, x1, y2, x2), fill = color, outline = outercolor)

def drawPhrase(draw, phrase, coord1):
	#check 6/14/22
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype('arial.ttf',18)
	# draw.text((x, y),"Sample Text",(r,g,b))
	draw.text((coord1[0], coord1[1]),"{}".format(phrase),(256,256,256), font=font)

def drawScaleBar(draw, topleft, bottomright, maxString, minString):
	from PIL import Image, ImageDraw, ImageFont
	
	x1 = topleft[0]
	x2 = bottomright[0]
	y1 = topleft[1]
	y2 = bottomright[1]
	draw.text((x1, y1-15), maxString)
	draw.text((x1, y2+5), minString)
	# Draw a three color vertical gradient.
	darkRED, RED, YELLOW, WHITE = ((0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255))
	color_palette = [darkRED, RED, YELLOW, WHITE]
	region = Rect(x1, y1, x2, y2)
	width, height = region.max.x+1, region.max.y+1

	vert_gradient(draw, region, gradient_color, color_palette)

def vert_gradient(draw, rect, color_func, color_palette):

	minval, maxval = 1, len(color_palette)
	delta = maxval - minval
	height = float(rect.height)  # Cache.
	for y in range(rect.min.y, rect.max.y+1):
		f = (y - rect.min.y) / height
		val = minval + f * delta
		color = color_func(minval, maxval, val, color_palette)
		draw.line([(rect.min.x, y), (rect.max.x, y)], fill=color)

def gradient_color(minval, maxval, val, color_palette):
	""" Computes intermediate RGB color of a value in the range of minval
		to maxval (inclusive) based on a color_palette representing the range.
	"""
	max_index = len(color_palette)-1
	delta = maxval - minval
	if delta == 0:
		delta = 1
	v = float(val-minval) / delta * max_index
	i1, i2 = int(v), min(int(v)+1, max_index)
	(r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
	f = v - i1
	return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

def getDatetime(datestring):
		date = str(

			datestring)

		if date == 'None':
			dtobject = 'None'

		try:
			dtobject = datetime.datetime.strptime(date, '%Y-%m-%d')

		except ValueError:
			try:
				dtobject = datetime.datetime.strptime(date, '%Y/%m/%d')
			except ValueError:
				try:
					dtobject = datetime.datetime.strptime(date, '%m-%d-%Y')
				except ValueError:
					try:
						dtobject = datetime.datetime.strptime(date, '%m/%d/%Y')
					except ValueError:
						try:
							dtobject = datetime.datetime.strptime(date, '%d-%m-%Y')
						except ValueError:
							try:
								dtobject = datetime.datetime.strptime(date, '%d/%m/%Y')
							except ValueError:
								return None
		return dtobject