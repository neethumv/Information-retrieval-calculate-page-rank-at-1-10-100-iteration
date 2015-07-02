
import sys
#P is the set of all pages; |P| = N
# S is the set of sink nodes, i.e., pages that have no out links
# M(p) is the set (without duplicates) of pages that link to page p
# L(q) is the number of out-links (without duplicates) from page q
# d is the PageRank damping/teleportation factor; use d = 0.85 as is typical


P = set();
M = dict();
d = 0.85;
L = dict();
S = list();
PR = dict();
page_rank = dict()
key_value = dict()

#Main program which takes the input file name
def main(filename):
	textfile = file('IterationResult.txt', 'wt')
	extractGraph(filename)
	#the iteration at which the PageRank calculation will stop
	iter = [1,10,100]
	newpage_rank = []
	for i in iter:
		page_rank = calpagerank(i)
		with open('IterationResult.txt', 'a') as fp:
			print 'writing in file'
			print page_rank
			for p in page_rank.items():
				fp.write("%s:%s\n" % p)
			fp.write("-----------------\n")
	
	print 'done reading the input file'
	
#this program takes the input file and creates the M dictionary, P set, L list and S list	
def extractGraph(filename):
	infile = open(filename)
	content = infile.readlines()
	for line in content:
		line = line.rstrip();
		x = line.split(' ');
		p = x[0];
		#adding the unique pages to the P set
		P.add(p)
		setlines = set(x[1:])

		#adding the in-link nodes for each pages in P 	
		if p in M:
			print M[p]
			M[p] = M[p].union(setlines)
			print M[p]
		else:
			M[p] = setlines

	#initialising the count of out-links for all the pages to 0 
	for i in P:
		L[i] = 0;
	#creating a key_value dictionary which hold the pages as keys and the number of its in-links as values
	for key in M:
		key_value[key] = len(M[key])
		
	#updating the L list with the number of out-links for each key value in M
	for values in M.values():
		for value in values:
			L[value] += 1
	#creating the S list which holds the sink node(page which does not have out-links)
	for p in P:
		if (L[p] == 0):
			if(p not in S):
				S.append(p)
	
	infile.close()	
	print 'M dictionary for the given graph is:\n'
	print M 
	print 'The set of pages in P are:\n'
	print P
	print 'The number of outlinks for each page are:\n'
	print L
	print 'The sink node if any:\n'
	print S 
	print 'the number of inlink count for each page:\n'
	print key_value
	
#this method calculates the page rank and stop the calculation at 1, 10th and 100th iteration	
def calpagerank(iter):
	newPR = dict()
	N = len(P)
	num_iter = 0
	
	for p in P:
		#initial value
		PR[p] = 1.0/N
	#stop the loop when the iteration reaches 1, 10 and 100	
	while (num_iter < iter):
		sinkPR = 0
		for p in S:
			#calculate total sink PR
			sinkPR += PR[p]
		for p in P:
			#teleportation
			newPR[p] = (1-d)/N;
			#spread remaining sink PR evenly
			newPR[p] += d*sinkPR/N
			#pages pointing to p
			for q in M[p]:
				#add share of page-rank from in-links
				newPR[p] += d*PR[q]/L[q] 
		
		for p in P:
			PR[p] = newPR[p]
		num_iter += 1 
			
	return PR
	


#Main program:

if __name__ == '__main__':
	main(sys.argv[1])
