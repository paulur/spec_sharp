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
        self.config     = ConfigBuilder(config).build_keyword_search_config();
        self.service    =  client.connect(
                            host        = self.config.host,
                            port        = self.config.port,
                            username    = self.config.user,
                            password    = self.config.password)

#         Print installed apps to the console to verify login
#         for app in service.apps: 
#             print 'app:\t' + app.name
        
    def search_by_config(self):
        self.search(self.config.s_name, self.config.construct_search_string())   
    
    def search_by_name(self, search_name):
        saved_searches = self.service.saved_searches
        saved_search   = saved_searches[search_name]
        job = saved_search.dispatch()
        
        while True:
            if job.is_ready():
                break
            sleep (2)
            
        self.display_result(job)
            
    def search(self, search_name, search_string):
        saved_searches = self.service.saved_searches
        try: 
            saved_search        = saved_searches[search_name]
            save_search_string  = saved_search.content.search
            if search_string and search_string != save_search_string: 
                print "update the saved search '%s' with a new search string" % search_name
                kwargs = {"search" : search_string}
                saved_search.update(**kwargs).refresh()
            else:
                print "search with existing search: '%s'" % search_name
        except KeyError:
            print "no search with name '%s' is found." % search_name
            saved_search = saved_searches.create(search_name, search_string)
                            
        print "line 59; search name: %s.\tsearch string: %s\n----" % (saved_search.name, saved_search.content.search)
        job = saved_search.dispatch()
        
        while True:
            if job.is_ready():
                break
            sleep (2)
           
        self.display_result(job)
#         
#         for result in results.ResultsReader(job.results()):
#             if isinstance(result, dict):
#                 print "Result: %s" % result['_raw']
#             elif isinstance(result, results.Message):
#                 # Diagnostic messages may be returned in the results
#                 print "Message: %s" % result
#                 print "search done."

    def list_saved_search(self):
        saved_searches = self.service.saved_searches
        for saved_search in saved_searches:
            header = saved_search.name
#             print header
#             print '='*len(header)
#             content = saved_search.content
#             for key in sorted(content.keys()):
#                 value = content[key]
#                 print "%s: %s" % (key, value)
#             history = saved_search.history()
#             if len(history) > 0:
#                 print "history:"    
#                 for job in history:
#                     print "    %s" % job.name
            print "%s: %s" % (header, saved_search.content.search) 
            
    def delete_search(self, s_name):
        self.service.saved_searches.delete(s_name)
    
    def display_result(self, job):
        for result in results.ResultsReader(job.results()):
            if isinstance(result, dict):
                print "Results raw: %s" % result['_raw']
            elif isinstance(result, results.Message):
                print "Message: %s" % result
        
service = SplunkService(CONST.KEYWORD_SERACH_CONFIG)
# service.search_by_name("OSSEC - Top Reporting Hosts")
# service.search("tmp", "password")
service.search_by_config()
# service.display_result(search_job)
# service.delete_search("tmp")
# service.list_saved_search()