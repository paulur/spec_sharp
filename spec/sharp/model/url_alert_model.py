'''
Created on Mar 3, 2015

@author: wli001
'''
from spec.sharp.config import model_config

from spec.sharp.config.model_config import *

class URLAlertTrainer(object):
    '''
    classdocs
    '''

    def __init__(self, model_config_file):
        mcb =  ModelConfigBuilder()
        config_file = CONST.CONFIG_DIR + 'test-model.xml'
        self.model_config  = mcb.build_config(config_file)  
     
    
     TODO: lookup model loc and generate model file name   