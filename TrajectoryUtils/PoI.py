'''
Created on Dec 19, 2012

@author: cris
'''

class PoI(object):
    '''
    classdocs
    this class models PoIs
    Id is numeric
    '''
    def __init__(self, id, city, title, geo, categ):
        '''
        Constructor
        '''
        
        self.id = id
        self.city = city
        self.title = title
        self.geo = geo
        self.categ = categ
        
        #wiki
        self.wiki_clicks = 0 
        self.page_it = False
        self.page_en = False

    def get_categ(self):
        return self.__categ


    def set_categ(self, value):
        self.__categ = value


    def set_id(self, value):
        self.__id = value


    def get_id(self):
        return self.__id


    def get_title(self):
        return self.__title


    def get_geo(self):
        return self.__geo


    def get_wiki_clicks(self):
        return self.__wiki_clicks


    def get_page_it(self):
        return self.__page_it


    def get_page_en(self):
        return self.__page_en


    def set_title(self, value):
        self.__title = value


    def set_geo(self, value):
        self.__geo = value


    def set_wiki_clicks(self, value):
        self.__wiki_clicks = value


    def set_page_it(self, value):
        self.__page_it = value


    def set_page_en(self, value):
        self.__page_en = value

        
          
        
    def __str__(self):
        s = ''
        delim = ';    '
        s += 'Id: ' + str(self.id) + delim
        s += 'Title: '+ self.title + delim
        s += 'Geo' + str(self.geo) + delim
        s += 'Categories: ' + str(self.categ) + delim
        #s += 'Number photos: ' + str(self.num_photo) + delim
        #s += 'Spatial density: ' + str(self.spatial_density) + delim + '\n'
        return s
    
    
    id = property(get_id, set_id, None, None)
    title = property(get_title, set_title, None, None)
    geo = property(get_geo, set_geo, None, None)
    wiki_clicks = property(get_wiki_clicks, set_wiki_clicks, None, None)
    page_it = property(get_page_it, set_page_it, None, None)
    page_en = property(get_page_en, set_page_en, None, None)
    categ = property(get_categ, set_categ, None, None)


        