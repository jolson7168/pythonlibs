
#Binary search
def binary_search(itemList, searchFor, offset,startIndex=0, endIndex=None):
#If not found, return either one before or one after, as determined by param offset
	if endIndex is None:
		endIndex = len(itemList)
	while startIndex < endIndex:
		mid = (startIndex + endIndex)//2
		midval = itemList[mid][1]
		#print "MID: %i Midval: %.8f" % (mid, midval)
		if midval < searchFor:
			startIndex = mid+1
		elif midval > searchFor:
			endIndex = mid
		else:
			#Found.
			return mid
	#Not found. 
	#mid is on the one before where our search value falls
	if (offset == -1):
		if (itemList[mid][1]>searchFor):
			if (mid-1)<0:
				return 0
			else:
				return mid-1
		else:
			return mid
	else:
		if (itemList[mid][1]>searchFor):
			return mid
		else:
			if (mid+1)>=len(itemList):
				return len(itemList)-1
			else:	
				return mid+1
