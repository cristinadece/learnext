'''
Created on Dec 20, 2012

@author: cris
'''

class VPoI(object):
    '''
    classdocs
    id is numeric
    '''


    def __init__(self, poi_id, num_photos, start, stop):
        '''
        Constructor
        '''
        self.id = poi_id
        self.num_photos = int(num_photos)
        self.start = long(start)
        self.stop = long(stop)

    def set_id(self, value):
        self.__id = value


    def get_id(self):
        return self.__id


    def get_num_photos(self):
        return self.__num_photos


    def get_start(self):
        return self.__start


    def get_stop(self):
        return self.__stop


    def set_num_photos(self, value):
        self.__num_photos = value


    def set_start(self, value):
        self.__start = value


    def set_stop(self, value):
        self.__stop = value

        
    def __str__(self):
        s = ""
        delim = "; "
        s += "Id: " + str(self.get_id()) + delim
        s += "Num photos: " + str(self.num_photos) + delim
        s += "Start: " + str(self.start) + delim
        s += "Stop: " + str(self.stop) + delim
        return s
    
    id = property(get_id, set_id, None, None)
    num_photos = property(get_num_photos, set_num_photos, None, None)
    start = property(get_start, set_start, None, None)
    stop = property(get_stop, set_stop, None, None)


        