'''
Created on Mar 3, 2015

@author: wli001
'''
import os
import re
import datetime

from collections import OrderedDict

from spec.sharp.CONST import CONST
from spec.sharp.config.model_config import *

class URLModelItem(object):        
    def __init__(self, t='', m='', p='', pl=[]):
        '''constructor'''
        self.timestamp  = t
        self.method     = m
        self.path       = p
        self.param_list = pl
       
    def __str__(self):
        return 'timestamp: ' + self.timestamp + '\tmethod:' + self.method + '\tpath: ' + self.path + '\tparams: ' + str(self.param_list)
        

class URLModeltemParser(object):    
    def do_naive_parse(self, log_item):
        print 'do naive parser.\n'
        '''16/Oct/2014:18:20:57''' 
        time    = log_item.split('[', 1)[1].split(']')[0]
        format_time = str(datetime.datetime.strptime(time, '%d/%b/%Y:%H:%M:%S'))
        print 'format-time: ' + format_time
        
        request = re.findall('"([^"]*)"', log_item)[0]
        mu  = request.split(' ')
        method  = mu[0]
        url     = mu[1]
        
        path, param_list    = self.parse_path_param_list(url)
        
        return URLModelItem(format_time, method, path, param_list)
    
    def do_formatter_parser(self, l, log_formatter, time_formatter):
        print '\n------\n do formatter parser....'        
#         print 'log formatter: ' + log_formatter
#         print 'time formatter: ' + time_formatter
        delimiter_list, format_string_pos = self.parse_log_format_string(log_formatter)
#         print 'delimiter_list: ' + str(delimiter_list)
#         print 'format string pos: ' + str(format_string_pos)        
        tokens  = self.tokenize_log_item(l, delimiter_list)                      
        time    = tokens[format_string_pos['t']]
        method  = tokens[format_string_pos['m']]
        url     = tokens[format_string_pos['u']]
        
        path, param_list    = self.parse_path_param_list(url)
        
        format_time = str(datetime.datetime.strptime(time, time_formatter))
#         format_time = str(datetime.datetime.strptime(time, '%d/%b/%Y:%H:%M:%S'))
#         print 'time: ' + time 
#         print 'format_time: ' + format_time
#         print 'method:' + method
#         print 'url:' + url
        
        return URLModelItem(format_time, method, path, param_list)
                
    def parse_log_format_string(self, format_string):        
        ''' log format string:
            %m        method
            %u        url, including query
            %t        time
            %-        placeholder
        '''
#         print 'parse format string;'
        string_format_list      = []
        content_list            = []
        delimiter_list          = []
        format_string_pos_dict  = {}
        
        flag = False
        for c in format_string:
            if not flag:
                if c == '%':
                    flag = True
                elif c != ' ':
                    delimiter_list.append(c)         
                    string_format_list.append(c)  
            elif flag:
                if c != '-':
                    format_string_pos_dict[c] = len(content_list)
                    
                content_list.append(c)                
                string_format_list.append(c)
                flag = False        
        
#         print string_format_list
#         print content_list
#         print delimiter_list
#         print format_string_pos_dict
        
        return delimiter_list, format_string_pos_dict   
    
    def tokenize_log_item(self, log_item, delimiter_list): 
#         delimiters = ' |\[|\"|\]'
        delimiters = ' '
        for d in delimiter_list:
            delimiters += '|\\' + d
#         print delimiters
        
        tokens = re.split(delimiters, log_item)
        non_space_tokens = []
        
        for t in tokens:
            if t :
                non_space_tokens.append(t)
        
        return non_space_tokens
        
    def parse_path_param_list(self, url):
        '''
        :param url: full url including path and query string
        '''
        if '?' not in url:
            return url, []
        
        pq      = url.split('?')
        path    = pq[0]
        query   = pq[1]
        
        if '=' not in query and '&' not in query:
            return url, [query]
        
        param_value_pairs   = query.split("&")         
        para_ordered_dict   = OrderedDict()
#             para_dict           = dict() 
        for p in param_value_pairs:
            if "=" not in p: continue
            param, value = p.split("=", 1)
            para_ordered_dict[param.strip()]=value.strip()            
#         print time + ': ' + method + ':\t' + path + '\t' 
#         print para_ordered_dict.keys()  
    
        param_list = para_ordered_dict.keys()
        
        return path, param_list
    
class URLModelTrainer(object):
    def __init__(self, model_config_file):
        mcb                 = ModelConfigBuilder()
        config_file         = CONST.CONFIG_DIR + 'test-model.xml'
        self.model_config   = mcb.build_config(config_file)  
        model_directory     = CONST.MODEL_DIR + self.model_config.model_name
        if os.path.isdir(model_directory):
            print 'model dir existed at: ' + model_directory
        else: 
            print 'create  dir: ' + model_directory
            os.makedirs(model_directory)
        '''model file name is the order of existing files in time series'''
        last_model_file_number          = len(os.listdir(model_directory))
        self.latest_model_file_name     = CONST.MODEL_DIR + str(last_model_file_number) + '.xml'
        self.model_file_name            = CONST.MODEL_DIR + str(last_model_file_number + 1) + '.xml'
        print 'last model file: ' + self.latest_model_file_name
        print 'model_file_name: ' + self.model_file_name

    def train_model(self):
        '''write the model'''
        with open(self.model_config.log_file) as f:
            log_entries = f.readlines()
        
        nts_detector    = NTSDetector()
        u_parser        = URLModeltemParser()
        for log_entry in log_entries:            
            model_item      = u_parser.do_formatter_parser(log_entry, self.model_config.log_formatter, self.model_config.time_formatter)
            print 'log-entry: ' + log_entry + '\n\t'
            print 'model_item:\t' + str(model_item)
            
            nts_detector.detect(model_item, log_entry)
#             todo: update model file w/ this model_item


class Detector(object):
    def alert_report(self, report):
        print 'ALERT: ' + report
        
class NTSDetector(Detector):
    '''non time series model'''
    def detect(self, model_item, log_item):
        print '****NTS dector***'
        self.method_alert(model_item, log_item)
        self.param_alert(model_item, log_item)
        
    def method_alert(self, model_item, log_item):
        '''check if insure method
        '''
        method = model_item.method.upper() 
        if method not in CONST.SECURE_HTTP_METHODS:
            self.alert_report('insecure http method: ' + method + ' in log item : ' + log_item)
    
    def param_alert(self, model_item, log_item):
        '''check params'''
        for p in model_item.param_list:
            if self.sensitive_param(p):
                self.alert_report('sensitive param name: ' + p + ' in log item : ' + log_item)
           
    def sensitive_param(self, param):
        return param.upper() in CONST.SENSITIVE_PARAM_NAMES
    
class TSDetector(Detector):
    '''time series model'''
    
    def unseen_path(self, url_item):
        ''' check a path '''
        
    def unsee_params(self, url_item):
        ''' check params '''

# uip  = URLModeltemParser()
# format_string = '%- %- %- [%t] "%m %u %-'
# log_item = '182.236.164.11 - - [16/Oct/2014:18:20:58] "post /oldlink?itemId=EST-18&pAssWord=SD6SL8FF10ADFF53101 HTTP 1.1" 408 893 "http://www.buttercupgames.com/product.screen?productId=SF-BVS-G01" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5" 134'
# uip.do_formatter_parser(log_item, format_string)


config_file = CONST.CONFIG_DIR + 'test-model.xml'
uat = URLModelTrainer(config_file)
uat.train_model()