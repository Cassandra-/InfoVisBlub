from distutils.core import setup
from Cython.Build import cythonize
#import os

#os.environ['CC'] = "C:\\MinGW\\bin"

setup(
    ext_modules = cythonize("student.pyx"
			,include_path = ['C:\\MinGW\\x86_64-w64-mingw32\\include']#, 'C:\\Anaconda3\\include']
			#,libraries = ['python3.dll']
			#,library_dirs = ['C:\\Anaconda3\\']
		)
)

#gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o yourmod.so yourmod.c