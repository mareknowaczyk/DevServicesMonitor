# -*- coding: utf-8 -*-

import re, os

from kinds_parser import (
  ParserRes,
  ParserModule,        
)

class PyramidServerParserRes(ParserRes):

    """wynik parsowania klasy PyramidServerParser"""

    def __init__(self, kind, app_name, app_dir, process_id):    
        ParserRes.__init__(self, kind, **{ 
            'app_name' : app_name,
            'app_dir' : app_dir,
            'process_id' : process_id
            } ) 

        

class PyramidServerParser(ParserModule):

    """PyramidServerParser
    
    Klasa parsująca stringa w poszukiwaniu procesu servera frameworka Pyramid.
    Jeśli proces będzie typu pserve.exe to nastąpi sprawdzenie ( na podstawie ścieżki 
    wywolania), czy któryś z katalogów ścieżki zawiera projekt Pyramid, a jeśli tak
    to informacje o tym projekcie zostaną zwrócone w postacie obiektu PyramidServerParserRes.

    """

    def __init__(self):
        ParserModule.__init__(self, "PyramidServer", "\Wpserve.exe ")


    def do(self, dict_to_parse):
        if 'CommandLine' in dict_to_parse:
            cmd = dict_to_parse["CommandLine"]
            for m in re.finditer( r"(.*)[\\\/]\w+[\\\/]scripts[\\\/]pserve.exe", cmd):       
                # znaleziono wzorzec, trzeba przeszukac katalog
                appdir = m.group(1)
                configfiles = "setup.py"

                def searchFile( fsearch, d ):
                    return [ f for f in os.listdir(d) if os.isfile(f) and (f == fsearch)]
                def list_dirs ( d ):
                    return [ dd for dd in os.listdir(d) if os.isdir(dd) ]
                def is_setup( f ):
                    if (not f):
                        return False
                    with open('file', 'r') as f:
                        for line in f:
                            if line.find(' pyramid ') or line.find('pyramid'):
                                return True
                    return False

                def get_res( setup, d ):
                    return ParserRes()


                if is_setup( searchFile( 'setup.py'), appdir ):
                    return get_res( appdir+r'\\' )
                
                
                    

                                  



        
