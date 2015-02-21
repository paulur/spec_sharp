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
        if "?" not in url:
            self.path = url
            self.query = ''            
        else:
            self.path, self.query = url.split("?", 1)
        
            
        param_value_pairs    = self.query.split("&")
        
        self.para_dict   = dict() #OrderedDict()
        for p in param_value_pairs:
            if "=" not in p: continue
#             print '\np:' + p
            param, value = p.split("=", 1)
            self.para_dict[param.strip()]=value.strip()
            
    def to_string(self):
        print self.method
        print self.path
        print self.para_dict
        
    def get_param_names(self):
        return self.para_dict.keys()
           
class URLProcessor(object):    
    def get_access_url_params(self, access_log): 
        with open(access_log) as f:
            lines = f.readlines()
        
        log_params_file = access_log + ".params"
        f_params  = open(log_params_file, "w")    
        params_index = dict()
        try: 
            for l in lines:         
                aum = AccessURLModel(l)
                f_params.write('\n' + aum.method + '\t' + aum.path + ': ')
                for pn in aum.get_param_names():
                    f_params.write(pn + ', ')
                    params_index[pn]=''
        finally:
            f_params.close()
        print 'params-written to: ' + log_params_file

        f_params_index = open( log_params_file + '.index', "w")
        for i in params_index:
            f_params_index.write(i + '\n')
        
        f_params_index.close   
        
up = URLProcessor()
access_log = CONST.WEBLOG_URLS
up.get_access_url_params(access_log)