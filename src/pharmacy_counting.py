import sys, os, csv, collections, re
import time
from exceptions import IllegalArgumentError
from customClasses import costList

OUTFIELDNAMES = "drug_name,num_prescriber,total_cost".split(',')
INFIELDNAMES = "id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost".split(',')


class pharmacy_counter(object) :

	def __init__(self, inFile, outFile, inFieldNames, outFieldNames):
		self.outFieldNames = outFieldNames
		self.inFieldNames = inFieldNames
		self.inFile = inFile
		self.outFile = outFile		
		self.outDict = collections.defaultdict(costList)
		self.inreader = csv.DictReader(self.inFile, self.inFieldNames)
		self.outwriter = csv.writer(self.outFile, self.outFieldNames)

	def readIn(self, header=True):
		if header: next(self.inreader)
		for line in self.inreader:
			drug = line['drug_name'].strip()
			#if not bool(re.match('^[a-zA-Z0-9 \-%./]+$', drug)): print("skipped drug " + drug); continue
			cost = line['drug_cost'].strip()
			if not bool(re.match('^[0-9.]+$', cost)): print("skipped drug " + drug + ". Something wrong with cost."); continue
			self.outDict[drug].num += 1
			self.outDict[drug].cost += float(cost)

	def writeOut(self, writeHeader=True):
		if writeHeader: self.outwriter.writerow(self.outFieldNames)
		for drug in self.outDict.keys():
			self.outwriter.writerow([drug, self.outDict[drug].num, int(self.outDict[drug].cost)])

	def close(self):
		self.inFile.close()
		self.outFile.close()


def openFile(fileN, perm):
	try:
		inFile = open(fileN, perm)
		return inFile
	except:
		return 0
		

def checkInputs(arg):
	if len(arg) < 3: raise IllegalArgumentError('Usage: ScriptName <Input File> <Output File>') 
	input, output = arg[1], arg[2]
	inFile, outFile = openFile(input, "r"), openFile(output, "w+")
	if not inFile: print("Can't open input file for read "+ input)
	if not outFile: print("Can't open output file for write "+ output)
	return inFile, outFile


def timeIt(fn):
	n1=time.time()
	fn()
	n2=time.time()
	return (n2-n1)/60


if __name__ == "__main__":
	inFile, outFile = checkInputs(sys.argv)
	if not inFile or not outFile:
		exit(0)
	pCtr = pharmacy_counter(inFile, outFile, INFIELDNAMES, OUTFIELDNAMES)
	runList = [pCtr.readIn, pCtr.writeOut, pCtr.close]

	for script in runList:
		print("Finished "+str(script)+" in " + str(timeIt(script)) + " minutes")

