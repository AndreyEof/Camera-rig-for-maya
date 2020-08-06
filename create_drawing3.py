import maya.cmds as mc
import sys
import maya.OpenMaya as om

def createShader(filePath):
	# create shader 
	shadName = mc.shadingNode('lambert', asShader=True)
	SG1 = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shadName + 'SG'))
	mc.connectAttr( (shadName + '.outColor'), (SG1 + '.surfaceShader'), f=True,)
	shadFileName = mc.shadingNode('file', asTexture=True, isColorManaged=True)
	pl_2d_tex = mc.shadingNode('place2dTexture', asUtility=True, isColorManaged=True)
	mc.connectAttr((pl_2d_tex +  ".coverage"), (shadFileName + ".coverage"), f=True)
	mc.connectAttr((pl_2d_tex + ".translateFrame"), (shadFileName + ".translateFrame"), f=True)
	mc.connectAttr((pl_2d_tex + ".rotateFrame"), (shadFileName + ".rotateFrame"), f=True)
	mc.connectAttr((pl_2d_tex + ".mirrorU"), (shadFileName + ".mirrorU"), f=True)
	mc.connectAttr((pl_2d_tex + ".mirrorV"), (shadFileName + ".mirrorV"), f=True)
	mc.connectAttr((pl_2d_tex + ".stagger"), (shadFileName + ".stagger"), f=True)
	mc.connectAttr((pl_2d_tex + ".wrapU"), (shadFileName + ".wrapU"), f=True)
	mc.connectAttr((pl_2d_tex + ".wrapV"), (shadFileName + ".wrapV"), f=True)
	mc.connectAttr((pl_2d_tex + ".repeatUV"), (shadFileName + ".repeatUV"), f=True)
	mc.connectAttr((pl_2d_tex + ".offset"), (shadFileName + ".offset"), f=True)
	mc.connectAttr((pl_2d_tex + ".rotateUV"), (shadFileName + ".rotateUV"), f=True)
	mc.connectAttr((pl_2d_tex + ".noiseUV"), (shadFileName + ".noiseUV"), f=True)
	mc.connectAttr((pl_2d_tex + ".vertexUvOne"), (shadFileName + ".vertexUvOne"), f=True)
	mc.connectAttr((pl_2d_tex + ".vertexUvTwo"), (shadFileName + ".vertexUvTwo"), f=True)
	mc.connectAttr((pl_2d_tex + ".vertexUvThree"), (shadFileName + ".vertexUvThree"), f=True)
	mc.connectAttr((pl_2d_tex + ".vertexCameraOne"), (shadFileName + ".vertexCameraOne"), f=True)
	mc.connectAttr((pl_2d_tex + ".outUV"), (shadFileName + ".uv"), f=True)
	mc.connectAttr((pl_2d_tex + ".outUvFilterSize"), (shadFileName + ".uvFilterSize"), f=True)
	mc.defaultNavigation(connectToExisting=True, source=shadFileName, destination=(shadName + ".color"), force=True)
	mc.setAttr(shadFileName + '.fileTextureName', filePath[0], type="string")
	size = sizeImages(filePath[0])
	planeName = createPlane(size)
	mc.sets( e=True, forceElement=shadName + 'SG')
	CreateUV(planeName[0])

def CreateUV(planeName):
	print "plane name =", planeName
	mc.select(planeName, r=True)
	mc.hilite(planeName) 
	mc.selectMode(component=True)
	mc.select((planeName + '.f[0]'), r=True)
	UV = mc.polyProjection((planeName + '.f[0]'), ch=0, type='Planar', ibd=True, kir=False, md='y')
	print "++++", UV
	mc.selectMode (object=True)

def createPlane(size):
	planeName = mc.polyPlane( w=size[0], h=size[1], sx=1, sy=1, ax=[0, 1, 0], cuv=2, ch=0 )
	return planeName
# Get image size
def sizeImages(path):
    img = om.MImage()
    img.readFromFile(path)
    
    util = om.MScriptUtil()
    widthUtil = om.MScriptUtil()
    heightUtil = om.MScriptUtil()
    
    widthPtr = widthUtil.asUintPtr()
    heightPtr = heightUtil.asUintPtr()
    
    img.getSize(widthPtr, heightPtr)
    
    width = util.getUint(widthPtr)
    height = util.getUint(heightPtr)
    print "===", (width, height)
    return (width, height)

def Path():
	try:
		OpenFile = open('c:\\temp\\path_for_plugin_in_maya.txt', 'r')
		path_file = OpenFile.read()
		OpenFile.close()
		if (path_file != True): print "none path"
	except:
		path_file = "none path"
	return (path_file)

def btf1(*args):
	filename = mc.fileDialog2(fileMode=1, caption="Import Image")
	createShader(filename)

def MainWindow():
	window = mc.window(title="Select file texture", iconName="SelFile", widthHeight=(440, 120), s=False)
	form = mc.formLayout(numberOfDivisions=100)
	bt1 = mc.button(label='Select Images', h= 30, command=btf1)
	bEnd = mc.button(label="Close", h= 30, command=('mc.deleteUI(\"' + window + '\", window=True)') )
	mc.formLayout( form, edit=True, attachForm=[
		(bt1, "top", 20),
		(bt1, "left", 10),
		(bt1, "right", 10),	
		(bEnd, "left", 10), 
		(bEnd, "top", 70), 
		(bEnd, "right", 10)]
		)
	mc.showWindow(window)