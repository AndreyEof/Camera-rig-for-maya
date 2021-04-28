### Script for import mocup characters and load character rig
### For questions and wishes, contact andreyeof@gmail.com

import maya.cmds as cmds
import os

path_character_rig = r'Z:\PROJECTS\Detectives\SEASONS\S02\Characters'
vocabulary_characters = { 
					'Bee':'Bee', 
					'Bella':'Bella', 
					'Carl':'Carl', 
					'Chihuahua':'Chihuahua', 
					'Chink':'Chink', 
					'Elly':'Elly', 
					'Erick':'Hedgehog Erick', 
					'Jam':'Hedgehog Jam', 
					'Sam':'Hedgehog Sam', 
					'Vika':'Hedgehog Vika', 
					'Lucy':'Lucy', 
					'Mary':'Mary', 
					'Nick':'Nick', 
					'Nina':'Nina', 
					'Phill':'Phil', 
					'Sofy':'Sofy' 
					}

def listRefObjects():
	list_refs_RN = []
	list_refs = []
	for ref_name in cmds.ls( rf=True ):
		for char_name in vocabulary_characters:
				if ref_name[:-2] == char_name:
					list_refs.append( ref_name[:-2] )
					list_refs_RN.append( ref_name )
	return( list_refs, list_refs_RN )

def importRefRigs(arg):
	for ref_name in arg:
		path_char = ( path_character_rig + "\\" + vocabulary_characters[ref_name] + "\\" + "9_SkM" + "\\" + "SkM_" + ref_name + '.ma')
		cmds.file(path_char, r=True, type="mayaAscii", namespace=ref_name, loadReferenceDepth="all", ignoreVersion=True)
		print('...load = ', ref_name )

def importReference(list_refs):
	for ref_name in list_refs:
		print("Import: ", ref_name )
		cmds.file(referenceNode=ref_name , ir=True)

def main():
	char_mocap_list = listRefObjects()
	importReference( char_mocap_list[1] )
	importRefRigs( char_mocap_list[0] )

main()

cmds.ungroup("ANIMATION")