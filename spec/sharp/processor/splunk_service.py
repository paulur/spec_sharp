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
        saved_searches = self.service.saved_searches
        try: 
            saved_search        = saved_searches[search_name]
            save_search_string  = saved_search.content.search
            if search_string != '' and search_string != save_search_string: 
                print "update the saved search %s with a new search string" % search_name
                kwargs = {"search" : search_string}
                saved_search.update(**kwargs).refresh()
            else:
                print "search with %s" % search_name
        except KeyError:
            print "no search with name %s is found." % search_name
            if search_string:
                saved_search = saved_searches.create(search_name, search_string)
            else:
                raise Exception("!!!search string is needed!!!")
                            
        print "line 59; search_example name: %s \tsearch string: %s\n----" % (saved_search.name, saved_search.content.search)
        job = saved_search.dispatch()
        
        while True:
            if job.is_ready():
                break
            sleep (2)
            
        for result in results.ResultsReader(job.results()):
            print result["_raw"]
        print "search done."
# print 'splunk service search_example:\n'
service = SplunkService(CONST.KEYWORD_SERACH_CONFIG)
service.search("tmpsd", "password | head 10")