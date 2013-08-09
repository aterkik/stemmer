import sys

if len(sys.argv) > 1:
	spaces = open(sys.argv[1], 'r').read().replace('\t', '    ')
	open('spaces_' + sys.argv[1], 'w').write(spaces)
