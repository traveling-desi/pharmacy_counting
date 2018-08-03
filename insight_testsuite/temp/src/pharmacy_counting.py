import sys, os, csv, collections
from exceptions import IllegalArgumentError
from customClasses import costList


outFieldNames = "drug_name,num_prescriber,total_cost".split(',')
inFieldNames = "id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost".split(',')

def openFile(fileN, perm):
	try:
		inFile = open(fileN, perm)
		return inFile
	except:
		print("Can't open"+ fileN)
		exit()

def checkInputs(arg, inFieldNames, outFieldNames):
	if len(arg) < 3: raise IllegalArgumentError('Usage: ScriptName <Input File> <Output File>') 
	input, output = arg[1], arg[2]
	inFile, outFile = openFile(input, "r"), openFile(output, "w+")
	return csv.DictReader(inFile, inFieldNames), csv.writer(outFile, outFieldNames)



def summarize():
	inreader, outwriter = checkInputs(sys.argv, inFieldNames, outFieldNames)
	next(inreader)
	outwriter.writerow(outFieldNames)
	outDict = collections.defaultdict(costList)
	for line in inreader:
		drug = line['drug_name']
		cost = float(line['drug_cost'])
		outDict[drug].num += 1
		outDict[drug].cost += cost

	for drug in outDict.keys():
		outwriter.writerow([drug,outDict[drug].num, outDict[drug].cost])

	#close(inreader); close(outwriter)

	

if __name__ == "__main__":
	summarize()

