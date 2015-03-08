'''
Created on Mar 3, 2015

@author: wli001
'''

import xml.etree.ElementTree as ET   

from spec.sharp.CONST import CONST 


'''
Model Config Format
<conf>
    <model-name>  (unique)
    <model-location> 
    <model-description>
    <log-type>
    <log-location>   
</conf>
'''


class ModelConfig(object):
    '''
    classdocs
    '''

    def __init__(self, m_name='', m_desc='', l_type='', l_file='', l_formatter='', t_formatter=''):
        '''
        Constructor
        '''
        self.model_name     = m_name
        self.model_desc     = m_desc
        self.log_type       = l_type
        self.log_file       = l_file
        self.log_formatter  = l_formatter
        self.time_formatter = t_formatter
        
    def __str__(self):
        return 'model_name: ' + self.model_name + \
                '\nmodel_desc: ' + self.model_desc + \
                '\nlog_type: ' + self.log_type + \
                '\nlog_file: ' + self.log_file + \
                '\nlog_formatter: ' + self.log_formatter + \
                '\ntime_formatter: ' + self.time_formatter
        
        
class ModelConfigBuilder(object):
    '''
        constructor
    '''
    def build_config(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()
        
        for child in root:
            tag     = child.tag
            text    = child.text
            
            if tag == 'model-name':
                m_name = text
            elif tag == 'model-description':
                m_desc = text
            elif tag == 'log-type':
                l_type = text
            elif tag == 'log-file':
                _l_loc = text
                l_loc = CONST.LOG_DIR + _l_loc
            elif tag == 'log-formatter':
                l_formatter = text
            elif tag == 'time-formatter':
                t_formatter = text
            else:
                '''done'''
        
        return ModelConfig(m_name, m_desc, l_type, l_loc, l_formatter, t_formatter)
                

mcb =  ModelConfigBuilder()
config_file = CONST.CONFIG_DIR + 'test-model.xml'
mc  = mcb.build_config(config_file)      
print mc