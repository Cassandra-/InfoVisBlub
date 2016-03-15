from sys import stdout
import json
from tinydb import TinyDB, Query

def writenow(*args):
    stdout.write("\r%s          " % ' '.join([str(a) for a in args])); stdout.flush()
def nl():
    stdout.write("\n")
def cl():
	stdout.write("\r"); stdout.flush()

def read(filename):
	global db, id
	f = open(filename,'r')

	cur_year = filename[-8:-4].lower().strip()
	
	f.readline()
	labels = [label.strip().lower() for label in f.readline().split(';')[:-1]]
	ftype = []
	ttype = []
	if 'Doorstroom HAVO-VWO to HBO-WO' in filename:
		splitter = 7
		from_labels = ['brin_nr','vest_nr','gem nr','gemeente','type','diploma','sector']
		to_labels = ['brin_nr','type','sector','gem_nr','gemeente']
	elif 'Doorstroom HAVO-VWO to MBO' in filename:
		splitter = 7
		from_labels = ['brin_nr','vest_nr','gem_nr','gemeente','type','diploma','sector']
		to_labels = ['brin_nr','leerweg','sector','kwalificatie','kwalif_code','brin_nr_kc','kenniscentrum','gem_nr','gemeente']+['type']
		ttype = ['mbo']
	elif 'Doorstroom VMBO to MBO' in filename:
		splitter = 7
		ftype,ttype = ['vmbo'],['mbo']
		from_labels = ['brin_nr','vest_nr','gem_nr','gemeente','leerweg','sector','afdeling']+['type']
		to_labels = ['brin_nr','sector','kwalificatie','kwalif_code','brin_nr_kc','kenniscentrum']+['type']
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
			fdict = dict(_from)
			tdict = dict(_to)
			fdict2 = dict( [('f'+k,v) for k,v in _from] )
			tdict2 = dict( [('f'+k,v) for k,v in _to] )
			
			fdict.update(tdict)
			fdict.update(fdict2)
			fdict.update(tdict2)
			fdict.update({'year':cur_year, '_id':id})
			id += 1
			db[str(id)] = fdict
	cl()


def main():
	global db, id
	id = 0
	#jsonDump = []
	db = {}#TinyDB('test.json')
	read('../Doorstroom HAVO-VWO to HBO-WO/03 Doorstroom havo-vwo naar ho in 2011.csv')
	if True:
		read('../Doorstroom HAVO-VWO to MBO/02 Doorstroom havo-vwo naar mbo in 2011.csv')
		read('../Doorstroom MBO to HBO/04. Doorstroom mbo naar ho in 2011.csv')
		read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2011.csv')
		read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2012.csv')
		read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2013.csv')
		read('../Doorstroom HAVO-VWO to HBO-WO/03. Doorstroom havo-vwo naar ho in 2014.csv')
		read('../Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2012.csv')
		read('../Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2013.csv')
		read('../Doorstroom HAVO-VWO to MBO/02. Doorstroom havo-vwo naar mbo in 2014.csv')
		read('../Doorstroom MBO to HBO/04 Doorstroom van mbo naar hbo in 2012.csv')
		read('../Doorstroom MBO to HBO/04. Doorstroom mbo naar hbo in 2013.csv')
		read('../Doorstroom MBO to HBO/04. Doorstroom mbo naar hbo in 2014.csv')
		read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2012.csv')
		read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2013.csv')
		read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2014.csv')
		read('../Doorstroom VMBO to MBO/01. Doorstroom vmbo naar mbo in 2014.csv')
		read('../Doorstroom PO to VO/05. Doorstroom po naar vo in 2012.csv')
		read('../Doorstroom PO to VO/05. Doorstroom po naar vo in 2013.csv')
		read('../Doorstroom PO to VO/05. Doorstroom po naar vo in 2014.csv')
	print( len(db) )
	f = open('tinyDBdata.json','w')
	f.write(json.dumps( {'_default':db} ) )

if __name__ == '__main__':
	main()