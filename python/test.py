#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import math

print "Enter a number:"
num = int(sys.stdin.readline())
to = int(math.sqrt(num))
ret = True
for i in range(2, to):
    if num % i == 0:
        ret = False
        break
if ret :
    print "YES"
else:
    print "NO"
	
	
#str = sys.stdin.readline()
#numbers = str.split(' ')
#ret = 0
#for n in numbers:
#	ret += n
#print ret

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
	NUM = 0
	
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
		Person.NUM += 1
	def property(self):
		self.num += 1


foo = Person()
foo.setName('Jason')
foo.greet()
#foo.__greet() #无法调用隐藏方法

foo.static()
foo.property()
print Person.NUM #结果为1
print foo.num

bar = Person()
bar.static() # 结果为2，因为Person.num是静态调用, self.num才是instance内部的变量
bar.property()
print Person.NUM
print bar.NUM
print bar.num


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
		print "del the object, Class Superman"

clark = Superman()
clark.setName('Clarkkkkk')
print clark.getName()
print clark.num
clark.greet()

print Superman.__bases__
print clark.__class__

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
s[1] = 'haha'
print s[4]
print s[1]
# __getitem__ 和 __setitem__ 是 []下标操作的接口


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
print data
heap = []
for n in data:
	heappush(heap, n)
print heap
heappush(heap, 0.5)
print heap


string = r"This is a long string\
with a backslash and a new line in it."
#这里的r表示原样输出，这里的\转义会被忽略
print string

print string.isdigit()
print string.upper()
print string.count('needle')
lines = string.splitlines()
print lines
#遍历每个字符
for c in string:
	pass

print ord('a')
print chr(97)
print ord(u'天')
print repr(unichr(22825))

def is_string(string):
	return isinstance(string, basestring)

print is_string('test')
#字符串反转
print string[::-1]

# import string
# def translator(frm='', to='', del='', keep=None):
# 	if len(to)==1:
# 		to = to*len(frm)
# 	trans = string.maketrans(frm, to)
# 	if keep is not None:
# 		allchars = string.maketrans('', '')
# 		del = allchars.translate(allchars, 
# 			keep.translate(allchars, del))
# 	def translate(s):
# 		return s.translate(trans, del)
# 	return translate


def read_file_by_chunks(filename, chunksize=100):
	file_obj = open(filename)
	while True:
		chunk = file_obj.read(chunksize)
		if not chunk:
			break
		yield chunk
	file_obj.close()

#默认按行遍历文件中的内容(最常用方法)
# for line in open('/tmp/python.txt', 'rU'):
# 	print line.rstrip('\n')

#按chunk遍历文件内容，得益于yield的使用
# for chunk in read_file_by_chunks('/tmp/python.txt'):
# 	print chunk.rstrip('\n')

#关于logging搜索"python TimedRotatingFileHandler"

def already_converted(url):
    return '?' in url and 'lqd=' in url and 'lcode=' in url

print  'Test for string contains', already_converted('http://tv.sohu.com/20150510/n412776646.shtml?lcode=AAAASRKIxcEXJgTE8izsN5WNN68rTFA6JHt8IWfMlNKJYRD_pSYV-XynPPgnpx8M_FWOVMBj0TWm_yY5twhLvHT4PFME-YPtilAk_xwcE3GKniMusk5&lqd=14444')


def testargs(first, *args, **kwargs):
	print first
	print args
	print kwargs
	pass

testargs("haha", "2", 3, a=1, b=2)