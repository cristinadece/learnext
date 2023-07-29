'''
Created on Dec 20, 2012

@author: cris
'''

class User(object):
    '''
    classdocs
    '''


    def __init__(self, id):
        '''
        Constructor
        '''
        self.id = id
        self.sessions = []

    def set_id(self, value):
        self.__id = value


    def get_id(self):
        return self.__id


    def get_sessions(self):
        return self.__sessions


    def set_sessions(self, value):
        self.__sessions = value

        
    def __str__(self):
        s = ""
        s += "User id: " + str(self.get_id()) + "; "
        s += "Num sessions: " + str(len(self.sessions)) + ";"  
        s += "Sessions" + str(self.get_sessions()) + '\n'
        return s 
        
    id = property(get_id, set_id, None, None)
    sessions = property(get_sessions, set_sessions, None, None)

