Project Title: "Elitism Enhancements for Genetic Algorithm Based Network Intrusion Detection System" (AceGA)

Please kindly obtain the published academic paper here: https://scholar.google.co.th/citations?user=qT9n7AIAAAAJ&hl=en

Contact Info: nik.muic@gmail.com

To run this program, you need to install deap (it's a python library).
optional: install pypy, it's a flavor of python intepreter (Much faster and better performance).


I.	Motivation

Network Security and Artificial intelligence are the two sub-fields in Computer Science
that I fascinate and have much interest in. Thus, I would like to make a contribution to
them by doing this project, as well as to learn and acquire knowledge as much as possible
along the way.

By integrating Genetic Algorithms into Network Intrusion Detection Systems, my purpose
could be realized.

II.	Problem

Signature-based Network Intrusion Detection Systems (i.e. Profile-based, Rule-based) is
able to detect and alert network administrators about the attack connections. But this
NIDS approach suffers high false-negative result rates, because a signature-based
Intrusion Detection System is only as good as its records of rules in its database. This
is due to its inability to learn and identify new types of attacks.

III.	Solution

A field in Artificial Intelligence: Evolutionary Algorithms, specifically Genetic
Algorithms (GA), has an excellent approach to solve this problem. There are two general
steps to apply GA to an NIDS, training stage and testing stage:

Training Stage: Firstly, GA can learn to make new rules (attack patterns) from existing
identified attack records in a dataset.

Testing Stage: Secondly, the newly made rules can then be stored in an IDS database in
order to strengthen the security level.
