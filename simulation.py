
import matplotlib.pyplot as plt
import random as rd
from Tkinter import *
import math
import copy
import time
import glob, os


#======================Global constants and initilisation of variables==============

#The number of cell an axis can display
XCELLAXIS = 50
YCELLAXIS = 50

#The initiale variable N and the size and step of its scale
N = 500
Nmax = 1000
Nmin = 0
Nstep = 1
Ntype = int

#The initiale Kapp period and the size and step of its scale
KappT = 30
KappTmax = 50
KappTmin = 0
KappTstep = 0.5
KappTtype = float

#The initiale Kapp amplitude and the size and step of its scale
KappA = 5
KappAmax = 15
KappAmin = 0
KappAstep = 0.1
KappAtype = float

#The initiale Koff period and the size and step of its scale
KoffT = 30
KoffTmax = 50
KoffTmin = 0
KoffTstep = 0.1
KoffTtype = float

#The initiale Koff amplitude and the size and step of its scale
KoffA = 0.1
KoffAmax = 1
KoffAmin = 0
KoffAstep = 0.01
KoffAtype = float

#The initiale variable NbIter (number of iterations) and the size and step of its scale
NbIter = 20
NbItermax = 0 
NbItermin = 100
NbIterstep = 1
NbItertype = int

def Koff(x, amplitude = KoffA, period = KoffT):
	return 0.15 + 0.5 * amplitude * math.sin(2*math.pi/(float(period)) * x)

def Kapp(x, amplitude = KappA, period = KappT):
	return 7.5 - 0.5 * amplitude * math.sin(2*math.pi/(float(period)) * x)





def sign(x):
	if x>0:
		return 1
	elif x==0:
		return 0
	else:
		return -1

#==============================================================
class Molecule:
	"""
	A Molecule object contains :
	- An x position (on the XCELLAXIS)
	- An y position (on the YCELLAXIS)
	- A color c (here red, blue or green)
	"""

	def __init__(self, color='g'):
		#The position of a molecule is randomly generated
		self.x = rd.randint(1, XCELLAXIS-1)
		self.y = rd.randint(1, YCELLAXIS-1)
		self.c = color

	def colourise(self, color='g'):
		#Change the color of a molecule
		self.c = color

	def __repr__(self):
		return "({}, {}, {})".format(self.x, self.y, self.c)

	def copy_mol(self):
		#A copy function to avoid Python copy issues for class and arrays
		M = Molecule()
		M.x = self.x
		M.y = self.y
		M.c = self.c
		return M


class MoleculeCollection:
	"""
	A MoleculeCollection object contains :
	- An array of Molecule objects

	It will represent the situation of the system at a moment of the evolution
	"""

	def __init__(self, len, color='g'):
		#The array is initialized with random molecules
		self.a = [Molecule(color=color) for i in range(len)]

	def __getitem__(self, index):
		return self.a[index]

	def __setitem__(self, index, element):
		self.a[index] = element

	def __repr__(self):
		res = "["
		b = True
		for elm in self:
			if b:
				b = False
			else:
				res += ', '
			res += elm.__repr__()
		return res+"]"

	def __len__(self):
		return len(self.a)

	def isEmpty(self):
		return len(self) == 0

	def __add__(self, mol):
		self.a.append(mol)

	def add_rd(self, color = 'g'):
		#Add a random molecule in the array
		self + (Molecule(color=color))

	def add_n(self, n, color = 'g'):
		#Add n random molecules in the array
		for i in range(n):
			self.add_rd(color=color)

	def colourise(self, color = 'g'):
		#Colourise all the molecules in the array
		for mol in self:
			mol.colourise(color)

	def colourise_part(self, count, color = 'g'):
		#Colourise a random count of molecules in the array
		indexes = [i for i in range(len(self))]
		indexes_to_colourise = rd.sample(indexes, min(count, len(self)))
		for i in range(len(self)):
			if i in indexes_to_colourise :
				self[i].colourise(color)

	def __delitem__(self, i):
		del self.a[i]


	def pop(self):
		try:
			self.isEmpty()
		except: 
			print "You try to remove molecule from an empty colection"
		self.a.pop()

	def remove_n(self, n):
		for i in range(n):
			self.remove()

	def remove(self, element):
		self.a.remove(element)


	def remove_color(self, color='g'):
		#Remove all the molecule of a given color in the array
		for mol in self:
			if mol.c == color:
				self.remove(mol)

	def count_present(self, absent_color='r'):
		#Count the number of molecules in the array of a different color than absent_color
		res = 0
		for elm in self:
			if elm.c != absent_color:
				res += 1
		return res

	def plot_collection(self):
		#Create a plot of a collection with dot for melcules
		for c in ['r', 'g', 'b']:
			
			x = []
			y = []

			for mol in self:
				if c == mol.c :
					x.append(mol.x)
					y.append(mol.y)

			plt.plot(x, y, c+'o')
		plt.show()

	def copy(self):
		#A copy function to avoid Python copy issues for class and arrays
		collection = MoleculeCollection(len(self))
		for i in range(len(self)):
			collection[i] = self[i].copy_mol()
		return collection

	def export(self, name="collection"):
		#Create an image file of the collection and put it in the folder evolution
		plt.clf()
		for c in ['r', 'g', 'b']:
		
			x = []
			y = []

			for mol in self:
				if c == mol.c :
					x.append(mol.x)
					y.append(mol.y)

			if c == 'r':
				label = 'Leave'
			elif c == 'g':
				label = 'Stay'
			else :
				label = 'Come'
			plt.plot(x, y, c+'o', label=label)

		plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
		plt.savefig("output/evolution/"+name+".png", format='png')
		plt.clf()





class EvolutionFilm:
	"""
	An EvolutionFilm object contains :
	- A sequence of MoleculeCollections
	"""
	
	def __init__(self):
		self.s = []

	def __getitem__(self, index):
		return self.s[index]

	def __len__(self):
		return len(self.s)

	def __repr__(self):
		res = ""
		for i in range(len(self)):
			res += "\nCollection {}".format(i)+" :\n"+self[i].__repr__()
		return res

	def __add__(self, collection):
		self.s.append(collection.copy())

	def export(self):
		#Export a whole image film
		i = 0
		for collection in self:
			i += 1
			collection.export(name="collection{}".format(i))
			



def generate(N0, KappT, KappA, KoffT, KoffA, NbIter):
	#Generate an evolution film of the system for the given parameters and the associate plot

	N = N0
	film = EvolutionFilm()
	evolution = [N]
	rapport = []



	current_collection = MoleculeCollection(N)

	for i in range(NbIter):

		valKapp = Kapp(i, KappA, KappT)
		valKoff = Koff(i, KoffA, KoffT)

		current_collection.remove_color(color = 'r')
		current_collection.colourise('g')
		current_collection.colourise_part(int(N*valKoff), 'r')
		current_collection.add_n(int(valKapp), 'b')
		
		film + copy.deepcopy(current_collection)

		
		N = N - int(N*valKoff) + int(valKapp)
		evolution.append(N)
		rapport.append(valKapp/valKoff)

	evolution.pop()

	return film, evolution, rapport

def generate_plot_output(evolution, rapport, NbIter):
	#Generate images files of the curve with a vertical bar to show where the system is
	PlotArrayX = [i for i in range(NbIter)]
	PlotArrayY = evolution

	for i in range(NbIter):
		plt.clf()
		plt.axvline(x=i, ymin=0, ymax = 20, linewidth=1, color='k')
		plt.plot(PlotArrayX, PlotArrayY, label='N')
		plt.plot(PlotArrayX, rapport, label='Kapp/Koff')
		plt.legend()
		plt.savefig("output/plots/graph{}.png".format(i+1), format='png')
		plt.clf()
	



#=============================================================
class ScaleValue:
	def __init__(self, value, mini, maxi, step, window, name, typ):
		self.value = value
		self.min = mini
		self.max = maxi
		self.step = step
		self.name = name
		self.scale = Scale(window, from_=mini, to=maxi, resolution=step, tickinterval=(maxi-mini)/float(5), length=100,label=name)
		self.type = typ 

	def show(self):
		self.scale.pack(side=LEFT)
		self.scale.set(self.value)

class ScaleArray:
	def __init__(self):
		self.a = []

	def show(self):
		for scale in self:
			scale.show()

	def __add__(self, element):
		self.a.append(element)

	def __getitem__(self, index):
		return self.a[index]

	def get_scales(self):
		return [scale.scale for scale in self]

	def get_values(self):
		return [scale.value for scale in self]

	def update_scales(self):
		for scale in self:
			scale.value = max(scale.type(scale.scale.get()), 0.05)

#==============================================================

class Interface(Frame):
	def __init__(self, window, **kwargs):
		#The graphical interface, here is the first one with the scales

		Frame.__init__(self, window, width=0, height=0, **kwargs)
		self.pack(fill=BOTH)
		self.isclosed = False

		#Initialization of the Global Scales Array
		GSA = ScaleArray()
		GSA + ScaleValue(N, Nmin, Nmax, Nstep, window, "N", Ntype)
		GSA + ScaleValue(KoffT, KoffTmin, KoffTmax, KoffTstep, window, "Koff period", KoffTtype)
		GSA + ScaleValue(KoffA, KoffAmin, KoffAmax, KoffAstep, window, "Koff amplitude", KoffAtype)
		GSA + ScaleValue(KappT, KappTmin, KappTmax, KappTstep, window, "Kapp period", KappTtype)
		GSA + ScaleValue(KappA, KappAmin, KappAmax, KappAstep, window, "Kapp amplitude", KappAtype)
		GSA + ScaleValue(NbIter, NbItermin, NbItermax, NbIterstep, window, "Number of iterations", NbItertype)


		for scale in GSA:
			scale.show()
		
		simul_button = Button(window, text="Simulate", command=lambda: self.send_scales(window))
		simul_button.pack(side=RIGHT)

		close_button = Button(window, text="Close", command=lambda: self.close(window))
		close_button.pack(side=RIGHT)


		self.buttons = simul_button, close_button
		self.scales = GSA

	def close(self, window):
		self.isclosed = True
		window.quit()

 
	def send_scales(self, window):
		#Get the values of the scales and save them in variables for future utilisations
		self.scales.update_scales()
		window.quit()

	def __getattr__(self, scales):
		return self.scales

	def __getattr__(self, buttons):
		return self.buttons

	
		


class Gif(Interface):
	def __init__(self, interface):
		#The interface of the gifs
		for scale in interface.scales:
			scale.scale.destroy()
		for button in interface.buttons:
			button.destroy()

		

		self.time = time.time()
		self.mFrame = Frame()
		self.mFrame.pack(side=TOP,expand=YES,fill=X)
		self.index = 0

		text = "N0 = {}, Kapp period = {}, Kapp amplitude = {}, Koff period = {}, Koff amplitude = {}, Phase shift = {}".format(N, KappT, KappA, KoffT, KoffA, PS)
		textlabel = Label(self.mFrame, text=text)
		textlabel.pack(side=TOP)

		Button(window, text="Close", command=window.quit).pack(side=LEFT)

		self.graph = Label(self.mFrame, image=plot_result[self.index])
		self.graph.pack(side=LEFT)
		
		self.watch = Label(self.mFrame, image=Sq[self.index])
		self.watch.pack(side=RIGHT)

		self.n = NbIter

		self.changeLabel()

	def changeLabel(self):
		#A function to make the gif works (always call itself)
		if time.time() >= self.time+5/float(self.n) :
			self.time = time.time()
			self.index += 1
			if self.index >= self.n:
				self.index = 0
			self.watch.configure(image=Sq[self.index])
			self.graph.configure(image=plot_result[self.index])
		self.mFrame.after(200, self.changeLabel)

def phase_shift(evolution, rapport):

	ev_max_indexes = []
	dev = evolution[0] - evolution[1]
	for i in range(1, len(evolution)-1):
		dev = evolution[i-1] - evolution[i]
		if (sign(dev) > sign(evolution[i] - evolution[i+1])):
			ev_max_indexes.append(i)


	ra_max_indexes = []
	dra = rapport[0] - rapport[1]
	for j in range(1,len(rapport)-1):
		dra = rapport[j-1] - rapport[j]
		if (sign(dra) > sign(rapport[j] - rapport[j+1])):
			ra_max_indexes.append(j)

	if len(ev_max_indexes)<2:
		return 0

	if ev_max_indexes[-1]-ra_max_indexes[-1] > 0:
		return ev_max_indexes[-1]-ra_max_indexes[-1]


	return ev_max_indexes[-1]-ra_max_indexes[-2]




def load_image_sequence(path, name, n):
	#The function to load all the image of a directory for future use
	t = []
	for i in range(n):
		img = PhotoImage(file=path+name+"{}.png".format(i+1))
		t.append(img)
	return t

def create_directories():
	#Create the directories for ploting if the don't already exists
	if not os.path.exists("output"):
	    os.makedirs("output")

	if not os.path.exists("output/evolution"):
	    os.makedirs("output/evolution")

	if not os.path.exists("output/plots"):
	    os.makedirs("output/plots")


def clean_previous_results():
	#Remove all the previous images from the directories
	filelist = glob.glob("output/evolution/*.png")
	for f in filelist:
	    os.remove(f)

	filelist = glob.glob("output/plot/*.png")
	for f in filelist:
	    os.remove(f)



create_directories()

#Comment the folowing line if you want too keep some results. 
#The programm will replace them by news if you don't change the names.
clean_previous_results()

window = Tk()


interface = Interface(window)
interface.mainloop()

values = interface.scales.get_values()

N = values[0]
KoffT = values[1]
KoffA = values[2]
KappT = values[3]
KappA = values[4]
NbIter = values[5]

if not (interface.isclosed):
	S, evolution, rapport = generate(N, KappT, KappA, KoffT, KoffA, NbIter)


	generate_plot_output(evolution, rapport, NbIter)
	S.export()

	Sq = load_image_sequence("output/evolution/", "collection", NbIter)
	plot_result = load_image_sequence("output/plots/", "graph", NbIter)

	PS = phase_shift(evolution, rapport)

	gif = Gif(interface)
	window.mainloop()