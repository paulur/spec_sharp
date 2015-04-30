'''
Created on Mar 3, 2015

@author: wli001
'''
import os
import re
import datetime
from xml.etree.ElementTree import *
from xml.etree import ElementTree
from xml.dom import minidom

from collections import OrderedDict

from spec.sharp.CONST import CONST
from spec.sharp.config.model_config import *

class URLModelItem(object):        
    def __init__(self, t='', m='', p='', pl=[]):
        '''constructor
            timestamp
            method
            path
            parameter list
        '''
        self.timestamp  = t
        self.method     = m
        self.path       = p
        if not len(pl) :                    
            pl.append(CONST.SPEC_SHARP_NULL) 
            
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
    
    def format_parse(self, log_item, log_formatter, time_formatter):
        '''
        parse a log entry into a model item for contsturing the model
        '''
        print '\n------\n do formatter parser....'        
#         print 'log formatter: ' + log_formatter
#         print 'time formatter: ' + time_formatter
        delimiter_list, format_string_pos = self.do_format_parse(log_formatter)
#         print 'delimiter_list: ' + str(delimiter_list)
#         print 'format string pos: ' + str(format_string_pos)        
        tokens  = self.tokenize_log_item(log_item, delimiter_list)                      
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
                
    def do_format_parse(self, format_string):        
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
        config_file         = model_config_file #CONST.CONFIG_DIR + 'test-model.xml'
        self.model_config   = mcb.build_config(config_file)  
        model_directory     = CONST.MODEL_DIR + self.model_config.model_name
        if not os.path.isdir(model_directory):            
            self.init_model_repos(model_directory)   
            
    def init_model_repos(self, model_directory):
        print 'initial model dir: ' + model_directory
        os.makedirs(model_directory)    
        
        root  = ET.Element('model')
        root.set('ini_ts', str(datetime.datetime.utcnow()))
        comment_node = Comment('initial model. no data.')
        root.append(comment_node)
        self.prettify_to_file(root, model_directory + '\\0.xml')
                
    def prettify_to_string(self, root):
        """Return a pretty-printed XML string for the Element.
        """
        xml_string = ElementTree.tostring(root, 'utf-8')
        return xml_string
#         reparsed = minidom.parseString(xml_string)
#         return reparsed.toprettyxml(indent='\t')
        
    def prettify_to_file(self, elem, file): 
        with open (file, 'w') as mf :
            mf.write(self.prettify_to_string(elem))
            mf.close()
        
    def train_model(self):
        '''write the model'''
        with open(self.model_config.log_file) as f:
            log_entries = f.readlines()
                       
        '''model file name is the order of existing files in time series'''
        model_directory         = CONST.MODEL_DIR + self.model_config.model_name    
        last_model_file_number  = len(os.listdir(model_directory))
        latest_model_file_name  = model_directory + '\\' + str(last_model_file_number-1) + '.xml'
        current_model_file_name = model_directory + '\\' + str(last_model_file_number) + '.xml'
        reprot_file_name        = CONST.REPORT_DIR + self.model_config.model_name + '-rpt.xml'
        
#         print 'last model file: ' + latest_model_file_name
#         print 'current current_model_file_name: ' + current_model_file_name
                
        last_model_root     = ET.parse(latest_model_file_name).getroot()        
        current_model_root  = ET.parse(latest_model_file_name).getroot()
        report_root         = Element('report')
        report_root.set('report_ts', str(datetime.datetime.utcnow()))
        report_root.set('model-name', self.model_config.model_name )
        
        nts_detector    = NTSDetector()
        ts_detector     = TSDetector()
    
        u_parser        = URLModeltemParser()  
        for log_entry in log_entries:            
            model_item      = u_parser.format_parse(log_entry, self.model_config.log_formatter, self.model_config.time_formatter)
            print 'log-entry: ' + log_entry + '\n\t'
            print 'model_item:\t' + str(model_item)
            
            #detector also update the model 
#             nts_detector.detect(model_item, log_entry)
            ts_detector.detect(model_item, current_model_root, log_entry, report_root)
        
        pretty_last_model       = self.prettify_to_string(last_model_root)
        pretty_current_mdoel    = self.prettify_to_string(current_model_root)
        
        print 'current mode xml: ', pretty_current_mdoel
       
        
        if pretty_current_mdoel != pretty_last_model:
#             print 'pretty_last_model: ' + pretty_last_model
#             print 'pretty_current_mdoel: ' + pretty_current_mdoel
            self.prettify_to_file(current_model_root, current_model_file_name)
            self.prettify_to_file(report_root, reprot_file_name)
            print 'model is updated.'
        else: 
            '''no change of the model'''
            print 'no update to the model.'
        
        

#     def update_model(self, model_item, last_model_root, current_model_root):
#         print 'udpate mdoe: last model root: \n' + tostring(last_model_root)
#         '''update the model'''    


class Detector(object):
    def alert_report(self, report):
        print 'ALERT: ' + report
        
    def report_alert(self, report_root, alert_type, alert_detail, orignal_request):
        alert_node  = SubElement(report_root, 'alert', {'type': alert_type})
        detail_node         = SubElement(alert_node, 'detail')
        detail_node.text    = alert_detail
        request_node        = SubElement(alert_node, 'original-request')
        request_node.text   = orignal_request.__str__()
        
class NTSDetector(Detector):
    '''non time series model'''
    def detect(self, model_item, log_entry):
        print '****NTS dector***'
        insecure_method = self.insecure_method_alert(model_item) 
        if (insecure_method) :             
            self.alert_report('insecure_method in log entry: ' + log_entry + '\n[' + insecure_method  + ']')
            
        sensitive_params = self.sensitive_param_alert(model_item)
        if len(sensitive_params) :
            self.alert_report('sensitive param names in log entry: ' + log_entry + '\n' + str(sensitive_params))
        
    def insecure_method_alert(self, model_item):
        '''check if insure method'''
        method = model_item.method.upper() 
        if method not in CONST.SECURE_HTTP_METHODS:
            return method
    
    def sensitive_param_alert(self, model_item):
        '''check params'''
        sensitive_params = []
        for p in model_item.param_list:
            if p.upper() in CONST.SENSITIVE_PARAM_NAMES:
                sensitive_params.append(p)
                
        return sensitive_params
           
    
class TSDetector(Detector):
    '''time series model'''
    def detect(self, model_item, model_root, log_entry, report_root):
        '''
        model_item: parse model item from log entry
        current_model_root: ElementTree_root        the xml root of the model to build
        log_entry: the orignal log entry
        '''
        print '***TS detector***'
        print 'ts detector for item :' + model_item.__str__()
        
        is_request_existed = 0                
        for r_node in model_root.iter('request'):
            node_method  = r_node.get('method')
            node_path    = r_node.get('path')
            print 'in the model: method ', node_method, ' path ', node_path
            print 'in the new item to check: method ', model_item.method, ' path ', model_item.path
            
            item_method     = model_item.method
            item_path       = model_item.path
            item_param_list = self.list_string(model_item.param_list)
            
            if node_method == item_method and node_path == item_path:
                is_request_existed = 1
                print 'no need add new request_node'    
                
                if  not item_param_list:
                    break 
                '''consider add empty param placeholder, if needed'''
                    
                is_param_list_existed = 0               
                      
                for p_node in r_node.iter('param-list'):
                    model_p_list = p_node.text
                    if item_param_list == model_p_list:
                        print 'p_list in the model: ', model_p_list
                        is_param_list_existed = 1          
                
                if not is_param_list_existed:
#                     self.alert_report('Detected: a new param-lsit: ' + model_item.__str__())
                    self.report_alert(report_root, CONST.ALERT_UNSEEN_PARAMS, 'param-list not seen', log_entry.__str__())
                    param_list      = SubElement(r_node, 'param-list')
                    param_list.text = item_param_list
                
        if not is_request_existed:    
            print 'Detected: a new request: ', model_item.__str__()
            self.report_alert(report_root, CONST.ALERT_UNSEEN_PATH, 'request path not seen', log_entry.__str__())
            self.add_request_node(model_root, model_item)
                    
    def list_string(self, list):
#             list_str = ''
#             for l in list:
#                 list_str +=l.strip()
#                 list_str +=','
#             
#             return list_str[:-1]
        return ','.join(list) 
    
    def add_request_node(self, parent, model_item):
            request = SubElement(parent, 'request', {'path': model_item.path, 'method': model_item.method})
            if model_item.param_list:
                param_list  = SubElement(request, 'param-list')
                param_list.text = self.list_string(model_item.param_list)
                print 'add request node with param-list:', param_list.text
            
    def unseen_path(self, url_item, current_model_root, log_entry):
#         TODO
        ''' check a path '''
        '''if new url: add the url to the new model''' 
        
    def unsee_params(self, url_item, current_model_root, log_entry):
#         TODO
        '''check params'''
        ''' if a new params: add the params to the path of existing path'''

# uip  = URLModeltemParser()
# format_string = '%- %- %- [%t] "%m %u %-'
# log_item = '182.236.164.11 - - [16/Oct/2014:18:20:58] "post /oldlink?itemId=EST-18&pAssWord=SD6SL8FF10ADFF53101 HTTP 1.1" 408 893 "http://www.buttercupgames.com/product.screen?productId=SF-BVS-G01" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5" 134'
# uip.format_parse(log_item, format_string)


config_file = CONST.CONFIG_DIR + 'test-model.xml'
uat = URLModelTrainer(config_file)
uat.train_model()