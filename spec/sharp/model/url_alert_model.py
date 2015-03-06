'''
Created on Mar 3, 2015

@author: wli001
'''
import os
import re

from collections import OrderedDict

from spec.sharp.CONST import CONST
from spec.sharp.config.model_config import *

class URLModelItem(object):
    '''constructor
    :param t    timestamp of the log event
    :param m    http request method
    :param p    request path
    :param p_list    request parameter list in order
    '''
    def __init__(self, t, m, p, p_list):
        self.timestamp  = t
        self.method     = m
        self.path       = p
        self.param_list = p_list
    
    def __str__(self, ):
        return 'timestamp: ' + self.timestamp + '\tmethod:' + self.method + '\tpath: ' + self.path + '\tp_lsit: ' + str(self.param_list) 

class URLItemParser(object):
    
    def parseItem(self, l): 
        time    = l.split('[', 1)[1].split(']')[0]
        request = re.findall('"([^"]*)"', l)[0]
        mu  = request.split(' ')
        method  = mu[0]
        url     = mu[1]
        pq      = url.split('?')
        path    = pq[0]
        query   = pq[1]
        
        param_value_pairs    = query.split("&")
        
        para_ordered_dict   = OrderedDict()
#             para_dict           = dict() 
        for p in param_value_pairs:
            if "=" not in p: continue
#             print '\np:' + p
            param, value = p.split("=", 1)
            para_ordered_dict[param.strip()]=value.strip()
            
#         print time + ': ' + method + ':\t' + path + '\t' 
#         print para_ordered_dict.keys()  
        
        return URLModelItem(time, method, path, para_ordered_dict.keys())

class URLAlertTrainer(object):
    '''
    classdocs
    '''

    def __init__(self, model_config_file):
        mcb                 =  ModelConfigBuilder()
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
        print 'last modle file: ' + self.latest_model_file_name
        print 'model_file_name: ' + self.model_file_name

    def train_model(self):
        '''write the model'''
        with open(self.model_config.log_file) as f:
            lines = f.readlines()
        
        u_parser    = URLItemParser()
        detector    = URLAlertDetector()
        for l in lines:
#             print l + '\n\t'
            item = u_parser.parseItem(l)
#             print item
            detector.detect(item)
#             method_alert(item.method)
#             path_alert(item.path)
#             param_alert(item.params)

class URLAlertDetector(object):
    def detect(self, url_item):
        self.method_alert(url_item)
        self.param_alert(url_item)
        
    def method_alert(self, url_item):
        '''check if insure method
        '''
        method = url_item.method.upper() 
        if method not in CONST.SECURE_HTTP_METHODS:
            self.alert_report('insecure http method: ' + method + ' in request: ' + str(url_item))
    
    def param_alert(self, url_item):
        '''check params'''
        for p in url_item.param_list:
            if self.sensitive_param(p):
                self.alert_report('sensitive param name: ' + p + ' in request: ' + str(url_item))
                
        
    def path_alert(self, path):
        '''check if unseen path'''
        
    def sensitive_param(self, param):
        return param.upper() in CONST.SENSITIVE_PARAM_NAMES
    
    def alert_report(self, alert):
        print '!alert!: ' + alert
        
config_file = CONST.CONFIG_DIR + 'test-model.xml'
uat = URLAlertTrainer(config_file)
uat.train_model()