'''
Created on Jan 2, 2015

@author: paul
'''
from httplib import REQUEST_ENTITY_TOO_LARGE

class URLParser(object):
    request_url_tokens = []
    
    def __init__(self, request_url_string):
        self.request_url_tokens = self.parse_url(request_url_string)
        
    def parse_url(self, request_url_string):
        '''
        tokenize a url string into tokens
        :request_url_string: request method with uri. for example, "GET /oldlink?itemId=EST-14&JSESSIONID=SD6SL7FF7ADFF53113"
        '''

class LayerdGraphNode(object):
    '''
    A URL model is a layer directed graph (i.e.,acyclic directed graph).
    The source (i.e., root) node is the method.
    '''


    def __init__(self, label, layer_id, count=0, parents=[], children=[]):
        '''
        Constructor
        '''
        self.label      = label
        self.layer_id   = layer_id
        self.count      = count
        self.parents    = parents
        self.children   = children

class LayeredGraphRoot(object):
        def __init__(self, children=[]):
            '''
            Constructor
            '''
            self.label      = 'root'
            self.layer_id   = 0
            self.count      = 1
            self.parents    = None
            self.children   = children
    
class LayeredGraphHead(object):
        def __init__(self, label, layer_id, count, root, children=[]):
            '''
            Constructor
            '''
            self.label      = 'root'
            self.layer_id   = 1
            self.count      = 0
            self.parents    = root
            self.children   = children
        
class URLLayeredGraph(object):
    root = LayeredGraphRoot()
    
    def __init__(self):
        self.current_layer  = 0
        self.current_list = [self.root]
        self.graph = [self.current_list]
        
    def add_node(self, lg_node):
        lg_node = None
    

    def add_path(self, url):
        '''
        add a url to the graph model
        :param: url a list of node
        '''
        ulr = None

        