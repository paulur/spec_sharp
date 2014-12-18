'''
Created on Dec 16, 2014

@author: paul
'''
import splunklib.client as client

from spec.sharp.config.config_builder import ConfigBuilder


class LogSearch(object):
    '''
    classdocs
    '''
    def __init__(self, config):
        '''
        Constructor
        '''
        self.config = ConfigBuilder(config).build_keyword_search_config();
        
    def search(self):
        # Create a Service instance and log in 
        service = client.connect(
            host    =self.config.host,
            port    =self.config.port,
            username=self.config.user,
            password=self.config.password)
        
        # Print installed apps to the console to verify login
        for app in service.apps: 
            print 'app:\t' + app.name
            
log_search = LogSearch("/home/paul/workspace/spec_sharp/keyword-search-config.xml")  
log_search.search()      