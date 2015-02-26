import boto
import logging
import os
from boto.s3.key import Key
import gcs_oauth2_boto_plugin


def uploadFileToCloudStore(accessKeyID, secretAccessKey, fileName, inBucket, theKey, logger=None, callback=None, md5=None, reducedRedundancy=False, contentType=None, destination='s3'):

	file = open(fileName, 'r+')

	if logger:
		logger.info('Starting upload. File: '+fileName +' Target: '+inBucket)
	else:
		print('Starting upload. File: '+fileName +' Target: '+inBucket)

	try:
		size = os.fstat(file.fileno()).st_size
    	except:
		file.seek(0, os.SEEK_END)
		size = file.tell()

	if destination == "gs":
		gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(accessKeyID, secretAccessKey)
		conn = boto.storage_uri(destination+"://"+inBucket+'/'+theKey)
		k = conn.new_key()

	elif destination =="s3":
		conn = boto.connect_s3(accessKeyID, secretAccessKey)
		bucket = conn.get_bucket(inBucket, validate=True)
		k = Key(bucket)


	k.key = theKey
	if contentType:
		k.set_metadata('Content-Type', contentType)
#	sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reducedRedundancy, rewind=True)
	sent = k.set_contents_from_file(file, cb=callback, md5=md5, rewind=True)

	file.seek(0)

	if sent == size:
		if logger:
			logger.info('Upload Success!')
		else:
			print('Upload Success!')
		return True
	else:
		if logger:
			logger.error('Upload Failed!')
		else:
			print('Upload Failed!')
    		return False
