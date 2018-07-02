from subprocess import call
import os

def main_menu(menu):
	if menu[0]=='#':
		if menu[1]=='0':
			print("\n1-- json_creation.py:	Create a JSONL file of all the peer-reviewed research articles downloaded from the ERIC database.\n2-- triplet_extraction.py:	Create triplets of (subject, relation, object) using JSONL file created in previous step.\n3-- word2vec.py:	Build a Word2Vec model while creating word vectors of all words present in the corpus.\n4-- initial_seed_list_creation.py:	Create a dictionary of seed words that will be used to create the seed tree in the next step.\n5-- seed_tree.py:	Create a list of possible nodes of the network and a corresponding synonym dictionary which will be used to map the triplets produced using 'triplet_extraction.py'.\n6-- relation_mapping.py:	Create a dictionary of mapped relation words.\n7-- triplet_mapping_alt.py:	Create a mapped node or relation for each of the (subject, relation, object) of a triplet.\n8-- json_graph.py:	Create JSON files which will be used as input for the front end of the network.\n\n")
		elif menu[1]=='1':	print("\n1-- json_creation.py:	Create a JSONL file of all the peer-reviewed research articles downloaded from the ERIC database.\n\n")
		elif menu[1]=='2':	print("\n2-- triplet_extraction.py:	Create triplets of (subject, relation, object) using JSONL file created in previous step.\n\n")
		elif menu[1]=='3':	print("\n3-- word2vec.py:	Build a Word2Vec model while creating word vectors of all words present in the corpus.\n\n")
		elif menu[1]=='4':	print("\n4-- initial_seed_list_creation.py:	Create a dictionary of seed words that will be used to create the seed tree in the next step.\n\n")
		elif menu[1]=='5':	print("\n5-- seed_tree.py:	Create a list of possible nodes of the network and a corresponding synonym dictionary which will be used to map the triplets produced using 'triplet_extraction.py'.\n\n")
		elif menu[1]=='6':	print("\n6-- relation_mapping.py:	Create a dictionary of mapped relation words.\n\n")
		elif menu[1]=='7':	print("\n7-- triplet_mapping_alt.py:	Create a mapped node or relation for each of the (subject, relation, object) of a triplet.\n\n")
		elif menu[1]=='8':	print("\n8-- json_graph.py:	Create JSON files which will be used as input for the front end of the network.\n\n")
		else:	print "\nEnter a valid response!\n\n"
		menu = raw_input("Which script to run?\n\n0-- Run all\n1-- json_creation.py\n2-- triplet_extraction.py\n3-- word2vec.py\n4-- initial_seed_list_creation.py\n5-- seed_tree.py\n6-- relation_mapping.py\n7-- triplet_mapping_alt.py\n8-- json_graph.py\n\nNOTE: Prefix the choice with '#' to read the description of the python script\n\nRESPONSE:	")
		main_menu(menu)

	elif (menu[0] in ['0','1','2','3','4','5','6','7','8']):
		if menu[0]=='0':
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/json_creation.py'])
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/triplet_extraction.py'])
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/word2vec.py'])
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/initial_seed_list_creation.py'])
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/seed_tree.py'])
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/relation_mapping.py'])
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/triplet_mapping_alt.py'])
			call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/json_graph.py'])
		elif menu[0]=='1':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/json_creation.py'])
		elif menu[0]=='2':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/triplet_extraction.py'])
		elif menu[0]=='3':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/word2vec.py'])
		elif menu[0]=='4':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/initial_seed_list_creation.py'])
		elif menu[0]=='5':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/seed_tree.py'])
		elif menu[0]=='6':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/relation_mapping.py'])
		elif menu[0]=='7':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/triplet_mapping_alt.py'])
		elif menu[0]=='8':	call(['python','/media/aabhaschauhan/Data/ERIC/Scripts/json_graph.py'])
		else:	
			menu = raw_input("Enter a valid response!\nWhich script to run?\n\n0-- Run all\n1-- json_creation.py\n2-- triplet_extraction.py\n3-- word2vec.py\n4-- initial_seed_list_creation.py\n5-- seed_tree.py\n6-- relation_mapping.py\n7-- triplet_mapping_alt.py\n8-- json_graph.py\n\nNOTE: Prefix the choice with '#' to read the description of the python script\n\nRESPONSE:	")
			main_menu(menu)

	else:
		menu = raw_input("Enter a valid response!\nWhich script to run?\n\n0-- Run all\n1-- json_creation.py\n2-- triplet_extraction.py\n3-- word2vec.py\n4-- initial_seed_list_creation.py\n5-- seed_tree.py\n6-- relation_mapping.py\n7-- triplet_mapping_alt.py\n8-- json_graph.py\n\nNOTE: Prefix the choice with '#' to read the description of the python script\n\nRESPONSE:	")
		main_menu(menu)

print "\nWELCOME TO THE EDNODE BACKEND INTERFACE!\n\n"

menu = raw_input("Which script to run?\n\n0-- Run all\n1-- json_creation.py\n2-- triplet_extraction.py\n3-- word2vec.py\n4-- initial_seed_list_creation.py\n5-- seed_tree.py\n6-- relation_mapping.py\n7-- triplet_mapping_alt.py\n8-- json_graph.py\n\nNOTE: Prefix the choice with '#' to read the description of the python script\n\nRESPONSE:	")

main_menu(menu)
