#!/usr/bin/python
#-*- coding: iso-8859-7 -*-

import os
from sqlalchemy import func
import codecs
import hashlib
import __init__
from dbPhoto import photoDir,photoFile
"""import dbPhoto"""
from sqlalchemy.orm.exc import *

"""τώρα πρέπει να δω τα ελληνικά στη βάση και πώς θα κάνω truncate με foreign key constraint"""
"""πρέπει να ελέγξω να μην προσθέτει τις ίδιες φωτογραφίες"""

"""create hash for file"""
def hashValueToFile(fpath):

	try:
		fd=open(fpath,'rb')
	except:
		print "open file error"

	
	sha=hashlib.sha256()
	while True:
		line=fd.read(8192)
		if not line:
			break
		sha.update(line)

	"""hashValue=sha.digest()"""
	hashValue=sha.hexdigest()
	return hashValue

def findDuplsFiles(rootDir):

	fd=codecs.open(__init__.photoFile,"w","utf-8")
	dupsFile={}
	
	for dirpath,dirnames,filenames in os.walk(rootDir,topdown=True):

		fd.write(dirpath.decode('utf-8') + '\n')

		for filename in filenames:

			fd.write(filename.decode('utf-8') + '\n')

			fpath=os.path.join(dirpath,filename)
			
			hashFile=hashValueToFile(fpath)
			"""print(fpath,' ',hashFile)"""			

			if hashFile not in dupsFile:
				dupsFile[hashFile]=[fpath]
			else:
				dupsFile[hashFile].append(fpath)
	fd.close()
	return dupsFile

"""import the database with files and dictionaries"""
def importDatabase(photofile):
	
	try:
		fd=open(photofile,'rb')
	except:
		print "open file error"
	
	for l in fd:

		numrows_photoDirs=__init__.dbsession.query(func.count(photoDir.id)).scalar()
			
		if numrows_photoDirs==0:
			numrows_photoDirs=1
		else:
			numrows_photoDirs+=1

		
		"""check if file table is empty"""
		numrows_photoFile=__init__.dbsession.query(func.count(photoFile.id)).scalar()
		if numrows_photoFile==0:
			numrows_photoFile=1
		else:
			numrows_photoFile+=1

		if l.startswith('/'):
			pathName=l.strip()

			select_path=__init__.dbsession.query(photoDir).filter(photoDir.pathname==pathName).one_or_none()
			if select_path==None:
				insert_dir=photoDir(id=str(numrows_photoDirs),pathname=pathName)
				__init__.dbsession.add(insert_dir)
			
			num_id_path=str(numrows_photoDirs)
		else:
			nameFile=l.strip()
			
			insert_file=photoFile(id=numrows_photoFile,id_path=num_id_path,filename=nameFile)
			"""insert_file=photoFile(id=numrows_photoFile,id_path=str(numrows_photoDirs),filename=nameFile)"""
			__init__.dbsession.add(insert_file)	
		
		__init__.dbsession.commit()
		
	fd.close()		

if __name__== '__main__':

	dupsFileDict=findDuplsFiles(__init__.rootDir)

	importDatabase(__init__.photoFile)

	fd=codecs.open("dupsFileDict","w","utf-8")
	
	for key,values in dupsFileDict.iteritems():
		if len(values)>1:			
			print(key,":")
			for val in values:			
					print val + " "
					fd.write(val + ' ')
			print("\n")
			fd.write('\n')

	fd.close()
	

	

	
