### Script for import mocup characters and load character rig
### For questions and wishes, contact andreyeof@gmail.com

import maya.cmds as cmds
import os
import maya.mel as mel
import json

window = ''
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
path_pose_lib = r'Z:\PROJECTS\Detectives\SEASONS\S02\Characters\Studio_Library_Pers\Matevosyan\_Bind\Detectives'

 
def listRefObjects():
	list_refs_RN = []
	list_refs = []
	for ref_name in cmds.ls( rf=True ):
		for char_name in vocabulary_characters:
				if ref_name[:-2] == char_name:
					list_refs.append( ref_name[:-2] )
					list_refs_RN.append( ref_name )
	return( list_refs, list_refs_RN )

def importRefRigs(ref_list):
	for ref_name in ref_list:
		ref_path = 0
		if ref_name == 'ChihuahuaRN':
			print( '...Chihuahua no loaded' )
			continue
		try:
			ref_path = ( cmds.referenceQuery( ref_name, filename=True ) )
		except:
			path_char = ( path_character_rig + "\\" + vocabulary_characters[ref_name[:-2]] + "\\" + "9_SkM" + "\\" + "SkM_" + ref_name[:-2] + '.ma')
			cmds.file(path_char, r=True, type="mayaAscii", namespace=ref_name[:-2], loadReferenceDepth="all", ignoreVersion=True)
			print('...load rig = %s' %ref_name )
		if ref_path:
			if 'SkM_' in ( ref_path.split('/')[-1].split('.')[0] ):
				continue
			else:
				print( 'else' )
			

def importReference(list_refs):
	for ref_name in list_refs:
		ref_path = ( cmds.referenceQuery( ref_name, filename=True ) )
		if ref_name == '...ChihuahuaRN no loaded':
			continue
		if ( ref_path.split('/')[-1].split('.')[0].split('_')[0] ) == 'SkM':
			print( '...%s is already loaded reference' %( ref_name ) )
			continue
		cmds.file(referenceNode=ref_name , ir=True)
		print('...load reference character = %s' %ref_name)

def bindPose(arg):
	for char_name in arg:
		cmds.currentTime( -1 )
		path_pose_lib_char = r'%s\%s.pose\pose.json' %( path_pose_lib, char_name)
		if char_name == 'Chihuahua':
			continue
		with open( path_pose_lib_char, 'r' ) as read_file:
			data_pose = json.load( read_file )
			for name_joint in data_pose['objects']:
				for attr in data_pose['objects'][name_joint]['attrs']:
					val = data_pose['objects'][name_joint]['attrs'][attr]['value']
					name_attr = ( '%s.%s' %(name_joint, attr) )
					type_attr = cmds.getAttr( name_attr, type=True )
					if ( 
						type_attr == "doubleLinear" or 
						type_attr == "doubleAngle" or 
						type_attr == "double" or
						type_attr == "bool" 
						):
						cmds.setAttr('%s.%s' %(name_joint, attr), float(val) )
					else:
						cmds.setAttr('%s.%s' %(name_joint, attr), str(val), type='string' )
		print( '...set bindpose => ', char_name )
		cmds.select(char_name + ':UnrealRoot')
		cmds.select(hi=True)
		cmds.SetKeyAnimated( an=True )

def MainWindow():
	window = cmds.window(title="Import Characters", widthHeight=(200, 150), s=False)
	form = cmds.formLayout(numberOfDivisions=100)
	bt1 = cmds.button(label='Start', h= 18, command=primeProgram, bgc=(0.5,0.3,0.3) )
	bEnd = cmds.button(label="Close", h= 100, command=('cmds.deleteUI(\"' + window + '\", window=True)'), bgc=(0.3,0.5,0.3) )
	cmds.formLayout( form, edit=True, attachForm=[
		(bt1, "top", 10),
		(bt1, "left", 10),
		(bt1, "right", 10),	
		(bEnd, "left", 10), 
		(bEnd, "top", 40), 
		(bEnd, "right", 10)]
		)
	cmds.showWindow(window)

def primeProgram(*arg):
	char_mocap_list = listRefObjects()
	importReference( char_mocap_list[1] )
	importRefRigs( char_mocap_list[1] )
	bindPose( char_mocap_list[0] )