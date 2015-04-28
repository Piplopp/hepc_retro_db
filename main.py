#!/usr/bin/python
# -*- coding: utf-8 -*-

#@author: Jerome PIVERT
#@date: 17/03/2014

#General imports
import os, sys		#magic import for magical and usefull functions
import argparse		#parser

#Project imports
import hepc_python as hp

#MAIN FUNCTION
def main():



	"""
	MAIN FUNCTION !
	"""
	
	
	
	#PARSER
	parser = argparse.ArgumentParser(usage="./%(prog)s [-h] [-i] [-p] [-d] [-o] [-f] [-g]\n", description="Projet de BDD M1 Rennes, gestion simple de la BDD hepc_retro")
	parser.add_argument("-i", "--identifiant",
		help="Nom de la protein a chercher pour executer vos requetes",
		default="Hepcidin",
		type=str
	)
	parser.add_argument("-p", "--proteinAssoc",
		help="Requete pour recuperer les proteines associees a une proteine id specifiee",
		action="store_true"
	)
	parser.add_argument("-d", "--diseaseAssoc",
		help="Requete pour recuperer les maladies associees a une protein id specifiee",
		action="store_true"
	)
	parser.add_argument("-o", "--occurence",
		help="Requete pour recupere le background d une proteine id specifiee",
		action="store_true"
	)
	parser.add_argument("-f", "--frequence",
		help="Requete pour recupere le background de publication d une proteine id specifiee",
		action="store_true"
	)
	parser.add_argument("-g", "--graph",
		help="Pour genere le graphique d interaction avec une proteine specifiee",
		action="store_true"
	)
	args = vars(parser.parse_args())
	
	
	#INIT DATABASE
	PATH_project = os.getcwd()
	PATH_rawData = PATH_project+"/data/*"
	
	
	if(hp.exists("hepc_retro.sq3")):
		print(hp.bcolors.WARNING + "BDD already exists" + hp.bcolors.ENDC)
	else:
		hp.initDatabase("hepc_retro.sq3", PATH_project)
	
	
	
	#DO SOME STUFF
	if args["proteinAssoc"]:
		print("Processing request "+hp.bcolors.OKBLUE+"getProtAssoc(...)"+hp.bcolors.ENDC+" ...")
		hp.getProtAssoc("hepc_retro.sq3", PATH_project, args["identifiant"])
		print(hp.bcolors.OKGREEN+"request successfully done"+hp.bcolors.ENDC)
	if args["diseaseAssoc"]:
		print("Processing request "+hp.bcolors.OKBLUE+"getDiseaseAssoc(...)"+hp.bcolors.ENDC+" ...")
		hp.getDiseaseAssoc("hepc_retro.sq3", PATH_project, args["identifiant"])
		print(hp.bcolors.OKGREEN+"request successfully done"+hp.bcolors.ENDC)
	if args["occurence"]:
		print("Processing request "+hp.bcolors.OKBLUE+"getOccurMoreThanOnceProt(...)"+hp.bcolors.ENDC+" ...")
		hp.getOccurMoreThanOnceProt("hepc_retro.sq3", PATH_project, args["identifiant"])
		print(hp.bcolors.OKGREEN+"request successfully done"+hp.bcolors.ENDC)
	if args["frequence"]:
		print("Processing request "+hp.bcolors.OKBLUE+"getPublicBackground(...)"+hp.bcolors.ENDC+" ...")
		hp.getPublicBackground("hepc_retro.sq3", PATH_project, args["identifiant"])
		print(hp.bcolors.OKGREEN+"request successfully done"+hp.bcolors.ENDC)
	if args["graph"]:
		print("Processing request "+hp.bcolors.OKBLUE+"displayProteinAssociation(...)"+hp.bcolors.ENDC+" ...")
		hp.displayProteinAssociation("hepc_retro.sq3", PATH_project, args["identifiant"])
		print(hp.bcolors.OKGREEN+"request successfully done"+hp.bcolors.ENDC)	
main()
