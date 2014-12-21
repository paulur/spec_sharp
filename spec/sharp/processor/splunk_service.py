'''
Created on Dec 16, 2014

@author: paul
'''
import splunklib.client as client

from spec.sharp.config.config_builder import ConfigBuilder
from spec.sharp.CONST import CONST
from time import sleep
import splunklib.results as results

class SplunkService(object):
    '''
    classdocs
    '''
    '''
        config: the config file name
    '''
    def __init__(self, config):
        '''
        Constructor
        '''
        config = ConfigBuilder(config).build_keyword_search_config();
        self.service    = self.connect(config)
        
    def connect(self, config):
        # Create a Service instance and log in 
        service = client.connect(
            host        = config.host,
            port        = config.port,
            username    = config.user,
            password    = config.password)
        
#         Print installed apps to the console to verify login
#         for app in service.apps: 
#             print 'app:\t' + app.name
            
        return service
       
    def search(self, search_name='', search_string=''):
        #do search_example
        saved_search = self.service.saved_searches[search_name]
        print "search_example name: %s \nsearch string: %s\n----" % (saved_search.name, saved_search.content.search)
        job = saved_search.dispatch()
        
        while True:
            if job.is_ready():
                break
            sleep (2)
            
        for result in results.ResultsReader(job.results()):
            print result["_raw"]
    
# print 'splunk service search_example:\n'
service = SplunkService(CONST.KEYWORD_SERACH_CONFIG)
service.search("tmp")      