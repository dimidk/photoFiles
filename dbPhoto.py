#!/usr/bin/python
#-*- coding: utf-8 -*-


from sqlalchemy.orm import mapper,sessionmaker
from sqlalchemy import Table,Column, Integer, String,ForeignKey,create_engine,MetaData,PrimaryKeyConstraint
from sqlalchemy.exc import *
import __init__

exitStatus=0
try:
	
	photoDirs_table=Table('photoDirs',__init__.meta,autoload=True)
	photoDirs=[c.name for c in photoDirs_table.columns]
	"""print(photoDirs)"""

	photoFile_table=Table('photoFile',__init__.meta,autoload=True)
	photoFile=[c.name for c in photoFile_table.columns]
	"""print(photoFile)"""

except:
	exitStatus=-1
	pass


if (exitStatus==-1):
	photodir_table=Table('photoDirs',__init__.meta, 
			Column('id', String(10), primary_key=True), 
			Column('pathname', String(150,collation='utf8_general_ci'))
		       )
	photofile_table=Table('photoFile',__init__.meta,
			Column('id', Integer, primary_key=True),
			Column('id_path', String(10), ForeignKey('photoDirs.id'), nullable=False, primary_key=True),
			Column('filename', String(150, collation='utf8_general_ci'))					
			)
	__init__.meta.create_all()


class photoDir(object):
	def __init__(self, id, pathname):
		self.id=id
		self.pathname=pathname

class photoFile(object):
	def __init__(self, id, id_path, filename):
		self.id=id
		self.id_path=id_path
		self.filename=filename



if (exitStatus==-1):
	mapper(photoDir,photodir_table)
	mapper(photoFile,photofile_table)
else:
	mapper(photoDir,photoDirs_table)
	mapper(photoFile,photoFile_table)




