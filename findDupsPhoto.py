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

			if hashFile not in dupsFile:
				dupsFile[hashFile]=[fpath]
			else:
				dupsFile[hashFile].append(fpath)
	fd.close()
	return dupsFile

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
				num_id_path=select_path.id
		else:
			nameFile=l.strip()
			
			insert_file=photoFile(id=numrows_photoFile,id_path=num_id_path,filename=nameFile)
			
			select_file=__init__.dbsession.query(photoFile.id_path,photoFile.filename).filter(photoFile.filename==nameFile).all()
			if select_file is None:
				
				__init__.dbsession.add(insert_file)	
			else:
				for id_path,filename in select_path:
					if (id_path==num_id_path and filename==nameFile):
						break
		
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
	

	

	
