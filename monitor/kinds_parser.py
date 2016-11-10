# -*- coding: utf-8 -*-

import re

class ParserRes(object):

    """Klasa rezultatu parsowania przez ParseModule """

    def __init__(self, kind, **kwargs):
        """Inicjalizacja 

        :kind: rodzaj sparsowanego obiektu
        [:*  ] : inne właściwości zależą od parsowanego obiektu

        """
        self.kind = kind
        for name, val in kwargs:
            setattr(self, name, val)


class ParserModule(object):

    """bazowy moduł parsera"""

    def __init__(self, kind, regex):
        """

        :regex: wyr. reg. do porównania 
        :kind: rodzaj obiektu do sparsowania

        """
        self._regex = regex
        self._kind = kind
    @property
    def kind( self ):
        return self._kind

    @classmethod
    def validate( class, obj ):
        attrs = ['next','do','process','_regex','_kind']
        return all( [ hasattr( obj, attr) for attr in attrs ] )

    def do(self, dict_to_parse):
        """Metoda wykonująca parsowanie (abstract)
        Metoda ta musi być nadpisana w każdej klasie potomnej.

        :dict_to_parse: słownik do sparsowania 
        :returns: obiekt ParserRes

        """
        raise Exception('Cannot invoke abstract class')
    
    def process(self, dict_to_parse):
        """Metoda przetwarzająca moduł w ła ńcuchu innych modułow
        Metoda parsuje wg wzorca `Chain of responsibility`

        Sposób przetworzenia:

        * każda wartość słownika jest sprawdzana za pomocą wyr. reg. self._regex, i jeśli
        * co najmniej jedna z wartości pasuje do wzorca to uruchmiana jest metoda
          :do(), która ma szansę przetworzyć słownik w celu wygenerowania bardziej
          szczegółowych danych w postaci obiektu :ParserRes
        * jeśli metoda :do() nie zwróci poprawnego rezultatu a obiekt posiada następny obiekt
          do przetworzenia (:next), to parsowanie zostanie uruchomione dla tego obiektu

        :dict_to_parse: słownik do sparsowania
        :returns: obiekt ParserRes

        """
        if not validate(self):
            raise Exception('Obiekt nie jest klasy ParserModule')

        res = None
        for f in dict_to_parse:
            if re.search( self._regex, dict_to_parse )
                res = do( dict_to_parse )
                break
        if (not res) and ( self.next ):
            res = self.next.process( dict_to_parse )
        return res


class KindParser(object):

    """Obiekt parsujący 
    - zawiera obiekty ParseModule
    """

    def __init__(self):
        self._modules = []

    def parse(self, dict_to_parse):
        """Parsowanie string dict_to_parse

        :dict_to_parse: string do sparsowania
        :returns: obiekt typu ParserRes lub None
        """
        if self._modules:
            return self._modules[0].process( dict_to_parse )

        return None
    def add_parser(self, parser):
        """Dodanie parsera do listy modułów przetwarzających

        :parser: obiekt typu ParserModule

        """
        last = self._modules[:-1]
        parser.next = None
        parser.prev = last
        if last:
            last.next = parser
        self._modules.append( parser )

