'''
Created on Mar 3, 2015

@author: wli001
'''
import os

from spec.sharp.CONST import CONST
from spec.sharp.config.model_config import *

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
        model_file_number       = (1 + len(os.listdir(model_directory)))
        self.model_file_name    =  CONST.MODEL_DIR + str(model_file_number) + '.xml'

    def train_model(self):
        '''write the model'''
        
config_file = CONST.CONFIG_DIR + 'test-model.xml'
uat = URLAlertTrainer(config_file)
print 'model_file_name: ' + uat.model_file_name