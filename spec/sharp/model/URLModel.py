'''
Created on Jan 2, 2015

@author: paul
'''
from zeitgeist.datamodel import parents

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
        
class URLLayeredGraph(object):
    def __init__(self, method):
        self.root = LayerdGraphNode(method, 0)
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

        