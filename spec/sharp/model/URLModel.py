'''
Created on Jan 29, 2015

@author: paul
'''

class URLModel(object):
    '''
    classdocs
    '''


    def __init__(self, path, paras):
        '''
        Constructor
        '''
        self.path = path
        self.parameters = paras
        
    def parse_query_paras(self, query):
        '''
        parse parameter name-value pairs from query string
        '''
        