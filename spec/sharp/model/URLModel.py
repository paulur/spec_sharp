'''
Created on Jan 29, 2015

@author: paul
'''
from collections import OrderedDict

from spec.sharp.CONST import CONST

class AccessURLModel(object):
    '''
    classdocs
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        self.method, url    = request.split( )
        self.path, query    = url.split("?", 1)
        para_value_pairs    = query.split("&")
        
        self.para_dict   = OrderedDict()
        for p in para_value_pairs:
            para, value = p.split("=")
            self.para_dict[para.strip()]=value.strip()
            
    def to_string(self):
        print self.method
        print self.path
        print self.para_dict
        
    def get_para_names(self):
        return self.para_dict.keys()
           

log_file = CONST.WEBLOG_URLS
with open(log_file) as f:
    lines = f.readlines()
    
for l in lines:
    print '-----------------\n %s', l.rstrip('\n')
    aum = AccessURLModel(l)
    print aum.get_para_names()

