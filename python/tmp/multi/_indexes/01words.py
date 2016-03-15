# words
# TreeMultiTest

# inserted automatically
import os
import marshal

import struct
import shutil

from hashlib import md5

# custom db code start
# db_custom


# custom index code start
# ind_custom
from CodernityDB.tree_index import MultiTreeBasedIndex
from itertools import izip

# source of classes in index.classes_code
# classes_code


# index code start

class TreeMultiTest(MultiTreeBasedIndex):

    custom_header = """from CodernityDB.tree_index import MultiTreeBasedIndex
from itertools import izip"""

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '16s'
        super(TreeMultiTest, self).__init__(*args, **kwargs)
        self.__l = kwargs.get('w_len', 2)

    def make_key_value(self, data):
        name = data['w']
        l = self.__l
        max_l = len(name)
        out = set()
        for x in xrange(l - 1, max_l):
            m = (name, )
            for y in xrange(0, x):
                m += (name[y + 1:],)
            out.update(set(''.join(x).rjust(16, '_').lower() for x in izip(*m)))  #ignore import error
        return out, dict(w=name)

    def make_key(self, key):
        return key.rjust(16, '_').lower()
