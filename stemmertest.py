""" Unit tests for Stemmer """

import unittest
from stemmer import Stemmer

VC_DATA = { 'tr' : 0,
			'ee' : 0,
			'tree' : 0,
			'y' : 0,
			'by' : 0,
			'trouble' : 1,
			'oats' : 1,
			'trees' : 1,
			'ivy' : 1,
			'fil' : 1,
			'troubles' : 2,
			'private' : 2,
			'oaten' : 2,
			'allay' : 2,
			'berhyme' : 2,
			'esay' : 2,
			'yclep' : 1,
			'yyclep' : 2,
			'lymoges' : 3}

class StemmerTest(unittest.TestCase):
    """ Main tester class. """
    def test_VC_measure(self):
        """ Tests the VC measure. """
        stemmer = Stemmer()
        for word, measure in VC_DATA.items():
            self.failUnless(stemmer.m(word) == measure,
                            "Measure test failed for word '%s' calculated (%d) \
						    should have been (%d)" % (word, stemmer.m(word),
                            measure))

    def test_stem(self):
        """ Checks the final stems. """
        stemmer = Stemmer()
        output = file('output.txt')
        for word in file('voc.txt'):
            word = word.strip()
            stem = output.next().strip()
            self.failUnless(stemmer.stem(word) == stem,
                                        "Test failed for word \'%s\' stemmed "\
                                        "to %s should have been %s"\
                                        % (word, stemmer.stemmed, stem))

if __name__ == '__main__':
    unittest.main()
