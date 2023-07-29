'''
Created on Dec 19, 2012

@author: cris
'''

class Session(object):
    '''
    classdocs
    '''


    def __init__(self, id):
        '''
        Constructor
        '''
        self.id = id
        self.pois = []  # pois is a list of PoI objects

    def get_id(self):
        return self.__id


    def get_pois(self):
        return self.__pois


    def set_id(self, value):
        self.__id = value


    def set_pois(self, value):
        self.__pois = value


    
                
    def __str__(self):
        s = "----------"
        delim = ";    "
        s += "Id: " +  str(self.get_id()) + delim
        s += "length: " + str(len(self.pois)) + delim
        s += "PoIs" + str(self.get_pois()) + delim
        return s
    
    id = property(get_id, set_id, None, None)
    pois = property(get_pois, set_pois, None, None)
    
    

   