import re, unittest
from stemmer import stemmer

vc_data = { 'tr' : 0,
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
			'lymoges' : 3 }

class StemmerTest(unittest.TestCase):
	def testVCMeasure(self):
		s = stemmer()
		for word, measure in vc_data.items():
			self.failUnless(s.m(word) == measure, "Measure test failed for word '%s' calculated (%d)  \
												   should have been (%d)" % (word, s.m(word), measure) )
	
	def testStem(self):	
		s = stemmer()
		output = file('output.txt')
		for word in file('voc.txt'):
			word = word.strip()
			stem = output.next().strip()
			self.failUnless(s.stem(word) == stem, "Test failed for word \'%s\' stemmed to %s " \
												  "should have been %s " % (word, s.stemmed, stem) )

if __name__ == '__main__': unittest.main()
