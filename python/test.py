from __future__ import division, absolute_import, print_function#, unicode_literals

import os
from sys import stdout
from time import time
from flask import Flask

app = Flask(__name__)

def writenow(*args):
    stdout.write("\r%s          " % ' '.join([str(a) for a in args])); stdout.flush()
def nl():
    stdout.write("\n")
def cl():
	stdout.write("\r"); stdout.flush()

class StudentDict:
	def __init__(self):
		self._data = []
		self._indexes = {'year':{}}
	
	def _adder(self,index,key,value):
		tmp = self._indexes.get(key,{})
		tmp2 = tmp.get(value,set())
		tmp2.add(index)
		tmp[value] = tmp2
		self._indexes[key] = tmp
	
	def keys(self):
		return self._indexes.keys()
	
	def add(self,student):
		index = len(self._data)
		self._data.append(student)
		# year
		tmp = self._indexes['year'].get(student._year,set())
		tmp.add(index)
		self._indexes['year'][student._year] = tmp
		# from
		for key,value in student._from:
			if (value == 'diploma'): value = True
			elif (value == 'geen diploma'): value = False
			self._adder(index,'f'+key,value)
			self._adder(index,key,value)
		# to
		for key,value in student._to:
			if (value == 'diploma'): value = True
			elif (value == 'geen diploma'): value = False
			self._adder(index,'t'+key,value)
			self._adder(index,key,value)
	
	def __len__(self):
		return len(self._data)
	
	def __add__(self,other):
		assert type(other) == type(self)
		ans = StudentDict()
		for student in self._data:
			ans.add(student)
		for student in other._data:
			ans.add(student)
		return ans
	
	def __radd__(self,other):
		return self.__add__(other)
	
	def __iadd__(self,other):
		return self.__add__(other)
	
	def __call__(self,*args,**kwargs):
		if False not in args:
			tot = set(range(0,len(self._data)))
			for key,value in kwargs.iteritems():
				try:
					tmp = self._indexes[key].get(value,set())
					tot &= tmp
				except: writenow('no key',key); nl()
		else:
			tot = set()
			for key in args:
				if key:
					tmp = set(self._indexes[key].keys())
					tot |= tmp
			for key,value in kwargs.iteritems():
				try:
					tmp = self._indexes[key].get(value,set())
					tot |= tmp
				except: writenow('no key',key); nl()
		return [(self._data[i] if type(i) == int else i) for i in tot]

class Student:
	def __init__(self,_year,_from,_to):
		self._year = _year
		self._from = _from
		self._to   = _to
	
	def __str__(self):
		return '[Student: (%s) from:%s, to:%s]'%(str(self._year),str(self._from),str(self._to) )

def read(filename,DATA):
	f = open(filename,'r')

	cur_year = filename[-8:-4].lower().strip()
	
	f.readline()
	labels = [label.strip().lower() for label in f.readline().split(';')[:-1]]
	
	if 'Doorstroom HAVO-VWO to HBO-WO' in filename:
		splitter = 7
		from_labels = ['brin nr','vest nr','gem nr','gemeente','type','diploma','profiel']
		to_labels = ['brin nr','type','profiel','gem nr','gemeente']
	elif 'Doorstroom HAVO-VWO to MBO' in filename:
		splitter = 7
		from_labels = ['brin nr','vest nr','gem nr','gemeente','type','diploma','profiel']
		to_labels = ['brin nr','leerweg','sector','kwalificatie','kwalif code','brin nr kc','kenniscentrum','gem nr','gemeente']
	elif 'Doorstroom VMBO to MBO' in filename:
		splitter = 7
		from_labels = ['brin nr','vest nr','gem nr','gemeente','leerweg','sector','afdeling']
		to_labels = ['brin nr','sector','kwalificatie','kwalif code','brin nr kc','kenniscentrum']
	elif 'Doorstroom MBO to HBO' in filename:
		splitter = 5
		from_labels = ['brin nr','instelling','sector','leerweg','niveau']
		to_labels = ['brin nr','instelling','croho']
	elif 'Doorstroom PO to VO' in filename:
		splitter = 5
		from_labels = ['brin nr','vest nr','instelling','straat','gemeente']
		to_labels = ['brin nr','vest nr','instelling','straat','gemeente']
	else:
		writenow('wrong file\n')
		return
	
	x = 0
	for line in f:
		x += 1
		if x % 5000 == 0:
			writenow('at',filename,cur_year,x)
		data = [i.strip().lower() for i in line.split(';')]
		num = int(data[-1])
		_from = tuple(zip(from_labels,data[:splitter]))
		_to = tuple(zip(to_labels,data[splitter:-1]))
		for i in range(num):
			s = Student(cur_year,_from,_to)
			DATA.add(s)
	cl()
	
	return DATA

def build_database():
	DATA = StudentDict()

	for root, _, files in os.walk('..'):
		for file in files:
			if file[-4:] == '.csv':
				read(os.path.join(root, file), DATA)
	return DATA

@app.route('/count/<ftype>')
def count(ftype):
    return str(len(DATA(ftype=ftype)))

@app.route('/from/<ftype>/to/<ttype>')
def from_to(ftype, ttype):
    return str(len(DATA(ftype=ftype, ttype=ttype)))
	
def main():
	t1 = time()
	global DATA
	DATA = build_database()
	t1 = time() - t1
	writenow('\n','loaded in',t1,'seconds. Total of',len(DATA),'students\n')
	writenow(len(DATA(ftype='vwo')),'did vwo of which',len(DATA(ftype='vwo',ttype='wo')),'went to wo\n')
	writenow('all keys of type are:',DATA(False,'type'))
	app.run()
	
if __name__ == '__main__':
	main()
