import string, sys, math
from _collections import defaultdict

transition= defaultdict(int)
emission= defaultdict(int)
context= defaultdict(int)
totalTags= defaultdict(int)
states= set()
WordInTag= dict()

#testFile= sys.argv[1]
#fTest= open(testFile, 'r')
fTest= open('catalan_corpus_dev_raw.txt', 'r')
fModel= open('hmmmodel.txt', 'r')
fOutput= open('hmmoutput.txt','w')

lines = fModel.readlines()

for line in lines:
	if line.startswith('T'):
		t, values= line.strip("\n").split(' ',1)
		key, prob= values.strip().split(' ')
		transition[key]= float(prob)
#		print key, transition[key]
	elif line.startswith('E'):
		e, values= line.strip("\n").split(' ',1)
		key, prob= values.strip().split(' ')
		emission[key]= float(prob)
#	elif line.startswith('S'):
#		s, counts= line.strip("\n").split(' ',1)
#		tag, counts= counts.split(' ')
#		totalTags[tag]= counts
#		
	elif line.startswith('C'):
		c, counts= line.strip("\n").split(' ',1)
		key, counts= counts.split(' ')
		context[key]= counts
	elif line.startswith('W'):
		w, wordandtags= line.strip("\n").split(' ',1)
		word, tags= wordandtags.strip().split(' ')
		if word not in WordInTag:
			WordInTag[word]= set()
		tags= tags.strip().strip(",").strip()
		tags= tags.split(",")
		for t in tags:
			WordInTag[word].add(t.strip())
			states.add(t.strip())
#print len(states)

lines= fTest.readlines()

for line in lines:
	probability= [defaultdict(str)]
	backpointer= [defaultdict(str)]
	obsv= line.strip("\n").split(' ')
	if obsv[0] in WordInTag:
		which_tags= WordInTag[obsv[0]]
		for i in which_tags:
			if i in states and (i+"->"+obsv[0].strip()) in emission:
				probability[0][i]= math.log(transition["q->"+i]) + math.log(emission[i+"->"+obsv[0].strip()])
				backpointer[0][i]= "q"
	else:
		for i in states:
			if transition["q->"+i] == 0:
				transition["q->"+i] = 1/(float(context["q"])+len(states))
			probability[0][i]= math.log(transition["q->"+i])
			backpointer[0][i]= "q"
			#print i, probability[0][i]
	for t in range(1, len(obsv)):
		probability.append(defaultdict(str))
		backpointer.append(defaultdict(str))
		if obsv[t] in WordInTag:
			which_tags= WordInTag[obsv[t]]
			for i in which_tags:
				maxval= -sys.maxint - 1
				if (i+"->"+obsv[t].strip()) in emission:
					for i0 in states:
						if i0 in probability[t-1]:
							probab= probability[t-1][i0] + math.log(transition[i0+"->"+i]) + math.log(emission[i+"->"+obsv[t].strip()])
							if probab > maxval:
								maxval= probab
								backpointer[t][i]= i0
				probability[t][i]= maxval
		else:
			for i in states:
				maxval= -sys.maxint - 1
				for i0 in states:
					if i0 in probability[t-1]:
						if transition[i0+"->"+i] == 0:
							transition[i0+"->"+i]= 1/(float(context[i0])+len(states))
						probab= probability[t-1][i0] + math.log(transition[i0+"->"+i])
						if probab > maxval:
							maxval= probab
							backpointer[t][i]= i0
				probability[t][i]= maxval
				#print "---"+i+" "+str(probability[0][i])

	argmax = -sys.maxint - 1
	for i in states:
		if i in probability[len(obsv)-1] and probability[len(obsv)-1][i] > argmax:
			argmax= probability[len(obsv)-1][i]
			mostprobablestate= i
	#print mostprobablestate
	#print backpointer
	#print probability
	#print transition["VB->VB"]
	#print type(mostprobablestate)
	result=""
	for k in range(len(backpointer)):
		result += obsv[len(obsv)-1-k]+"/"+mostprobablestate+" "
		mostprobablestate= backpointer[len(backpointer)-1-k][mostprobablestate]
	#print result
	result= result.strip().split(' ')
	sequence=""
	for k in range(len(result)):
		sequence += result[len(result)-1-k]+" "
	#print sequence
	fOutput.write(sequence+"\n")