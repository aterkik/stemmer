Stemmer
=======

Martin Porter's stemming algorithm implemented in pure Python


Usage
=====

>>> from stemmer import Stemmer
>>> s = Stemmer()
>>> s.stem('logically')
'logic'
>>> s.stem('doing')
'do'
>>> s.stem('acceptable')
'accept'
>>> s.stemmed # returns the last stemmed word
'accept'
    
License
=======

The software is licensed under the MIT license.


