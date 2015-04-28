#!/usr/bin/python3
# -*- coding: utf-8 -*-

#@author: Jerome PIVERT
#@date: 17/03/2014

#@resume: class for colors (ASCII code) used for coloring terminal output such as print
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


import sqlite3				# for the DB
import sys, os				# magical import for magical and usefull functions
import glob				# BEST MODULE EVER.
import csv
from collections import defaultdict
import networkx as nx			# graph interaction
import matplotlib.pyplot as plt		# plot plot plotipiplot

#################
# Miscellaneous #
#################

#CHECK IF DB FILE EXISTS
def exists(path):
	return os.path.isfile(path)

#OPEN AND CLOSE CONNECTION TO DB
def connection(path):
	"""Return the connection and the cursor for doing
	some stuff in the db
	path -String- absolute PATH of your db
	"""
	db = path #open 'database'
	return sqlite3.connect(db), sqlite3.connect(db).cursor() #connect to current database
def closeConnection(cursor, connection):
	"""Close the connection of the db to stop doing
	some stuff
	cursor -Object- cursor to close
	connection -Object- connection to close
	"""
	cursor.close()
	connection.close()


###############
# DB creation #
###############

#INIT AND FILL DATABASE WITH RAW_DATA FILES
def initDatabase(databaseName, path):



	"""Create the database, you need to specify the name of your base and the path for your data
	databaseName -String- name of your db
	path -String- path to your project
	"""
	
	
	
	connect, cursor = connection(path+"/"+databaseName)
	#cursor = connect.cursor() #creates a cursor, this allow me to cancel my actions until I commit

	dirname = path+"/data/*"
	for i in glob.iglob(dirname):
		tname = os.path.splitext(os.path.basename(i))[0]
		print("Processing FILE " + bcolors.HEADER + os.path.basename(i) + bcolors.ENDC + " ...")
		cursor.execute("CREATE TABLE IF NOT EXISTS " + tname + """(
				SourceId VARCHAR(10),
				SourceLabel VARCHAR(250),
				SourceEntityType VARCHAR(1),
				EdgeLabel VARCHAR(250),
				TargetId VARCHAR(250),
				TargetLabel VARCHAR(250),
				TargetEntityType VARCHAR(1),
				PUBMED_ID VARCHAR(8),
				nsent INT,
				ntagged_nsent INT,
				nsent_nrelation INT,
				Period VARCHAR(10))"""
		)
		#fill TABLES
		with open(i, "r") as f:
			f = csv.DictReader(f, delimiter="\t")
			for row in f:
				insertstr = "INSERT INTO " +tname+ " VALUES(" + "\"" +row["SourceId"]+ "\"" + "," + "\"" +row["SourceLabel"]+ "\"" + "," + "\"" +row["SourceEntityType"]+ "\"" + "," + "\"" +row["EdgeLabel"]+ "\"" + "," + "\"" +row["TargetId"]+ "\"" + "," + "\"" +row["TargetLabel"]+ "\"" + "," + "\"" +row["TargetEntityType"]+ "\"" + "," + "\"" +row["PUBMED_ID"]+ "\"" + "," +row["nsent"]+ "," +row["ntagged_nsent"]+ "," +row["nsent_nrelation"]+ "," + "\"" +row["period"]+ "\""")"
				cursor.execute(insertstr)


	#Force new empty table for some tests
	cursor.execute("CREATE TABLE IF NOT EXISTS events_0000""""(
				SourceId VARCHAR(10),
				SourceLabel VARCHAR(250),
				SourceEntityType VARCHAR(1),
				EdgeLabel VARCHAR(250),
				TargetId VARCHAR(250),
				TargetLabel VARCHAR(250),
				TargetEntityType VARCHAR(1),
				PUBMED_ID VARCHAR(8),
				nsent INT,
				ntagged_nsent INT,
				nsent_nrelation INT,
				Period VARCHAR(10))"""
	)
	
	print(bcolors.OKGREEN + "success" + bcolors.ENDC)
	connect.commit()
	closeConnection(cursor, connect)




#####################
# PUBLIC FUNCTIONS  #
#####################

#BESOIN 1
def getProtAssoc(databaseName, path, idProt="Hepcidin"):



	"""Return the associated protein to the idProt and thus by year
	databaseName -String- name of the file wich contains the db
	path -String- PATH where the db file is located
	idProt -String- name of the protein to look for assoc, default is Hepcdidin
	"""
	
	
	
	connect, cursor = connection(path+"/"+databaseName)
	#cursor = connect.cursor()
	
	#PRINT SOME INFORMATIONS
	print("SQL: SELECT DISTINCT LOWER(TargetLabel) FROM "+bcolors.HEADER+"tname"+bcolors.ENDC+" WHERE LOWER(SourceLabel) LIKE LOWER(\"%"+bcolors.HEADER+idProt+bcolors.ENDC+"%\") AND LOWER(TargetEntityType)=LOWER(\"p\") ORDER BY Period")
	print("ProtID querry: "+bcolors.HEADER+idProt+bcolors.ENDC)
	
	#DO THE MATHS
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name") #get all tables names
	for ttuples in cursor.fetchall():
		tname = ttuples[0]
		print("Searching assoc in " +bcolors.HEADER+tname+bcolors.ENDC+ " ...")

		sqlstr = "SELECT DISTINCT LOWER(TargetLabel) FROM " +tname+ " WHERE LOWER(SourceLabel) LIKE LOWER(\"%"+idProt+"%\") AND LOWER(TargetEntityType)=LOWER(\"p\") ORDER BY Period"
		cursor.execute(sqlstr)

		#FILE WRITING
		with open(path+"/requestResult/"+idProt+"_protAssoc_"+tname+".txt", "w") as f:
			for elements in cursor.fetchall():
				f.write(elements[0]+"\n")

	connect.commit()
	closeConnection(cursor, connect)


#BESOIN 2
def getDiseaseAssoc(databaseName, path, idProt="Hepcidin"):



	"""Return the associated disease to the idProt and thus by year
	databaseName -String- name of the file wich contains the db
	path -String- PATH to where the db file is located
	idProt -String- name of the protein to look for assoc, default is Hepcdidin
	"""
	
	
	
	connect, cursor = connection(path+"/"+databaseName)
	#cursor = connect.cursor()
	
	#PRINT SOME INFORMATIONS
	print("SQL: SELECT DISTINCT LOWER(TargetLabel) FROM "+bcolors.HEADER+"tname"+bcolors.ENDC+" WHERE LOWER(SourceLabel) LIKE LOWER(\"%"+bcolors.HEADER+idProt+bcolors.ENDC+"%\") AND LOWER(SourceEntityType)=LOWER(\"p\") AND LOWER(TargetEntityType)=LOWER(\"i\")")
	print("ProtID querry: "+bcolors.HEADER+idProt+bcolors.ENDC)
	
	#DO THE MATHS
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
	for ttuples in cursor.fetchall():
		tname = ttuples[0]
		print("Searching assoc in " +bcolors.HEADER+tname+bcolors.ENDC+ " ...")
		
		sqlstr = "SELECT DISTINCT LOWER(TargetLabel) FROM " +tname+ " WHERE LOWER(SourceLabel) LIKE LOWER(\"%"+idProt+"%\") AND LOWER(SourceEntityType)=LOWER(\"p\") AND LOWER(TargetEntityType)=LOWER(\"i\")"
		cursor.execute(sqlstr)
		
		#FILE WRITING
		with open(path+"/requestResult/"+idProt+"_diseaseAssoc_"+tname+".txt", "w") as f:
			for elements in cursor.fetchall():
				f.write(elements[0]+"\n")

	connect.commit()
	closeConnection(cursor, connect)


def getOccurMoreThanOnceProt(databaseName, path, idProt="Hepcidin"):


	"""Return the proteins that can were detected in
	at least 2 years and are associated with idProt protein
	databaseName -String- name of the file which contain the db
	path -String- PATH to where the db file is located
	idProt -String- name of the protein to look for occur, default is Hepcidin
	"""

	
	connect, cursor = connection(path+"/"+databaseName)

	#PRINT SOME INFORMATIONS
	print("SQL: SELECT DISTINCT LOWER(TargetLabel) FROM "+bcolors.HEADER+"tname"+bcolors.ENDC+" WHERE LOWER(SourceLabel) LIKE LOWER(\"%"+bcolors.HEADER+idProt+bcolors.ENDC+"%\") AND LOWER(TargetEntityType)=LOWER(\"p\") ORDER BY Period")
	print("ProtID querry: "+bcolors.HEADER+idProt+bcolors.ENDC)

	#DO THE MATHS
	redondant = defaultdict(lambda:int(0))
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
	for ttuples in cursor.fetchall():
		tname = ttuples[0]
		print("Searching assoc in " +bcolors.HEADER+tname+bcolors.ENDC+ " ...")
		sqlstr = "SELECT DISTINCT LOWER(TargetLabel) FROM " +tname+ " WHERE LOWER(SourceLabel) LIKE LOWER(\"%"+idProt+"%\") AND LOWER(TargetEntityType)=LOWER(\"p\") ORDER BY Period"
		cursor.execute(sqlstr)
		for i in cursor.fetchall():
			redondant[i[0]] += 1
		
	#FILE WRITING
	with open(path+"/requestResult/"+idProt+"_OccurMoreThanOnce.txt", "w") as f:
		for key in redondant:
			if(redondant[key] > 1):
				f.write(key+"\n")

	connect.commit()
	closeConnection(cursor, connect)


def getPublicBackground(databaseName, path, idProt="Hepcidin"):



	"""Returns the number of associated 
	databaseName -String- name of the file which contains the db
	path -String- PATH to where the db file is located
	idProt -String- name of the protein to look for publication background, default is Hepcidin
	"""	



	connect, cursor = connection(path+"/"+databaseName)

	#PRINT SOME INFORMATIONS
	print("SQL: NOPE, don't need specific SQL here")
	print("ProtID querry: "+bcolors.HEADER+idProt+bcolors.ENDC)

	#DO THE MATHS
	getOccurMoreThanOnceProt(databaseName, path, idProt)
	getProtAssoc(databaseName, path, idProt)

	background = set()
	with open(path+"/requestResult/"+idProt+"_OccurMoreThanOnce.txt", "r") as fbckgrd:
		for lines in fbckgrd:
			background.add(lines.strip())
	#Fill dict with all idProt associated protein by year
	for fprotAssoc in glob.iglob(path+"/requestResult/"+idProt+"_protAssoc*"):
		thisYear = set()
		with open(fprotAssoc, "r") as f:
			for lines in f:
				thisYear.add(lines.strip())
		intersect = thisYear.intersection(background) #present in both sets
				#FILE WRITING
		with open(path+"/requestResult/"+idProt+"_publiBackground.txt", "a+") as f:
			if(len(thisYear) > 0):
				f.write("Pour "+os.path.splitext(os.path.basename(fprotAssoc))[0]+" on retrouve un background de "+str(len(intersect))+" publications, soit "+str(float(len(intersect))*100.0/float(len(thisYear)))+"% des publications totales de cette annee\n")
			else:
				f.write("Pour "+os.path.splitext(os.path.basename(fprotAssoc))[0]+" on retrouve un background de "+str(len(intersect))+" publications, soit "+str(float(len(intersect))*100.0/float(1))+"% des publications totales de cette annee\n")

	connect.commit()
	closeConnection(cursor, connect)



#####################
# INTERACTION GRAPH #
#####################

def displayProteinAssociation(databaseName, path, idProt="Hepcidin"):



	"""Draw the interaction graph for the given protein
	databaseName -String- name of the DB file
	path -String- PATH to where the db file is located
	idProt -String- prot id to draw a graph of, default is Hepcidin
	"""
	
	
	
	#Generate and use the files to construct the datas
	datas = list(set())
	getProtAssoc(databaseName, path, idProt)
	for fprotAssoc in sorted(glob.iglob(path+"/requestResult/"+idProt+"_protAssoc*")):
		with open(fprotAssoc, "r") as f:
			tmpSet = set()
			for lines in f:
				tmpSet.add(lines.strip())
			datas.append(tmpSet)
	datas.pop(0) #dont need this one

	#Construct the graph
	year = 2001
	g = nx.Graph()
	g.add_node(idProt[0])
	for thisYear in datas:
		for this in thisYear:
			if this not in g.nodes():
				g.add_node(this)
				g.add_edge(this, idProt[0])
		plt.axis("off")
		plt.title(idProt+" associated protein in " +str(year)+ ": " +str(len(g.nodes()))+ " related proteins")
		nx.draw(g)
		plt.savefig(path+"/"+idProt+"interaction_graph_"+str(year)+".png")
		#plt.show()
		print(bcolors.OKGREEN+str(year)+": graph done; "+str(len(g.nodes()))+" proteins"+bcolors.ENDC)
		year+=1
