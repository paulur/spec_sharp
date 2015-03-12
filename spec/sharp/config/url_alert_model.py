'''
Created on Mar 3, 2015

@author: wli001
'''
''''
URL Alert Model Format
<model>
    <request>
        <method></method>
        <path since=version> </path>
        <params since=version last-appearance-time= >
            param-name-1, …, param-name-n
        </params>
     </request>
</model>
'''

class URLAlertModel(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        