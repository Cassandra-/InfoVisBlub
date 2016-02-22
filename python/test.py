
year = 'y'
city_from = 'cf'
niveau_from = 'nf'
profile_from = 'pf'
has_diploma = 'hp'
city_to = 'cf'
niveau_to = 'nf'
profile_to = 'pf'


class StudentDict:
	def __init__(self):
		self._data = []
		self._indexes = {year:{},city_from:{},city_to:{},niveau_from:{},niveau_to:{},profile_from:{},profile_to:{},has_diploma:{}}
		# self._city_from = {}
		# self._niveau_from = {}
		# self._profile_from = {}
		# self._has_diploma = {}
		# self._city_to = {}
		# self._niveau_to = {}
		# self._profile_to = {}
	
	def add(self,student):
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
		# niveau from
		tmp = self._indexes[niveau_from].get(student.niveau_from,set())
		tmp.add(index)
		self._indexes[niveau_from][student.niveau_from] = tmp
		# profile from
		tmp = self._indexes[profile_from].get(student.profile_from,set())
		tmp.add(index)
		self._indexes[profile_from][student.profile_from] = tmp
		# has diploma
		tmp = self._indexes[has_diploma].get(student.has_diploma,set())
		tmp.add(index)
		self._indexes[has_diploma][student.has_diploma] = tmp
		# city to
		tmp = self._indexes[city_to].get(student.city_to,set())
		tmp.add(index)
		self._indexes[city_to][student.city_to] = tmp
		# niveau to
		tmp = self._indexes[niveau_to].get(student.niveau_to,set())
		tmp.add(index)
		self._indexes[niveau_to][student.niveau_to] = tmp
		# profile to
		tmp = self._indexes[profile_to].get(student.profile_to,set())
		tmp.add(index)
		self._indexes[profile_to][student.profile_to] = tmp
	
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
			tot = set(xrange(0,len(self._data)))
			for key in keys:
				try:
					tmp = self._indexes[key.start].get(key.stop,set())
					tot &= tmp
				except: pass
		else:
			tot = set()
			for key in keys:
				try:
					tmp = self._indexes[key.start].get(key.stop,set)
					tot |= tmp
				except: pass
		return [self._data[i] for i in tot]		

class Student:	
	def __init__(self,year,city_from,niveau_from,has_diploma,profile_from,niveau_to,profile_to,city_to):
		self.year = year
		self.city_from = city_from
		self.niveau_from = niveau_from
		self.has_diploma = has_diploma
		self.profile_from = profile_from
		self.niveau_to = niveau_to
		self.profile_to = profile_to
		self.city_to = city_to
	
	def __str__(self):
		return 'Student: (%s) (from: %s %s %s; %s; to: %s %s %s)'%(
					str(self.year),
					str(self.city_from),str(self.niveau_from),str(self.profile_from),
					str(self.has_diploma),
					str(self.city_to),str(self.niveau_to),str(self.profile_to) )

def read(filename,DATA):
	f = open(filename,'r')

	cur_year = filename[-8:-4].lower().strip()
	print cur_year
	
	f.readline()
	f.readline()
	
	#DATA = StudentDict()
	for line in f:
		data = line.split(';')
		num = int(data[-1])
		for i in range(num):
			s = Student(cur_year,
						data[3].lower().strip(),
						data[4].lower().strip(),
						data[5].lower().strip() == 'diploma', 
						data[6].lower().strip(),
						data[8].lower().strip(),
						data[9].lower().strip(),
						data[-2].lower().strip() )
			DATA.add(s)
	#print '\n'.join(str(i) for i in DATA._data)
	#print ''
	#print '\n'.join(str(i) for i in DATA[profile_from:'nat/gezond',profile_to:'techniek',year:'2011',True] )
	return DATA

def build_database():
	DATA = StudentDict()
	read('../Doorstroom HAVO-VWO to HBO-WO/03 Doorstroom havo-vwo naar ho in 2011.csv',DATA)
	read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2012.csv',DATA)
	read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2013.csv',DATA)
	read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2014.csv',DATA)
	print len(DATA._data)
	print '\n'.join(str(i) for i in DATA[city_to:'amsterdam',profile_from:'nat/gezond',profile_to:'techniek',year:'2011',True] )
	print len(DATA[niveau_from:'vwo',niveau_to:'wo',year:'2014']),len(DATA[niveau_from:'vwo',year:'2014']),len(DATA[niveau_from:'vwo',niveau_to:'hbo',year:'2014'])
	
	
if __name__ == '__main__':
	build_database()