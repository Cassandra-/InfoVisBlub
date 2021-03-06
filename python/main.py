from __future__ import division, absolute_import, print_function#, unicode_literals

print( "You should run from the project root." )

from sys import stdout, argv
from time import time
from flask import Flask, Response
import os
import random
import json
import csv

RESOURCES = ['./javascript','./javascript/utils','./Flow','./Geomap', './Geomap/Flow']

app = Flask(__name__)

def writenow(*args):
    stdout.write("\r%s          " % ' '.join([str(a) for a in args])); stdout.flush()
def nl():
    stdout.write("\n")
def cl():
	stdout.write("\r"); stdout.flush()

#=====StudentDict objects
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
			once = False
			tot = set(range(0,len(self._data)))
			for key,value in kwargs.items():
				try:
					if type(value) == list or type(value) == tuple:
						tmp = set()
						for v in value:
							tmp |= self._indexes[key].get(v,set())
					else:
						tmp = self._indexes[key].get(value,set())
					tot &= tmp
					if tmp != set():
						once = True
				except: pass#writenow('no key',key); nl()
			if not once:
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
				except: pass#writenow('no key',key); nl()
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
		from_labels = ['brin_nr','vest_nr','gem_nr','gemeente','type','diploma','sector']
		to_labels = ['brin_nr','type','sector','gem_nr','gemeente']
	elif 'Doorstroom HAVO-VWO to MBO' in filename:
		splitter = 7
		from_labels = ['brin_nr','vest_nr','gem_nr','gemeente','type','diploma','sector']
		to_labels = ['brin_nr','leerweg','sector','kwalificatie','kwalif code','brin_nr_kc','kenniscentrum','gem_nr','gemeente']+['type']
		ttype = ['mbo']
	elif 'Doorstroom VMBO to MBO' in filename:
		splitter = 7
		ftype,ttype = ['vmbo'],['mbo']
		from_labels = ['brin_nr','vest_nr','gem_nr','gemeente','leerweg','sector','afdeling']+['type']
		to_labels = ['brin_nr','sector','kwalificatie','kwalif code','brin_nr kc','kenniscentrum']+['type']
	elif 'Doorstroom MBO to HBO' in filename:
		splitter = 5
		ftype,ttype = ['mbo'],['hbo']
		from_labels = ['brin_nr','instelling','sector','leerweg','niveau']+['type']
		to_labels = ['brin_nr','instelling','croho']+['type']
	elif 'Doorstroom PO to VO' in filename:
		splitter = 5
		from_labels = ['brin_nr','vest_nr','instelling','straat','gemeente']
		to_labels = ['brin_nr','vest_nr','instelling','straat','gemeente']
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

#===== SERVER STUFF
@app.route('/years/<begin>/<end>')
def set_years(begin,end):
	global years
	begin,end = int(float(begin)),int(float(end))
	years = [str(begin+i) for i in range(end-begin+1)]
	print( 'years now',years)
	return "okay"

@app.route('/list1/build')
def list1_build():
	out = "<table>\n<tr><td><i>from</i></td><td><i>to</i></td><td><i>name</i></td></tr></i>"
	tot = []
	idn=0
	for key in list(DATA.allkeys('sector') ):
		tch = fch = tgo = fgo = ''
		tnum = len(DATA(fsector=list(fprofiel_keys),tsector=key)) 
		fnum = len(DATA(tsector=list(tprofiel_keys),fsector=key))
		
		if tnum == 0:
			tgo = 'disabled="disabled"'
			tprofiel_keys.discard(key)
		if fnum == 0:
			fgo = 'disabled="disabled"'
			fprofiel_keys.discard(key)
		
		if key in tprofiel_keys:
			tch = 'checked="true"'
		if key in fprofiel_keys:
			fch = 'checked="true"'
		
		a = (fnum+tnum, '<tr id="mytr%d">\
<td><input type="checkbox" %s %s onclick="change_sector(\'%s\',this.checked,true)">\
<td><input type="checkbox" %s %s onclick="change_sector(\'%s\',this.checked,false)">\
</td><td>%s</tr>\r\n'%(idn,fch,fgo,key,tch,tgo,key,key)
		    )
		tot.append(a)
		idn += 1
	tot.sort(key=lambda a: -a[0])
	out += ' '.join([x for n,x in tot])
	return out+"</table>"

@app.route('/list1/select/<name>/<bool>/<t>')
def list1_select(name,bool,t):
	global tprofiel_keys,fprofiel_keys
	if t == 'true':
		if bool == 'true':
			if fprofiel_keys == DATA.allkeys('sector'):
				fprofiel_keys = set([name])
			else:
				fprofiel_keys.add(name)
		else:
			fprofiel_keys.discard(name)
			if fprofiel_keys == set():
				fprofiel_keys = DATA.allkeys('sector')
	else:
		if bool == 'true':
			if tprofiel_keys == DATA.allkeys('sector'):
				tprofiel_keys = set([name])
			else:
				tprofiel_keys.add(name)
		else:
			tprofiel_keys.discard(name)
			if tprofiel_keys == set():
				tprofiel_keys = DATA.allkeys('sector')
	
	return list1_build()
	
@app.route('/keys/<query>')
def returnkeys(query):
	print(query)
	args,kwargs = str2arg(query)
	print(args)
	keys = DATA.allkeys(*args)
	return jsonfy(keys)
	
@app.route('/regions/<zoom>/<id>/<curzoom>')
def region_keys(zoom,id,curzoom):
	zoom = zoomer(zoom)
	if (zoom,id) in regions:
		regions.discard( (zoom,id) )
		region_data[zoom][id]['selected']='false'
	elif id in region_data[zoom]:
		regions.add( (zoom,id) )
		region_data[zoom][id]['selected']='true'
	
	return map_update(curzoom)

@app.route('/regions/<zoom>')
def map_update(zoom):
	curzoom = zoomer(zoom)
	obj = dict( (k,dict(v)) for k,v in region_data[curzoom].items() )
	for z,i in regions:
		if z != curzoom:
			obj[i] = dict(region_data[z][i])
			obj[i]['special'] = z
			if int(z) < int(curzoom):
				obj[i]['rad'] *= 3
			else:
				obj[i]['rad'] /= 3
	
	if STUDCOUNT:
		m = 0
		for k,v in obj.items():
			if 'brinnr' in v:
				v['rad'] = len( DATA(**{'tsector':list(tprofiel_keys), 'fsector':list(fprofiel_keys), 'year':years, 'brinnr':v['brinnr'] } ) )
			else:
				v['rad'] = len( DATA(**{'tsector':list(tprofiel_keys), 'fsector':list(fprofiel_keys), 'year':years, 'gemeente':v['name'] } ) )
			if m < v['rad']:
				m = v['rad']
		for k,v in obj.items():
			v['rad'] = int(v['rad'] / m * 10 + 0.5)
			
	linker(obj)
	
	if curzoom != zoom:
		for k,v in obj.items():
			v['rad'] *= 2
	
	return jsonfy(obj)

def linker(obj):
	for k,v in obj.items():
		if v['selected'] == 'true':
			if 'brinnr' in v:
				t1 = t2 = 'brinnr'
			else:
				t1,t2 = 'gemeente','name'
			v['to_link'] = []
			v['from_link'] = []
			for k2,v2 in obj.items():
				if 'brinnr' in v2:
					t3 = t4 = 'brinnr'
				else:
					t3,t4 = 'gemeente','name'
				from_q = {'tsector':list(tprofiel_keys), 'fsector':list(fprofiel_keys), 'year':years, ('f'+t1):v[t2], ('t'+t3):v2[t4] }
				to_q = {'tsector':list(tprofiel_keys), 'fsector':list(fprofiel_keys), 'year':years, ('t'+t1):v[t2], ('f'+t3):v2[t4] }
				from_n = len( DATA(**from_q) );
				to_n = len( DATA(**to_q) );
				if from_n > 0 and v2['selected'] == 'false':
					v['from_link'].append({'id':k2, 'n':from_n})
				if to_n > 0:
					if v2['selected'] == 'true':
						v['to_link'].append({'id':k2, 'n':to_n, 'col':'black'})
					else:
						v['to_link'].append({'id':k2, 'n':to_n})

def zoomer(zoom):
	if zoom == '9':
		return '8'
	if zoom == '11':
		return '10'
	if zoom == '13':
		return '12'
	return zoom
	
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
	
def jsonfy(dic):
	obj = json.dumps(dic)
	ans = obj.replace("}","}\r\n")
	return ans

def get(keys,args=[],kwargs={}):
	ans = []
	for (i1,k1),(i2,k2) in [(i,j) for i in enumerate(keys) for j in enumerate(keys)]:
		n = len(DATA(*args,ftype=k1,ttype=k2,**kwargs) )
		if n > 0:
			ans.append((i1,i2,n))
	return ans

list_reg=[]
list_inv=[]

def read_jona():
    with open('./python/investigeren.csv', 'rb') as invest:
        inv=csv.reader(invest, delimiter=';')
        for row in inv:
            list_inv.append(row)
    with open ('./python/regionale.csv', 'rb') as regionale:
        reg=csv.reader(regionale, delimiter=';')
        for row in reg:
            list_reg.append(row)

def cities(regions):
    province=None
    if regions == 'Netherlands':
        province = 'Nederland'

    for i in range(0,len(regions)-1):
        a = str(regions[i].decode('utf8')).lower()
        for j in range(0,len(list_reg)-1):
            b = str(list_reg[j][0]).lower()
            if a == b:
                province = str(list_reg[j][2])
                break
        if province:
            break
    
    if province is None:
        return None

    for i in range(0,len(list_inv)-1):
        if str(list_inv[i][0]) == province:
            return list_inv[i+2], list_inv[i+3], list_inv[i+4], list_inv[i+1]

@app.route('/sankey/update')
def sankey_update():
	colors = ['#500','#050','#005','#550','#055','#505','#555']
	types = list(DATA.allkeys('type') )
	tprofiles = list(tprofiel_keys)
	fprofiles = list(fprofiel_keys)
	links = [];
	if len(regions) < 1:
		links += [{"source":s,"target":t,"value":v, "color":"#000", "region":"Netherlands"} for s,t,v in get(types, \
						[],{'tsector':tprofiles, 'fsector':fprofiles, 'year':years})]
	else:
		for i,region in enumerate(regions):
			if 'brinnr' in region_data[region[0]][region[1]]:
				sname = region_data[region[0]][region[1]]['name']
				brinnr = region_data[region[0]][region[1]]['brinnr']
				print(sname,brinnr,len(DATA(brin_nr=brinnr)))
				links += [{"source":s,"target":t,"value":v, "color":colors[i%len(colors)], "region":sname} for s,t,v in get(types, \
								[],{'tsector':tprofiles,'fsector':fprofiles,'year':years,'brin_nr':brinnr})]
			else:
				reg = region_data[region[0]][region[1]]['name']
				links += [{"source":s,"target":t,"value":v, "color":colors[i%len(colors)], "region":reg} for s,t,v in get(types, \
								[],{'tsector':tprofiles, 'fsector':fprofiles, 'year':years, 'gemeente':reg})]
        obj = {"nodes": [{"name":i} for i in types], "links": links }
	print(links)
	return jsonfy(obj)

@app.route('/info/update')
def info_update():
	types = list(DATA.allkeys('type') )
	tprofiles = list(tprofiel_keys)
	fprofiles = list(fprofiel_keys)
	links = []
	if len(regions) < 1:
            links += [{"source":s,"inv":[], "target":t,"tsector":tprofiles,"value":v, "years": years,"region":"Netherlands"} for s,t,v in get(types, \
						[],{'tsector':tprofiles, 'fsector':fprofiles, 'year':years})]
	else:
		for i,region in enumerate(regions):
			if 'brinnr' in region_data[region[0]][region[1]]:
				sname = region_data[region[0]][region[1]]['name']
				brinnr = region_data[region[0]][region[1]]['brinnr']
				print(sname,brinnr,len(DATA(brin_nr=brinnr)))
				links += [{"source":s,"target":t,"years": years,"tsector":tprofiles,"value":v, "region":sname} for s,t,v in get(types, \
								[],{'tsector':tprofiles,'fsector':fprofiles,'year':years,'brin_nr':brinnr})]
			else:
				reg = region_data[region[0]][region[1]]['name']
                                links += [{"source":s,"inv":[],"target":t,"value":v, "years": years,"tsector":tprofiles,"region":reg} for s,t,v in get(types, \
								[],{'tsector':tprofiles, 'fsector':fprofiles, 'year':years, 'gemeente':reg})]
        for i in range(0,len(links)):
            inv=cities(links[i]['region'])
            links[i]['inv'] = inv
        obj = {"nodes": [{"name":i} for i in types], "links": links}
	print(obj)
	return jsonfy(obj)

@app.route('/')
def index():
	return open('./javascript/dashbord.htm','r').read()

#====== INIT	
def init():
	for r in RESOURCES:
		files = os.listdir(r)
		for file in files:
			fname = str(random.random())[2:].replace('-','')
			if file[-4:] == '.css':
				com = "@app.route('%s')\ndef %s():\n\tresp = Response( open('%s','r').read() )\n\tresp.headers['Content-Type'] = 'text/css; charset=UTF-8'\n\treturn resp"%(
					r[1:]+'/'+file,'f'+fname,r+'/'+file)
			else:
				com = "@app.route('%s')\ndef %s():\n\treturn open('%s','r').read()"%(
					r[1:]+'/'+file,'f'+fname,r+'/'+file)
			exec( com)

def region_init():
	global regions, region_data
	
	cities = json.load(open('./Geomap/zoom_cities.json','r'))
	clusters = json.load(open('./Geomap/zoom_cluster.json','r'))
	schools = json.load(open('./Geomap/zoom_schools.json','r'))
	province = json.load(open('./Geomap/zoom_province.json','r'))
	
	regions = set()
	region_data = {'7':province, '8':clusters, '9':clusters, '10':cities, '11':cities, '12':schools, '13':schools}

def main(size=0,studcount=False):
	init()
        read_jona()
	t1 = time()
	global DATA, tprofiel_keys, fprofiel_keys, years, regions, region_data, STUDCOUNT
	STUDCOUNT = studcount;
	DATA = build_database(size)
	t1 = time() - t1
	writenow('\n','loaded in',t1,'seconds. Total of',len(DATA),'students\n')
	
	tprofiel_keys = DATA.allkeys('sector')
	fprofiel_keys = DATA.allkeys('sector')
	years = ['2011','2012','2013','2014']
	
	region_init()
	#writenow(len(DATA(ftype='vwo')),'did vwo of which',len(DATA(ftype='vwo',ttype='wo')),'went to wo\n')
	#writenow('all keys of type are:',DATA(False,'type'))
	app.run()
	
if __name__ == '__main__':
	size,studcount = 0, False
	try: size = int(argv[1])
	except: pass
	try: studcount = (argv[2][0].lower() == 't')
	except: pass
	
	main(size,studcount)
