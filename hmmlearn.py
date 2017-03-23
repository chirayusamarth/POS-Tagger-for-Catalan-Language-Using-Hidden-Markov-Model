import sys
from _collections import defaultdict

transition= defaultdict(int)
emission= defaultdict(int)
context= defaultdict(int)
totalTags= defaultdict(int)
WordInTag= dict()
states= set()

#trainingFile= sys.argv[1]
#fTraining= open(trainingFile, 'r')
fTraining= open('catalan_corpus_train_tagged.txt', 'r')
fModel= open('hmmmodel.txt','w')

sentences= fTraining.readlines()
	
for word_tags in sentences:
	word_tags= word_tags.strip().split(' ')
	previous="q"
	context[previous]+=1
	for wordtag in word_tags:
		word= wordtag[:-3]
		tag= wordtag[-2:]
		if wordtag!=word_tags[-1]:
			context[tag]+=1
		totalTags[tag]+=1
		transition[previous+" "+tag]+=1
		emission[tag+" "+word]+=1
		previous=tag
		if word not in WordInTag:
			WordInTag[word]= set()
		WordInTag[word].add(tag)
		#print word, WordInTag[word]
		states.add(tag)
#print states
totalStates= len(states)
print totalStates

for key in transition:
	previous, tag= key.split(' ')
	#fModel.write("T "+key+" "+str(transition[key])+" "+str(float(transition[key]+1)/(context[previous]+totalStates))+"\n")
	#if key not in transition:
	fModel.write("T "+previous+"->"+tag+" "+str(float(transition[key]+1)/(context[previous]+totalStates))+"\n")
	#else:
	#	fModel.write("T "+previous+"->"+tag+" "+str(float(transition[key])/float(context[previous]))+"\n")

for key in emission:
	tag, word= key.split(' ')
	#fModel.write("E "+tag+" "+word+" "+str(emission[key])+" "+str(totalTags[tag])+" "+str(float(emission[key])/float(totalTags[tag]))+"\n")
	fModel.write("E "+tag+"->"+word+" "+str(float(emission[key])/float(totalTags[tag]))+"\n")

#for key in totalTags:
#	fModel.write("S "+key+" "+str(totalTags[key])+"\n")

for key in context:
	fModel.write("C "+key+" "+str(context[key])+"\n")

for word in WordInTag:
	s = "W "+ word + " "
	for tag in WordInTag[word]:
		s += str(tag) + ","
	s += "\n"
	fModel.write(s)
#	print s