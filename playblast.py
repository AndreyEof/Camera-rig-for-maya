import maya.cmds as mc
import maya.mel as mel
import os
from pymel.core import *
import maya.OpenMaya as om
import maya.OpenMayaUI as omu

def SelMeshView():
    view = omu.M3dView.active3dView()
    om.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), om.MGlobal.kReplaceList)
    listGeo = mc.ls(sl=True)
    mc.select(cl=True)
    return listGeo

def HideInvisMesh():
    HideCam()
    max = mc.playbackOptions(q=True, max=True)
    count = 1
    arr_geo = []
    while(count < max):
        mc.currentTime(count)
        list = SelMeshView()
        for i in list:
            if i not in arr_geo:
                arr_geo.append(i)
        count += 5
    for i in arr_geo:
        mc.select(i, add=True)
    mc.HideUnselectedObjects()

def Smooth():
    listGeo = mc.ls(sl=True)
    mc.select(cl=True)
    for i in listGeo:
        vis = mc.getAttr(i + ".visibility")
        if vis == True:
            mc.select(i, r=True)
            countPol = polyEvaluate( f=True )
            countTre = polyEvaluate( t=True )
            if (countPol <= 10000) or (countTre <= 22000 ):
                mc.displaySmoothness(po=3)
                mc.select(cl=True)

def PrefName():
    listCam = mc.listCameras()
    prefName = ""
    for i in listCam:
        if "camera" in i:
            if ":" in i:    
                j = i.split(':')
                p = 0
                while p != len(j)-1:
                    prefName = prefName + j[p] + ":" 
                    p += 1
            elif "_" in i:
                j = i.split('_')
                p = 0
                while p != len(j)-1:
                    prefName = prefName + j[p] + "_"
                    p += 1
    return prefName

def HideCam():
    prefName = PrefName()
    mc.select(prefName + "camera", r=True)
    mc.hide()
    mc.select(cl=True)
    listCam = mc.listCameras()
    for i in listCam:
        mc.select(i, r=True)
        mc.hide()
        mc.select(cl=True)

def SinglePersp():
    panView = mel.eval('setNamedPanelLayout "Four View"; updateToolbox();')
    panView = mel.eval('setNamedPanelLayout "Single Perspective View"; updateToolbox();')
    perspPanel = mc.getPanel( withLabel='Persp View')

    mc.setAttr("hardwareRenderingGlobals.enableTextureMaxRes", 1)
    mc.setAttr("hardwareRenderingGlobals.textureMaxResolution", 512)
    mc.modelEditor(perspPanel, e=True, displayTextures=True)
    prefName = PrefName()
    mel.eval('lookThroughModelPanel ' + prefName + 'cameraShape ' + perspPanel)
    
    for elem  in  getPanel(typ="modelPanel"):
            mel.eval( 'setRendererInModelPanel  "ogsRenderer" '+ elem.name() )
    mel.eval('setAttr "hardwareRenderingGlobals.multiSampleEnable" 1;')
    mel.eval('setAttr "hardwareRenderingGlobals.ssaoEnable" 1;')

    mel.eval('modelEditor -e -nurbsCurves false ' + perspPanel)
    mel.eval('modelEditor -e -cameras false ' + perspPanel)
    mel.eval('modelEditor -e -joints false ' + perspPanel)
    mel.eval('modelEditor -e -ikHandles false ' + perspPanel)
    mel.eval('modelEditor -e -deformers false ' + perspPanel)
    mel.eval('modelEditor -e -follicles false ' + perspPanel)
    mel.eval('modelEditor -e -dynamicConstraints false ' + perspPanel)
    mel.eval('modelEditor -e -handles false ' + perspPanel)
    mel.eval('modelEditor -e -motionTrails false ' + perspPanel)
    mel.eval('modelEditor -e -locators false ' + perspPanel)
    mc.camera((prefName + "cameraShape"), e=True, displayFilmPivot=0, displayFilmOrigin=0, displaySafeAction=0, displaySafeTitle=0, displayFilmGate=0, displayResolution=0, overscan=1.0, displayGateMask=0)

    mel.eval('modelEditor -edit -displayAppearance smoothShaded -activeOnly false ' + perspPanel)
    mel.eval('DisplayWireframe; displaySmoothness -full;')
    mel.eval('modelEditor -edit -displayAppearance smoothShaded -activeOnly false ' + perspPanel)

    try:
        mel.eval('AEReloadAllTextures;')
    except:
        print ">>> Error: AEReloadAllTextures <<<"
    mel.eval('optionVar -intValue playblastOverrideViewport false; updatePlayblastMenus("playblastOverrideViewport","overrideViewportItemPB");')
    mc.modelEditor(perspPanel, e=True, udm=False)
    mc.modelEditor(perspPanel, e=True, lights=True)
    mc.modelEditor(perspPanel, e=True, polymeshes=True)


def MyPlayblast():
    prt = mc.getFileList(folder = path)
    nameSce = cmds.file(q=True, sn=True)
    nameSce = (os.path.split(nameSce)[1].split('.')[0])
    path_move = "P:\\AI\\s13\\animation\\color\\"
    mc.setAttr("defaultResolution.width", 1280)
    mc.setAttr("defaultResolution.height", 720)
    mc.playblast(format='qt',
    f=(path_move + nameSce +".mov"), 
    forceOverwrite=True, 
    sequenceTime=0, 
    clearCache=1, 
    viewer=0, 
    showOrnaments=1, 
    offScreen=True,
    fp=4, 
    percent=100, 
    compression="H.264", 
    quality=70, 
    widthHeight=[1280, 720])

def Sequence(name):
    
    mc.file(path + name, o=True, prompt=False, save=False, force=True)
    HideInvisMesh()
    Smooth()
    SinglePersp()
    MyPlayblast()


def Main():
    global path
    path = 'P:\\AI\\s13\\animation\\ma\\temp\\'
    prt = mc.getFileList(folder = path)
    for i in prt:
        name = i
        i = i.split('.')
        i = i[len(i)-1:]
        if i[0] == "ma":
            Sequence(name)
        else:
            print "=================== else ======================"