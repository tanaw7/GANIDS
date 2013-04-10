### Purpose is to use a rule tester to test the audit data records

from idsproto import *

#        [0, 0, 1, 'finger', 1050, 79, 192, 168, 1, 30, 192, 168, 0, 20, '-']
tester = [0, 0, -1, -1, -1, 23, 192, -1, -1, -1, -1, -1, -1, -1, -1]

matched_lines = 0.0
for line in auditData:
	matched_fields = 0.0

	for index, field in enumerate(line, start=0):
		if (tester[index] == field) or (tester[index] == -1):
			matched_fields = matched_fields + 1.0

	if matched_fields == 15.0:
		matched_lines = matched_lines + 1.0
		print line
		print tester

print "There are(is): %s Matched lines" % matched_lines