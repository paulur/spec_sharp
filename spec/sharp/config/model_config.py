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

    def __init__(self, m_name='', m_loc='', m_desc='', l_type='', l_loc=''):
        '''
        Constructor
        '''
        self.model_name = m_name
        self.model_loc  = m_loc
        self.model_desc = m_desc
        self.log_type   = l_type
        self.log_loc    = l_loc
        
    def __str__(self):
        return 'model_name: ' + self.model_name + \
                '\nmodel_loc: ' + self.model_loc + \
                '\nmodel_desc: ' + self.model_desc + \
                '\nlog_type: ' + self.log_type + \
                '\nlog_loc: ' + self.log_loc
        
        
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
            elif tag == 'model-location':
                _m_loc = text
                '''replace $model_dir$ with real dir'''
                m_loc = _m_loc.replace('$model_dir$', CONST.MODEL_DIR)
            elif tag == 'model-description':
                m_desc = text
            elif tag == 'log-type':
                l_type = text
            elif tag == 'log-location':
                _l_loc = text
                '''replace $log_dir$ with real dir'''
                l_loc = _l_loc.replace('$log_dir$', CONST.LOG_DIR)
            else:
                '''done'''
        
        return ModelConfig(m_name, m_loc, m_desc, l_type, l_loc)
                

mcb =  ModelConfigBuilder()
config_file = CONST.CONFIG_DIR + 'test-model.xml'
mc  = mcb.build_config(config_file)      
print mc