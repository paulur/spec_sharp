'''
Created on Dec 17, 2014

@author: paul
'''

class CONST(object):
    '''
    constants used in this application
    '''
    ROOT_DIR                = "C:\\Users\\wli001\\git\\spec_sharp\\file\\"
    MODEL_DIR               = ROOT_DIR + "model\\"
    LOG_DIR                 = ROOT_DIR + "log\\"
    CONFIG_DIR              = ROOT_DIR + "config\\"
    REPORT_DIR              = ROOT_DIR + "report\\"
    KEYWORD_SERACH_CONFIG   = LOG_DIR + "keyword-search-conf.xml"
    WEBLOG_ENTRIES          = MODEL_DIR + "weblog-entries.txt"
    WEBLOG_URLS             = ROOT_DIR + "weblog-urls.txt"


    SECURE_HTTP_METHODS     = ['GET', 'POST', 'DELETE', 'POST', 'HEAD']
    SENSITIVE_PARAM_NAMES   = ['PASSWORD', 'LASTNAME', 'PHONE', 'ADDRESS']
    
    SPEC_SHARP_NULL         = 'spec-sharp-null'
    
    ALERT_UNSEEN_PARAMS     = 'not seen params'
    ALERT_UNSEEN_PATH       = 'not seen request path'     