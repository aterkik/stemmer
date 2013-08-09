Stemmer
=======

Martin Porter's stemming algorithm implemented in pure Python


Usage
=====

>>> from stemmer import stemmer
>>> stemmer.stem('logically')
'logic'
>>> stemmer.stem('doing')
'do'
>>> stemmer.stem('acceptable')
'accept'
>>> stemmer.stemmed # returns the last stemmed word
'accept'
    
License
=======

The software is licensed under the MIT license.


