### Purpose is to use a rule tester to test the audit data records
### This part should be in the evaluator

from idsproto import *

#        [0, 0, 1, 'finger', 1050, 79, 192, 168, 1, 30, 192, 168, 0, 20, '-']
individual = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 'guess']

matched_lines = 0.0
A = 0.0
AnB = 0.0
for line in auditData:
	matched_fields = 0.0

	for index, field in enumerate(line, start=0):
		if (individual[index] == field) or (individual[index] == -1):
			matched_fields = matched_fields + 1.0
	if matched_fields >= 14.0:
		A += 1
	if matched_fields == 15.0:
		AnB += 1
	if matched_fields == 15.0:
		matched_lines = matched_lines + 1.0
		#print line

print 'A:', A
print 'AnB:', AnB
#print "There are(is): %s Matched lines" % matched_lines