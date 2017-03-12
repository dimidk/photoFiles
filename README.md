# photoFiles
find duplicates photo files and import a database with unique photo files. 
__init__.py file creates database or check if database exists using sqlalchemy database toolkit.
dbPhoto.py file connect to database and maps the tables to classes. 
findDupFiles.py file searches the root photo directory recursively to find duplicate files based on content. When 
a photo is double or triple or more inserted only once in database.
