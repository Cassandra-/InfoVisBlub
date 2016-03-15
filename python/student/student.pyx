#from system import stdout

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
				pass#stdout.write('no key %s\n'%(arg))
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
			once = False
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
					if tmp != set():
						once = True
				except: pass
			if not once:
				tot = set()
		else:
			tot = set()
			for key,value in kwargs.items():
				try:
					tmp = self._indexes[key].get(value,set())
					tot |= tmp
				except: pass
		return tot
		
	def students(self,idxes):
		return [(self._data[i] if type(i) == int else i) for i in idxes]

class Student:
	def __init__(self,_year,_from,_to):
		self._year = _year
		self._from = _from
		self._to   = _to
	
	def __str__(self):
		return '[Student: (%s) from:%s, to:%s]'%(str(self._year),str(self._from),str(self._to) )

#===== DATA LOADING
def read(filename,DATA):
	f = open(filename,'r')

	cur_year = filename[-8:-4].lower().strip()
	
	f.readline()
	labels = [label.strip().lower() for label in f.readline().split(';')[:-1]]
	ftype = []
	ttype = []
	if 'Doorstroom HAVO-VWO to HBO-WO' in filename:
		splitter = 7
		from_labels = ['brin nr','vest nr','gem nr','gemeente','type','diploma','sector']
		to_labels = ['brin nr','type','sector','gem nr','gemeente']
	elif 'Doorstroom HAVO-VWO to MBO' in filename:
		splitter = 7
		from_labels = ['brin nr','vest nr','gem nr','gemeente','type','diploma','sector']
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
		#stdout.write('wrong file\n')
		return
	
	x = 0
	for line in f:
		x += 1
		#if x % 5000 == 0:
			#stdout.write('\rat %s %s %s           '%(filename,cur_year,x) )
		data = [i.strip().lower().replace('/','_') for i in line.split(';')]
		num = int(data[-1])
		_from = tuple(zip(from_labels,data[:splitter]+ftype))
		_to = tuple(zip(to_labels,data[splitter:-1]+ttype))
		for i in range(num):
			s = Student(cur_year,_from,_to)
			DATA.add(s)
	#stdout.write('\r')
	
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

	return DATA