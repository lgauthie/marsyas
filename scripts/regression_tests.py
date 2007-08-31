#!/usr/bin/python
import sys
import os
import filecmp

LOG_FILE = 'results.log'

# chdir to test directory
marsyasBaseDir = os.path.dirname(sys.argv[0])
marsyasBaseDir = os.path.abspath( marsyasBaseDir )
marsyasBaseDir = os.path.join(marsyasBaseDir+os.sep+'..'+os.sep)
marsyasBaseDir = os.path.abspath( marsyasBaseDir )
os.chdir (marsyasBaseDir + os.sep + 'regressionTests')

#print os.getcwd()

# setup release/debug/installed mode
if len(sys.argv) > 1:
	mode = sys.argv[1]
else:
	mode = 'release'
if not( (mode=='release') or (mode=='debug') or (mode=='installed')):
	print "Please select `release', `debug', or `installed' mode."
	sys.exit()
if (mode == 'installed'):
	mode = ''

problem = 0

def doTests(test_filename, temp_filename):
	global logfile
	global problem
	test_commands = []
	test_answers = []

	# load tests
	tests = open('..'+os.sep+test_filename).readlines()
	for line in tests:
		if (not(line[0]=='#') and not(line[0]=='\n')):
			line_split = line.split('\t')
			test_commands.append( line_split[0] )
			if (len(line_split)==2):
				test_answers.append( line_split[1].strip() )
			else:
				test_answers.append('')

	# do tests
	for i in range( len(test_commands) ):
		command = ''
		if mode != '':
			command = '..%(sep)s..%(sep)sbin%(sep)s%(mode)s%(sep)s' % {'sep': os.sep, 'mode': mode}
		command += test_commands[i]
		#print command
		if (os.system(command) != 0): # if something went wrong
			problem = 1
			logfile.write("Test " + str(i) + " FAILED:   " + test_commands[i]+'\n')
			break
		if not(test_answers[i] == ''):
			# use .au files because identical-sounding .wav files can have
			# different headers
			if filecmp.cmp(temp_filename, test_answers[i]):
				logfile.write("Test " + str(i) + " successful\n")
			else:
				logfile.write("Test " + str(i) + " FAILED:   " + test_commands[i]+'\n')
				problem = 1
		else:
			# we would have found a problem above
			logfile.write("Test " + str(i) + " successful\n")

#test_file = 'testlist.txt'
logfile = open(LOG_FILE, 'w')
os.chdir('audio')
logfile.write("--------- Audio tests\n")
doTests('audio-tests.txt', 'out.au')
logfile.write("--------- Text output tests\n")
doTests('text-tests.txt', 'out.txt')
logfile.close()

print "*********   TEST RESULTS *********"
if (problem):
	print "Some test(s) failed.  Please see regressionTests/" + LOG_FILE,
	print "for an account of the damage."
	print "  (tests are 0-indexed)"
	sys.exit(1)
else:
	print "All tests passed.  Congratulations, you didn't",
	print "break Marsyas!  (this time)"
	sys.exit(0)

