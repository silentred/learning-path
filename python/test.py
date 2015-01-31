#!/usr/bin/python

def factorial(n):
	if n==1:
		return 1
	else:
		return n*factorial(n-1)

#print factorial(5)

def power(x, n):
	if n==0:
		return 1
	else:
		return x * power(x,n-1)

#print power(2,10)

def search(sequence, number, lower=0, upper=None):
	if upper is None:
		upper = len(sequence)-1

	if lower==upper:
		assert number == sequence[upper]
		return upper
	else:
		middle = (lower + upper)//2
		if number>sequence[middle]:
			return search(sequence, number, middle+1, upper)
		else:
			return search(sequence, number, lower, middle)

seq = [32,45,65,12,61,76]
seq.sort()
#print search(seq, 65)

seq = ['sdfd', '!@', 'sd23', '***']
def func(x):
	return x.isalnum()

#print filter(func, seq)
#print [x for x in seq if x.isalnum()]
#print filter(lambda x: x.isalnum(), seq)


seq = [32,45,65,12,61,76]
#print reduce(lambda x, y: x+y, seq)

__metaclass__ = type

class Person():
	__name = 'Default Name'
	num = 0
	
	def setName(self, name):
		self.__name = name
	
	def getName(self):
		return self.__name
	
	def greet(self):
		print "hello world! %s" % self.__name
		self.__greet()

	def __greet(self):
		print 'private greeting'

	def static(self):
		Person.num += 1


foo = Person()
foo.setName('Jason')
#foo.greet()
#foo.__greet()

foo.static()
#print Person.num
bar = Person()
bar.static()
#print Person.num


class Superman(Person):
	"""docstring for Superman"""
	__name = 'Clark'
	num = 1

	def __init__(self, value=None):
		if value is not None:
			self.__name = value

	def greet(self):
		print "Superman is me, %s" % self.__name

	def __del__(self):
		print "del the object"

clark = Superman()
#clark.setName('Clarkkkkk')
#print clark.getName()
#print clark.num
#clark.greet()

#print Superman.__bases__
#print clark.__class__

#x = raw_input('enter number1: ')
#y = raw_input('enter number2: ')
#try:
#	print int(x)/int(y)
# except ZeroDivisionError:
# 	print "number2 is zero"
# except TypeError:
# 	print "type is wrong"
# except ValueError:
# 	print "value is wrong"
#except (TypeError, ValueError), e:
#	print e

def checkIndex(key):
	if not isinstance(key, (int, long)):
		raise TypeError
	if key<0:
		raise IndexError

class MySeq():
	"""docstring for MySeq"""
	def __init__(self, start= 0, step=1):
		self.start = start
		self.step = step
		self.changed = {}

	def __getitem__(self, key):
		checkIndex(key)
		try:
			return self.changed[key]
		except KeyError, e:
			return self.start + key*self.step
	def __setitem__(self, key, value):
		checkIndex(key)
		self.changed[key] = value

s = MySeq(1,2)
#print s[4]


class Rec():
	"""docstring for Rec"""
	def __init__(self):
		self.width = 0
		self.height = 0
	def getSize(self):
		return self.width, self.height
	def setSize(self, size):
		self.width, self.height = size
	size = property(getSize, setSize)

r = Rec();
r.size = 12,6
#print r.size


mySets = []
for i in range(10):
	mySets.append(set(range(i, i+5)))
#print reduce(set.union, mySets)


from heapq import *
from random import shuffle

data = range(10)
shuffle(data)
#print data
heap = []
for n in data:
	heappush(heap, n)
#print heap
heappush(heap, 0.5)
#print heap
filename = '/home/jason/projects/learning-gist/python/install-pip.txt'
f = open(filename)
# while True:
# 	# char = f.read(1)
# 	# if not char: break
# 	# print char

# 	line = f.readline()
# 	if not line:break
# 	print line

# for x in f.readlines():
# 	print x

# for x in f:
# 	print x
f.close()

import fileinput
# for line in fileinput.input(filename):
# 	print line


# wxWedgit
import wx
def load(event):
	file = open(filename.GetValue())
	contents.SetValue(file.read())
	file.close()
def save(event):
	file = open(filename.GetValue(), 'w')
	file.write(contents.GetValue())
	file.close()

app = wx.App()
win = wx.Frame(None, title="Simple Test", size=(410, 335))
bkg = wx.Panel(win)

loadBtn = wx.Button(bkg, label="Open")
loadBtn.Bind(wx.EVT_BUTTON, load)

saveBtn = wx.Button(bkg, label="Save")
saveBtn.Bind(wx.EVT_BUTTON, save)

filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE|wx.HSCROLL)

hbox = wx.BoxSizer()
hbox.Add(filename, proportion=1, flag=wx.EXPAND)
hbox.Add(loadBtn, proportion=0, flag=wx.LEFT, border=5)
hbox.Add(saveBtn, proportion=0, flag=wx.LEFT, border=5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND|wx.ALL, border=5)
vbox.Add(contents, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=5)

bkg.SetSizer(vbox)
# win.Show()
# app.MainLoop()



from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF
# d= Drawing(100, 100)
# s = String(50, 50, 'Hello world', textAnchor='middle')
# d.add(s)

#renderPDF.drawToFile(d, 'hello.pdf', 'A Simple PDF File')

from reportlab.lib import colors
from reportlab.graphics.shapes import *
data = [
#year, month, predected, high, low
(2007, 12, 11.3, 11.4, 11.2),
(2008, 1, 12.3, 13.2, 12.1),
(2008, 2, 11.1, 11.5, 11.0),
(2008, 3, 30.3, 40.2, 30.5),
(2008, 4, 50.3, 40.3, 40.2),
(2008, 5, 40.7, 40.4, 40.1),
(2008, 6, 40.8, 40.5, 40.3),
(2008, 7, 40.1, 40.6, 40.2),
(2008, 8, 40.3, 50.7, 40.0)
]

drawing = Drawing(200, 150)
pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
times = [200*((row[0] + row[1]/12.0) -2007)-180 for row in data]

drawing.add(PolyLine(zip(times, pred), strokeColor=colors.blue))
drawing.add(PolyLine(zip(times, high), strokeColor=colors.red))
drawing.add(PolyLine(zip(times, low), strokeColor=colors.green))
drawing.add(String(65, 115, 'Sunspots', fontSize=18, fillColor=colors.red))

#renderPDF.drawToFile(drawing, 'report.pdf', 'Sunspots')

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from xml.sax import parse

class TestHandler(ContentHandler):
	def startElement(self, name, attrs):
		print name, attrs.keys()

parse('website.xml', TestHandler())







