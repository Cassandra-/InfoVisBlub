from __future__ import division, absolute_import, print_function#, unicode_literals

print( "You should run from the project root." )

from sys import stdout
from time import time
from flask import Flask
import os
import random
import json

RESOURCES = ['./javascript']

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
		
	def allkeys(self,*args):
		ans = set()
		for arg in args:
			try:
				ans |= set(self._indexes[arg].keys())
			except:
				writenow('no key',arg);nl()
		return ans
	
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
			for key,value in kwargs.items():
				try:
					if type(value) == list:
						tmp = set()
						for v in value:
							tmp |= self._indexes[key].get(v,set())
					else:
						tmp = self._indexes[key].get(value,set())
					tot &= tmp
				except: writenow('no key',key); nl()
			if len(tot) == len(self):
				tot = set()
		else:
			tot = set()
			for key in args:
				if key:
					tmp = set(self._indexes[key].keys())
					tot |= tmp
			for key,value in kwargs.items():
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
	ftype = []
	ttype = []
	if 'Doorstroom HAVO-VWO to HBO-WO' in filename:
		splitter = 7
		from_labels = ['brin nr','vest nr','gem nr','gemeente','type','diploma','profiel']
		to_labels = ['brin nr','type','profiel','gem nr','gemeente']
	elif 'Doorstroom HAVO-VWO to MBO' in filename:
		splitter = 7
		from_labels = ['brin nr','vest nr','gem nr','gemeente','type','diploma','profiel']
		to_labels = ['brin nr','leerweg','sector','kwalificatie','kwalif code','brin nr kc','kenniscentrum','gem nr','gemeente']+['type']
		ttype = ['mbo']
	elif 'Doorstroom VMBO to MBO' in filename:
		splitter = 7
		ftype,ttype = ['vmbo'],['mbo']
		from_labels = ['brin nr','vest nr','gem nr','gemeente','leerweg','sector','afdeling']+['type']
		to_labels = ['brin nr','sector','kwalificatie','kwalif code','brin nr kc','kenniscentrum']+['type']
	elif 'Doorstroom MBO to HBO' in filename:
		splitter = 5
		ftype,ttype = ['mbo'],['hbo']
		from_labels = ['brin nr','instelling','sector','leerweg','niveau']+['type']
		to_labels = ['brin nr','instelling','croho']+['type']
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
		data = [i.strip().lower().replace('/','_') for i in line.split(';')]
		num = int(data[-1])
		_from = tuple(zip(from_labels,data[:splitter]+ftype))
		_to = tuple(zip(to_labels,data[splitter:-1]+ttype))
		for i in range(num):
			s = Student(cur_year,_from,_to)
			DATA.add(s)
	cl()
	
	return DATA

def build_database(small=10):
	DATA = StudentDict()
	read('./Doorstroom HAVO-VWO to HBO-WO/03 Doorstroom havo-vwo naar ho in 2011.csv',DATA)
	if (small > 0):
		read('./Doorstroom HAVO-VWO to MBO/02 Doorstroom havo-vwo naar mbo in 2011.csv',DATA)
		read('./Doorstroom MBO to HBO/04. Doorstroom mbo naar ho in 2011.csv',DATA)
		read('./Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2011.csv',DATA)
	if (small > 1):
		read('./Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2012.csv',DATA)
		read('./Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2013.csv',DATA)
		read('./Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2014.csv',DATA)
		read('./Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2012.csv',DATA)
		read('./Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2013.csv',DATA)
		read('./Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2014.csv',DATA)
	if (small > 2):
		read('./Doorstroom MBO to HBO/04 Doorstroom van mbo naar hbo in 2012.csv',DATA)
		read('./Doorstroom MBO to HBO/04. Doorstroom mbo naar hbo in 2013.csv',DATA)
		read('./Doorstroom MBO to HBO/04. Doorstroom mbo naar hbo in 2014.csv',DATA)
		read('./Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2012.csv',DATA)
		read('./Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2013.csv',DATA)
		read('./Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2014.csv',DATA)
		read('./Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2014.csv',DATA)
	if (small > 3):
		read('./Doorstroom PO to VO/05. Doorstroom po naar vo in 2012.csv',DATA)
		read('./Doorstroom PO to VO/05. Doorstroom po naar vo in 2013.csv',DATA)
		read('./Doorstroom PO to VO/05. Doorstroom po naar vo in 2014.csv',DATA)

	#for root, _, files in os.walk('..'):
	#	for file in files:
	#		if file[-4:] == '.csv':
	#			read(os.path.join(root, file), DATA)
	return DATA

@app.route('/list1/build')
def list1_build():
	out = "<table>\n"
	for key in list(DATA.allkeys('sector','profiel') ):
		out += '<tr><td><input type="checkbox" onclick="change_sector(\'%s\',this.checked)"></td><td>%s</tr>\n'%(key,key)
	return out+"<table>"

@app.route('/list1/select/<name>/<bool>')
def list1_select(name,bool):
	global profiel_keys
	print(name, bool, bool=='true')
	if bool == 'true':
		if profiel_keys == DATA.allkeys('sector','profiel'):
			profiel_keys = set([name])
		else:
			profiel_keys.add(name)
	else:
		profiel_keys.discard(name)
		if profiel_keys == set():
			profiel_keys = DATA.allkeys('sector','profiel')
	print(profiel_keys)
	return "okay"
	
@app.route('/keys/<query>')
def returnkeys(query):
	print(query)
	args,kwargs = str2arg(query)
	print(args)
	keys = DATA.allkeys(*args)
	return json.dumps(keys)
	
def str2arg(i):
	s = i.split(';')
	l,d = [], {}
	for e in s:
		if '=' in e:
			k,v = e.split('=')
			d[k] = v
		else:
			if e.lower() == 'false':
				l.append(False)
			else:
				l.append(e)
	return l,d

@app.route('/count/<query>')
def count(query):
	print( query )
	args,kwargs = str2arg(query)
	print( args,kwargs )
	return str(len(DATA(*args, **kwargs )))

def get(keys,args=[],kwargs={}):
	ans = []
	for (i1,k1),(i2,k2) in [(i,j) for i in enumerate(keys) for j in enumerate(keys)]:
		n = len(DATA(*args,ftype=k1,ttype=k2,**kwargs) )
		if n > 0:
			ans.append((i1,i2,n))
	return ans

@app.route('/sankey/update')
def sankey_update():
	types = list(DATA.allkeys('type') )
	profiles = list(profiel_keys)
	args,kwargs = [], {'sector':profiles,'profiel':profiles}
	obj = {"nodes": [{"name":i} for i in types],
			"links": [{"source":s,"target":t,"value":v} for s,t,v in get(types,args,kwargs)]
		}
	print(obj)
	return json.dumps(obj)
	

@app.route('/test3/<query>')
def test3(query):
	print( query)
	args,kwargs = str2arg(query)
	keys = DATA(False,'type')
	print(keys)
	print(args,kwargs)
	obj = {"nodes": [{"name":i} for i in keys],
			"links": [{"source":s,"target":t,"value":v} for s,t,v in get(keys,args,kwargs)]
		}
	print( obj)
	return json.dumps(obj)

@app.route('/test2')
def test2():
	keys = DATA(False,'type')
	print(keys)
	obj = {"nodes": [{"name":i} for i in keys],
			"links": [{"source":s,"target":t,"value":v} for s,t,v in get(keys)]
		}
	print( obj)
	return json.dumps(obj)

@app.route('/test')
def test():
	energy = {"nodes":[
							{"name":"hello"},
							{"name":"world"},
							{"name":"ding"},
							{"name":"blub"}
						],
			  "links":[
							{"source":0,"target":1,"value":123},
							{"source":0,"target":2,"value":13},
							{"source":0,"target":3,"value":31},
							{"source":1,"target":3,"value":131}
						]
					}
	print(energy)
	return json.dumps(energy)

@app.route('/')
def index():
	return open('./javascript/dashbord.htm','r').read()

@app.route('/oldmain')
def index_old():
	return open('./javascript/test.htm','r').read()

	
def init():
	for r in RESOURCES:
		files = os.listdir(r)
		for file in files:
			com = "@app.route('%s')\ndef %s():\n\treturn open('%s','r').read()"%(
				r[1:]+'/'+file,'f'+str(random.random())[2:],r+'/'+file)
			print(com)
			exec( com)


def main():
	init()
	t1 = time()
	global DATA, profiel_keys
	DATA = build_database(0)
	t1 = time() - t1
	writenow('\n','loaded in',t1,'seconds. Total of',len(DATA),'students\n')
	
	profiel_keys = DATA.allkeys('profiel','sector')
	
	#writenow(len(DATA(ftype='vwo')),'did vwo of which',len(DATA(ftype='vwo',ttype='wo')),'went to wo\n')
	#writenow('all keys of type are:',DATA(False,'type'))
	app.run()
	
if __name__ == '__main__':
	main()
