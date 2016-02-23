from __future__ import division, absolute_import, print_function#, unicode_literals

from sys import stdout

def writenow(*args):
    stdout.write("\r%s          " % ' '.join([str(a) for a in args])); stdout.flush()
def nl():
    stdout.write("\n")
def cl():
	stdout.write("\r"); stdout.flush()

#year = 'year'
#city_from = 'Acityfrom'
#city_to = 'Acityto'
#has_diploma = 'Ahasdip'
#school_from = 'Aschfrom'
#school_to = 'Aschto'

#niveau = 'Kniv'
#profile = 'Kprov'
#leerweg = 'Klweg'
#sector = 'Ksec'
#kwalificatie = 'Kkwal'
#instelling = 'Kinst'

#f = 'Tfrom'
#t = 'Tto'


class StudentDict:
	def __init__(self):
		self._data = []
		self._indexes = {'year':{}}
			#year:{},city_from:{},city_to:{},has_diploma:{},
			#	niveau:{},profile:{},
		#		leerweg:{},sector:{},kwalificatie:{},instelling:{}
		#	}
		# self._city_from = {}
		# self._niveau_from = {}
		# self._profile_from = {}
		# self._has_diploma = {}
		# self._city_to = {}
		# self._niveau_to = {}
		# self._profile_to = {}
	
	def _adder(self,index,key,value):
		tmp = self._indexes.get(key,{})
		tmp2 = tmp.get(value,set())
		tmp2.add(index)
		tmp[value] = tmp2
		self._indexes[key] = tmp
	
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
			'''tmp = self._indexes.get('f'+key,{})
			tmp2 = tmp.get(value,set())
			tmp2.add(index)
			tmp[value] = tmp2
			self._indexes['f'+key] = tmp
			
			tmp = self._indexes.get(key,{})
			tmp2 = tmp.get(value,set())
			tmp2.add(index)
			tmp[value] = tmp2
			self._indexes[key] = tmp'''
		# to
		for key,value in student._to:
			if (value == 'diploma'): value = True
			elif (value == 'geen diploma'): value = False
			self._adder(index,'f'+key,value)
			self._adder(index,key,value)
			'''tmp = self._indexes.get('t'+key,{})
			tmp2 = tmp.get(value,set())
			tmp2.add(index)
			tmp[value] = tmp2
			self._indexes['t'+key] = tmp
			
			tmp = self._indexes.get(key,{})
			tmp2 = tmp.get(value,set())
			tmp2.add(index)
			tmp[value] = tmp2
			self._indexes[key] = tmp'''
		
	def add_old(self,student):
		index = len(self._data)
		self._data.append(student)
		# year
		tmp = self._indexes[year].get(student.year,set())
		tmp.add(index)
		self._indexes[year][student.year] = tmp
		# city from
		tmp = self._indexes[city_from].get(student.city_from,set())
		tmp.add(index)
		self._indexes[city_from][student.city_from] = tmp
		# city to
		tmp = self._indexes[city_to].get(student.city_to,set())
		tmp.add(index)
		self._indexes[city_to][student.city_to] = tmp
		# has diploma
		tmp = self._indexes[has_diploma].get(student.has_diploma,set())
		tmp.add(index)
		self._indexes[has_diploma][student.has_diploma] = tmp
		# school from
		for key,value in student.school_from:
			tmp = self._indexes[key].get(value,set())
			tmp.add(index)
			self._indexes[key][value] = tmp
		# school to
		for key,value in student.school_to:
			tmp = self._indexes[key].get(value,set())
			tmp.add(index)
			self._indexes[key][value] = tmp
		return
	
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
	
	def __getitem__(self,keys):
		if type(keys) != tuple:
			keys = (keys,)
		if False not in keys:
			tot = set(range(0,len(self._data)))
			for key in keys:
				try:
					if key.step is None:
						tmp = self._indexes[key.start].get(key.stop,set())
					else:
						tmp = self._indexes[key.start+key.stop].get(key.step,set())
					tot &= tmp
				except: writenow('no key',key); nl()
		else:
			tot = set()
			for key in keys:
				try:
					if not key.step:
						tmp = self._indexes[key.start].get(key.stop,set())
					else:
						tmp = self._indexes[key.start+key.stop].get(key.step,set())
					tot |= tmp
				except: writenow('no key','key'); nl()
		return [self._data[i] for i in tot]		

class Student_old:	
	def __init__(self,year,city_from,city_to,school_from,school_to,has_diploma):
		self.year = year
		self.city_from = city_from
		self.city_to = city_to
		self.school_from = school_from
		self.school_to = school_to
		self.has_diploma = has_diploma
		
	def __str__(self):
		return 'Student: (%s) (from: %s-%s (%s) to: %s-%s)'%(
					str(self.year),
					str(self.city_from),str(self.school_from),
					str(self.has_diploma),
					str(self.city_to),str(self.school_to) )

class Student:
	def __init__(self,_year,_from,_to):
		self._year = _year
		self._from = _from
		self._to   = _to
	
	def __str__(self):
		return '[Student: (%s) from:%s, to:%s]'%(str(self._year),str(self._from),str(self._to) )

class HO:
	def __init__(self,niveau,profile):
		self.niveau = niveau
		self.profile = profile
	
	def __str__(self):
		return '%s-%s'%(self.niveau,self.profile)
	
	def __hash__(self):
		return self.niveau.__hash__() + 31* self.profile.__hash__()
	
class MBO:
	def __init__(self,leerweg,sector,kwalificatie,instelling):
		self.leerweg = leerweg
		self.sector = sector
		self.kwalificatie = kwalificatie
		self.instelling = instelling
	
	def __str__(self):
		return 'mbo(%s):%s-%s(%s)'%(self.leerweg,self.sector,self.kwalificatie,self.instelling)
	
	def __hash__(self):
		return self.leerweg.__hash__() + 7* self.sector.__hash__() + \
				11* self.kwalificatie.__hash__() + 13* self.instelling.__hash__()
		
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
		to_labels = ['brin nr','leerweg','sector','kwalificatie','kwalif code','brin nr kc','kenniscentrum','gemeente']
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
		if x % 2000 == 0:
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

	n = '''
	for line in f:
		x += 1
		if x % 10000 == 0:
			writenow('at',cur_year,x)
		data = line.split(';')
		num = int(data[-1])
		if len(data) == 13:
			city_from = data[3].lower().strip()
			city_to = data[-2].lower().strip()
			has_diploma = data[5].lower().strip() == 'diploma'
			school_from = ((niveau,data[4].lower().strip()), (profile,data[6].lower().strip()) )
			school_to = ((niveau,data[8].lower().strip()), (profile,data[9].lower().strip()) )
			#school_from = HO(data[4].lower().strip(), data[6].lower().strip() )
			#school_to = HO(data[8].lower().strip(), data[9].lower().strip() )
		elif len(data) == 17:
			city_from = data[3].lower().strip()
			city_to = data[-2].lower().strip()
			has_diploma = data[5].lower().strip() == 'diploma'
			school_from = ((niveau,data[4].lower().strip()), (profile,data[6].lower().strip()) )
			school_to = ((leerweg,data[8].lower().strip()), (sector,data[9].lower().strip()),
							(kwalificatie,data[10].lower().strip()), (instelling,data[13].lower().strip()) )
		
		for i in range(num):
			s = Student(cur_year, city_from, city_to, school_from, school_to, has_diploma)
			DATA.add(s)			
	cl()
	#print '\n'.join(str(i) for i in DATA._data)
	#print ''
	#print '\n'.join(str(i) for i in DATA[profile_from:'nat/gezond',profile_to:'techniek',year:'2011',True] )
	return DATA
	'''

def build_database():
	DATA = StudentDict()
	read('../Doorstroom PO to VO/05. Doorstroom po naar vo in 2012.csv',DATA)
	read('../Doorstroom PO to VO/05. Doorstroom po naar vo in 2013.csv',DATA)
	read('../Doorstroom PO to VO/05. Doorstroom po naar vo in 2014.csv',DATA)
	read('../Doorstroom MBO to HBO/04. Doorstroom mbo naar ho in 2011.csv',DATA)
	read('../Doorstroom MBO to HBO/04 Doorstroom van mbo naar hbo in 2012.csv',DATA)
	read('../Doorstroom MBO to HBO/04. Doorstroom mbo naar hbo in 2013.csv',DATA)
	read('../Doorstroom MBO to HBO/04. Doorstroom mbo naar hbo in 2014.csv',DATA)
	read('../Doorstroom HAVO-VWO to HBO-WO/03 Doorstroom havo-vwo naar ho in 2011.csv',DATA)
	read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2012.csv',DATA)
	read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2013.csv',DATA)
	read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2014.csv',DATA)
	read('../Doorstroom HAVO-VWO to MBO/02 Doorstroom havo-vwo naar mbo in 2011.csv',DATA)
	read('../Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2012.csv',DATA)
	read('../Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2013.csv',DATA)
	read('../Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2014.csv',DATA)
	read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2011.csv',DATA)
	read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2012.csv',DATA)
	read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2013.csv',DATA)
	read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2014.csv',DATA)
	read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2014.csv',DATA)
	return DATA
	#print len(DATA._data)
	#print '\n'.join(str(i) for i in DATA[city_to:'amsterdam',profile_from:'nat/gezond',profile_to:'techniek',year:'2011',True] )
	#print len(DATA[niveau_from:'vwo',niveau_to:'wo',year:'2014']),len(DATA[niveau_from:'vwo',year:'2014']),len(DATA[niveau_from:'vwo',niveau_to:'hbo',year:'2014'])

def main():
	DATA = build_database()
	writenow('\n',len(data),'\n')
	
if __name__ == '__main__':
	main()