'''
Created on Dec 16, 2014

@author: paul
'''
import re
from time import sleep

import splunklib.client as client
import splunklib.results as results

from spec.sharp.config.splunk_config import ConfigBuilder
from spec.sharp.CONST import CONST


class SplunkService(object):
    '''
    classdocs
    '''
    urls = []
    log_entries = []
    
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
#         for app in self.service.apps: 
#             print 'app:\t' + app.name
    def search_by_name(self, func, search_name):
        saved_searches = self.service.saved_searches
        saved_search   = saved_searches[search_name]
        job = saved_search.dispatch()
         
        while True:
            if job.is_ready():
                break
            sleep (2)
             
        func(job)
        print "search done"
        
    def search_by_config(self, process_result=''):
        self.search(self.config.s_name, self.config.construct_search_string(), process_result)   
                
    def search(self, search_name, search_string, process_result):
        ''' process_result: the callback function to process the search result'''
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
        
        print "search name: %s.\tsearch string: %s\n----" % (saved_search.name, saved_search.content.search)
        
        job = saved_search.dispatch()
        
        while True:
            if job.is_ready():
                break
            sleep (2)
            
        for result in results.ResultsReader(job.results(count=0)):
            if isinstance(result, dict):
#                 print "Results raw: %s" % result['_raw']
#                 if __debug__: 
#                     print '.'
                if (process_result):
#                     print "do-traverse-func:"
                    process_result(result)
            elif isinstance(result, results.Message):
                print "Not Traverse Message: %s" % result
        print "search done"
           
#         self.display_result(job)
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
#                 print "Results: %s" % result
                print "Results raw: %s" % result['_raw']
            elif isinstance(result, results.Message):
                print "Message: %s" % result           
                       
    
    
    def create_urls_entries_files(self):
        self.urls    = []
        self.log_entries = []
        self.search_by_config(self.process_web_log_entry)
        f_urls  = open(CONST.WEBLOG_URLS, "w")
        for u in service.urls: 
#             print u
            f_urls.write("%s\n" % u)
        self.urls    = []
        f_urls.close()
         
        f_log_entries = open(CONST.WEBLOG_ENTRIES, "w")
        for e in service.log_entries:
            f_log_entries.write("%s\n" % e)
        self.log_entries = []   
        f_log_entries.close()

    def process_web_log_entry(self, result):
        log_entry = result['_raw']
        self.log_entries.append(log_entry)
        
        url = re.findall('"([^"]*)"', log_entry)[0]
        if ' ' in url: 
            self.urls.append(url.split(' ')[0] + ' ' + url.split(' ')[1])
        else:
            print 'irregular url: ' + url
         
service = SplunkService(CONST.KEYWORD_SERACH_CONFIG)
service.create_urls_entries_files()
#testing remove
# service.search_by_config()
# service.display_result(search_job)
# service.delete_search("tmp")
# service.list_saved_search()