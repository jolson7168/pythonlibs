import boto
import logging
import os
from boto.s3.key import Key
import gcs_oauth2_boto_plugin

def logProgress(sent, totalSize, logger=None):
    perDone = round(((sent/float(totalSize))*100),2)
    if logger:
    	logger.info(str(round(((sent/float(totalSize))*100),2))+"% complete") 
    else:
	print str(round(((sent/float(totalSize))*100),2))+"% complete"

def uploadFileGCS(clientID, clientSecret, fileName, keyName, bucket, storageSchema, logger=None):

	if logger:
		logger.info('Starting upload. File: '+fileName +' Target: '+bucket)
	else:
		print('Starting upload. File: '+fileName +' Target: '+bucket)

	if storageSchema == "gs":
		gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(clientID, clientSecret)
	with open(fileName, 'r') as localfile:
		dst_uri = boto.storage_uri(bucket + '/' + keyName, storageSchema)
		dst_uri.new_key().set_contents_from_file(localfile)
		print 'Successfully created "%s/%s"' % (dst_uri.bucket_name, dst_uri.object_name)



def uploadStringToS3(aws_access_key_id, aws_secret_access_key, uploadString, bucket, theKey, logger=None, callback=None, md5=None, reduced_redundancy=False, content_type=None):

    if logger:
    	logger.info('Starting upload. String: '+uploadString +' Target: '+bucket)
    else:
    	print('Starting upload. String: '+uploadString +' Target: '+bucket)

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket, validate=True)
    k = Key(bucket)
    k.key = theKey
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_string(uploadString, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy)

    if sent == len(uploadString):
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

def uploadToS3(aws_access_key_id, aws_secret_access_key, filename, bucket, theKey, logger=None, callback=None, md5=None, reduced_redundancy=False, content_type=None):

    file = open(filename, 'r+')

    if logger:
    	logger.info('Starting upload. File: '+filename +' Target: '+bucket)
    else:
    	print('Starting upload. File: '+filename +' Target: '+bucket)

    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket, validate=True)
    k = Key(bucket)
    k.key = theKey
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)

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
