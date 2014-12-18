'''
Created on Dec 16, 2014

@author: paul
'''
import xml.etree.ElementTree as ET   

import splunklib.client as client

class KeywordSearchConfig(object):
    '''
    classdocs
    '''
    def __init__(self, host='', port='', user='', password='', \
                 s_name='', s_keywords='', s_time='', \
                 s_stats='', s_limit=''):
        self.host       = host
        self.port       = port
        self.user       = user
        self.password   = password
        self.s_name     = s_name
        self.s_keywords = s_keywords
        self.s_time     = s_time
        self.s_stats    = s_stats
        self.s_limit    = s_limit 
        
    def __str__(self):
        return 'server: ' + self.host + ':' + self.port + ', user: ' + self.user + \
                '/' + self.password + \
                '\nsearch-name: ' + self.s_name + \
                '\nsearch-keywords: ' + self.s_keywords + \
                '\nsearch-time: ' + self.s_time + \
                '\nsearch-stats: ' + self.s_stats + \
                '\nsearch-limit: ' + self.s_limit             
        
        
class ConfigBuilder(object):
    '''
    builder config class from a config file
    '''
    config_file = '' 
    ''' = "/home/paul/workspace/spec_sharp/keyword-search-config.xml" '''

    def __init__(self, cf):
        '''
        Constructor
        '''
        self.config_file=cf
     
    def build_keyword_search_config(self):
        tree        = ET.parse(self.config_file)
        root        = tree.getroot()    
        config      = KeywordSearchConfig()
            
        for child in root:
            tag     = child.tag
            text    = child.text
            
            if tag == 'host':
                config.host = text
            elif tag == 'port':
                config.port  = text
            elif tag == 'user':
                config.user  = text
            elif tag == 'password':
                config.password  = text
            elif tag == 'search-name':
                config.s_name = text
            elif tag == 'search-keywords':
                config.s_keywords = text
            elif tag == 'search-time':
                config.s_time = text
            elif tag == 'search-stats':
                config.s_stats = text
            elif tag == 'search-limit':
                config.s_limit  = text
            else :
                '''do nothing'''                
            
        return config
    
    def main(self):
        print 'hi: config'
    
        '''testing code'''
        cb = ConfigBuilder("/home/paul/workspace/spec_sharp/keyword-search-config.xml")
        config = cb.build_keyword_search_config()
        print config.__str__()
        
        # Create a Service instance and log in 
        service = client.connect(
            host=config.host,
            port=config.port,
            username=config.user,
            password=config.password)
        
        # Print installed apps to the console to verify login
        for app in service.apps:
            print app.name 