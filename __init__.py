#!/usr/bin/python
#-*- coding: utf-8 -*-


from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import *
import passwd


dbDict={'user':passwd.userName,'password':passwd.password,'host':passwd.hostName}
dbUrlFormat='mysql+mysqlconnector://{user}:{password}@{host}/{database}'
dbUrlDefault=(dbUrlFormat.format(database='mysql',**dbDict))
dbUrlNew=(dbUrlFormat.format(database=passwd.newDB,**dbDict))

def connectDB():
	exitdb={}
	try:
		engine=create_engine(dbUrlNew,encoding='utf8',echo=True)
		conn=engine.connect()
		exitdb['engine']=engine
		exitdb['exitcode']=0

	except ProgrammingError:
		print("Database doesn't exist")
		exitdb['engine']=engine
		exitdb['exitcode']=-1

	return exitdb

def createDB():
	try:
		engine=create_engine(dbUrlDefault,encoding='utf8',echo=True)
		conn=engine.connect() 
		conn.execute("COMMIT")
		conn.execute("CREATE DATABASE %s" % passwd.newDB)
		conn.execute("COMMIT")
		conn.close()
		
	except ProgrammingError:
		print("User doesn't have privileges")
	


exitDict=connectDB()
exitStatus=exitDict['exitcode']

if (exitStatus==0):
	print("Connect to database")
	engine=exitDict['engine']

else:
	print("create new database")
	createDB()
	exitDict=connectDB()
	engine=exitDict['engine']
	meta=MetaData(bind=engine)
	Session=scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
	dbsession=Session()

meta=MetaData(bind=engine)
Session=scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
dbsession=Session()



