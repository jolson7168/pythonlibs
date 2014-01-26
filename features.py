from __future__ import print_function
import json
import datetime
import outputFunctions
from pprint import pprint

consolidationLog =[]


def default(obj):
    """Default JSON serializer."""
    import calendar, datetime

    if isinstance(obj, datetime.datetime):
    	theDate = obj.strftime('%Y-%m-%dT%H:%M:%S')
    return theDate
	

def compareArrays(x, y):
	#Is this safe?
	if (set(x) == set(y)):
		return True
	else:
		return False

def setNewValue(featureType,newEntry,value, isOverride):
	newEntry["timestamp"] = datetime.datetime.now() 
	newEntry["value"] = value
	if isOverride:
		newEntry["override"] = True
	return newEntry


def getFeature(part, feature, filename=None, lastFeature=False, isVersioned=True, metaData=False):
	if (filename != None):
		if filename in part["files"]: 
			if (metaData == False):			
				if (feature in part["files"][filename]["contents"]):
					if ("override" in part["files"][filename]["contents"][feature]) and (not lastFeature):
						if ("valueList" in part["files"][filename]["contents"][feature]):
							maxEl=len(part["files"][filename]["contents"][feature]["valueList"])
							found = False
							current = 0
							while (not found) and (current < maxEl):
								if "override" in (part["files"][filename]["contents"][feature]["valueList"][current]):
									found = True
								else:
									current=current+1
							if not found:  #Override flag set, no override value
								return None
							else:
								return part["files"][filename]["contents"][feature]["valueList"][current]["value"]
						
						else:
							print("No valuelist")
					else:
						if ("valueList" in part["files"][filename]["contents"][feature]):
							maxEl=len(part["files"][filename]["contents"][feature]["valueList"])-1
							if ("value" in part["files"][filename]["contents"][feature]["valueList"][maxEl]):
								return part["files"][filename]["contents"][feature]["valueList"][maxEl]["value"]
							else:
								print("Value missing")
						else:
							print("No valuelist")
				else:
					return None
			else:
				if (feature in part["files"][filename]):
					if ("override" in part["files"][filename][feature]) and (not lastFeature):
						if ("valueList" in part["files"][filename][feature]):
							maxEl=len(part["files"][filename][feature]["valueList"])
							found = False
							current = 0
							while (not found) and (current < maxEl):
								if "override" in (part["files"][filename][feature]["valueList"][current]):
									found = True
								else:
									current=current+1
							if not found:  #Override flag set, no override value
								return None
							else:
								return part["files"][filename][feature]["valueList"][current]["value"]
						
						else:
							print("No valuelist")
					else:
						if ("valueList" in part["files"][filename][feature]):
							maxEl=len(part["files"][filename][feature]["valueList"])-1
							if ("value" in part["files"][filename][feature]["valueList"][maxEl]):
								return part["files"][filename][feature]["valueList"][maxEl]["value"]
							else:
								print("Value missing")
						else:
							print("No valuelist")
				else:
					return None
		else:
			return None
	else:			
		if (feature in part):
			if not isVersioned:
				return part[feature]
			elif ("override" in part[feature]) and (not lastFeature):
				if ("valueList" in part[feature]):
					maxEl=len(part[feature]["valueList"])
					found = False
					current = 0
					while (not found) and (current < maxEl):
						if "override" in (part[feature]["valueList"][current]):
							found = True
						else:
							current=current+1
					if not found:  #Override flag set, no override value
						return None
					else:
						return part[feature]["valueList"][current]["value"]
				else:
					print("No valuelist")
			else:
				if ("valueList" in part[feature]):
					maxEl=len(part[feature]["valueList"])-1
					if ("value" in part[feature]["valueList"][maxEl]):
						return part[feature]["valueList"][maxEl]["value"]
					else:
						print("Value missing")
				else:
					print("No valuelist")
		else:
			return None

def addFeatureValue(part, feature, value, isOverride=False, filename=None, metaData=False):
	newEntry={}
	existingVal=None
	featureType = getFeatureType(value)
	if (filename == None):
		if ("featureType" in part[feature]):
			if "valueList" in part[feature]:
				maxEl=len(part[feature]["valueList"])-1
				if maxEl>=0:
					if "value" in part[feature]["valueList"][maxEl]: 
						existingVal = getFeature(part,feature,lastFeature=True)
						if existingVal != value:
							addType = "Change"   #Change
							setNewValue(part[feature]["featureType"],newEntry,value, isOverride)
							part[feature]["valueList"].append(newEntry)
						else:
							addType = "Existing"   #Already Exists, no change
					else:  #No "value"
						addType="Add"  #Add
						setNewValue(part[feature]["featureType"],newEntry,value, isOverride)
						part[feature]["valueList"].append(newEntry)
				else:
					addType = "Add"   #Add
					setNewValue(part[feature]["featureType"],newEntry,value, isOverride)
					part[feature]["valueList"].append(newEntry)
			else: #No valuelist
				addType = "Add"  #Add
				part[feature]["valueList"] = []
				setNewValue(part[feature]["featureType"],newEntry,value, isOverride)
				part[feature]["valueList"].append(newEntry)
			if isOverride:
				part[feature]["override"]=True

	else:
		if filename in part["files"]:
			if (metaData == False):			
				if feature in part["files"][filename]["contents"]:
					if ("featureType" in part["files"][filename]["contents"][feature]):
						if "valueList" in part["files"][filename]["contents"][feature]:
							maxEl=len(part["files"][filename]["contents"][feature]["valueList"])-1
							if maxEl>=0:
								if "value" in part["files"][filename]["contents"][feature]["valueList"][maxEl]: 
									existingVal = getFeature(part,feature,filename=filename,lastFeature=True)
									if existingVal != value:
										addType = "Change"   #Change
										setNewValue(part["files"][filename]["contents"][feature]["featureType"],newEntry,value, isOverride)
										part["files"][filename]["contents"][feature]["valueList"].append(newEntry)
									else:
										addType = "Existing"   #Already Exists, no change, but might need to override
										if isOverride:
											setNewValue(part["files"][filename]["contents"][feature]["featureType"],newEntry,value, isOverride)
											part["files"][filename]["contents"][feature]["valueList"].append(newEntry)									
									

								else:  #No "value"
									addType="Add"  #Add
									setNewValue(part["files"][filename]["contents"][feature]["featureType"],newEntry,value, isOverride)
									part["files"][filename]["contents"][feature]["valueList"].append(newEntry)
							else:
								addType = "Add"   #Add
								setNewValue(part["files"][filename]["contents"][feature]["featureType"],newEntry,value, isOverride)
								part["files"][filename]["contents"][feature]["valueList"].append(newEntry)
						else: #No valuelist
							addType = "Add"  #Add
							part[feature]["valueList"] = []
							setNewValue(part["files"][filename]["contents"][feature]["featureType"],newEntry,value, isOverride)
							part["files"][filename]["contents"][feature]["valueList"].append(newEntry)
						if isOverride:
							part["files"][filename]["contents"][feature]["override"]=True
			else: #metaData = True
				if feature in part["files"][filename]:
					if ("featureType" in part["files"][filename][feature]):
						if "valueList" in part["files"][filename][feature]:
							maxEl=len(part["files"][filename][feature]["valueList"])-1
							if maxEl>=0:
								if "value" in part["files"][filename][feature]["valueList"][maxEl]: 
									existingVal = getFeature(part,feature,filename=filename,lastFeature=True,metaData=True)
									if existingVal != value:
										addType = "Change"   #Change
										setNewValue(part["files"][filename][feature]["featureType"],newEntry,value, isOverride)
										part["files"][filename][feature]["valueList"].append(newEntry)
									else:
										addType = "Existing"   #Already Exists, no change, but might need to override
										if isOverride:
											setNewValue(part["files"][filename][feature]["featureType"],newEntry,value, isOverride)
											part["files"][filename][feature]["valueList"].append(newEntry)									
								else:  #No "value"
									addType="Add"  #Add
									setNewValue(part["files"][filename][feature]["featureType"],newEntry,value, isOverride)
									part["files"][filename][feature]["valueList"].append(newEntry)
							else:
								addType = "Add"   #Add
								setNewValue(part["files"][filename][feature]["featureType"],newEntry,value, isOverride)
								part["files"][filename][feature]["valueList"].append(newEntry)
						else: #No valuelist
							addType = "Add"  #Add
							part["files"][filename][feature]["valueList"] = []
							setNewValue(part["files"][filename][feature]["featureType"],newEntry,value, isOverride)
							part["files"][filename][feature]["valueList"].append(newEntry)
						if isOverride:
							part["files"][filename][feature]["override"]=True
#	if existingVal is not None:
#		s={"addType":addType,"featureType":featureType,"feature":feature,"existing":existingVal,"new":value}
#	else:
#		s={"addType":addType,"featureType":featureType,"feature":feature,"new":value}
#	consolidationLog.append(s)

def featureExists(part,feature,filename=None):
	found = False	
	if (filename != None):
		if filename in part["files"]:
			if feature in part["files"][filename]["contents"]:
				found = True
	else:	
		if feature in part:
			found = True
	return found				

def setFeature(part, feature, value, filename=None, doIgnore=False, isOverride=False, metaData=False):
	if not doIgnore: 
		featureType = getFeatureType(value)
		if (filename!=None):
			if "files" not in part:
				part["files"]={}
			if filename in part["files"]:
				if (metaData == True):
					if (feature in part["files"][filename]):
						if (featureType== 1): #Type1	
							addFeatureValue(part, feature,value,filename=filename,metaData=True)
						elif (featureType == 2):
							if (not compareArrays(getFeature(part,feature,filename=filename,lastFeature=True), value)):		#Type2
								addFeatureValue(part, feature,value,filename=filename,metaData=True)
						else:	#Type3
							addFeatureValue(part, feature,value,filename=filename,metaData=True)
					else:
						part["files"][filename][feature] = {}	
						part["files"][filename][feature]["featureType"] = featureType
						part["files"][filename][feature]["valueList"] = []
						addFeatureValue(part, feature,value,isOverride,filename=filename,metaData=True)
				else:
					if (feature in part["files"][filename]["contents"]):
						if (featureType== 1):						#Type1	
							addFeatureValue(part, feature,value,isOverride=isOverride,filename=filename)
						elif (featureType == 2):
							if (not compareArrays(getFeature(part,feature,filename=filename,lastFeature=True), value)):		#Type2
								addFeatureValue(part, feature,value,isOverride=isOverride,filename=filename)
						else:										#Type3
							addFeatureValue(part, feature,value,isOverride=isOverride,filename=filename)
					else:
						part["files"][filename]["contents"][feature] = {}
						part["files"][filename]["contents"][feature]["featureType"] = featureType
						part["files"][filename]["contents"][feature]["valueList"] = []
						if isOverride:
							part["files"][filename]["contents"][feature]["override"] = True
						addFeatureValue(part, feature,value,isOverride,filename=filename)
			else:
				print("Filename: "+filename+ " does not exist in part")
		else:		
			if (feature in part):
				if (featureType== 1):						#Type1	
					addFeatureValue(part, feature,value, isOverride)
				elif (featureType == 2):
					if (not compareArrays(getFeature(part,feature,lastFeature=True), value)):		#Type2
						addFeatureValue(part, feature,value, isOverride)
				else:										#Type3
					addFeatureValue(part, feature,value, isOverride)
			else:
				part[feature] = {}
				part[feature]["featureType"] = featureType
				part[feature]["valueList"] = []
				if isOverride:
					part["files"][filename]["contents"][feature]["override"] = True
				addFeatureValue(part, feature,value, isOverride)
#	else:
#		s={"addType":"ignored","featureType":featureList[feature]["type"],"feature":feature,"new":value}
#		consolidationLog.append(s)


#Fix this, not sure if logic around the typing is sound.
def getFeatureType(value):
	if (type(value) is str) or (type(value) is unicode) or (type(value) is int) or (type(value) is float):
		return 1
	elif isinstance(value, list):
		if (type(value[0]) is str) or (type(value[0]) is unicode) or (type(value[0]) is int) or (type(value[0]) is float):
			return 2	
		else:
			return 3


def appendConsolidationLog(logPath):
	newEntry={}
	rightNow=datetime.datetime.now()
	newEntry["consolidationDate"]= rightNow
	newEntry["consolidationActions"]=[]
	newEntry["consolidationActions"]=consolidationLog
	try:
		with open(logPath) as logFile:
			theLog = json.load(logFile)
	except IOError:
			theLog ={}
	theLog[rightNow.strftime("%m/%d/%y %H:%M")]=newEntry
	fp= open(logPath, "w+")
	print (json.dumps(theLog,indent=4,sort_keys=True,default=default),file=fp)
	fp.truncate()
	fp.close()

#This needs work.
def consolidateFeatures(newPart,existingPart,featureList,consolidationLogPath):
	consolidated={}
	consolidated=existingPart
	for feature in newPart:
		if (featureList[feature]["migrated"] == "yes"):
			if (featureList[feature]["versioned"] == "yes"):
				#if feature already in existingPart, it is handled below
				setFeature(consolidated, feature, newPart[feature])
			if (featureList[feature]["versioned"] == "no"):
				if feature not in consolidated:
					setFeature(consolidated, feature, newPart[feature])
		elif (featureList[feature]["migrated"] == "special - unique"):
			if (featureList[feature]["versioned"] == "no"):
				if feature not in consolidated:
					setFeature(consolidated, feature, newPart[feature])
		elif (featureList[feature]["migrated"] == "special - combined"):		#Files
				if feature not in consolidated:
					consolidated[feature] = {}
				for aFile in newPart[feature]:					#each file
					print("Feature: "+str(feature))
					fileName=aFile["path"].rsplit('\\', 1)[1]
					if not (fileName in consolidated[feature]):
						consolidated[feature][fileName]={}
						consolidated[feature][fileName]["contents"]={}
					for fileFeature in aFile:				#each meta feature for file
						#aFile = entire contents of the file
						#feature here = files
						if (featureList[fileFeature]["migrated"] == "yes"):
							if (featureList[fileFeature]["versioned"] == "yes"): 
								setFeature(consolidated, fileFeature, aFile[fileFeature], filename=fileName, metaData=True)
						elif (featureList[fileFeature]["migrated"] == "special - combined"):
							if fileFeature not in consolidated[feature][fileName]:
								consolidated[feature][fileName][fileFeature]={}
							for contentFeature in aFile[fileFeature]: #each feature in contents
 								setFeature(consolidated,contentFeature,aFile[fileFeature][contentFeature],filename=fileName)
		#appendConsolidationLog(consolidationLogPath)
	return consolidated

def loadFeatures(pathToFeatureFile):
	featureDict={}
	try:
		with open(pathToFeatureFile) as featureFile:
			features = json.load(featureFile)
			for feature in features["features"]:
				featureDict[str(feature["name"])]=feature
			return featureDict
	except IOError:
		#handle file not found				
		return featureDict
