import maya.mel as mel
import maya.cmds as mc
import pymel.core.uitypes as ui;
import sys

# opredelyaem nomer shota
nameSce = mc.file(q=True,sn=True)
NS = nameSce.split('_')
for i in NS:
    if i[:2] == 'SH':
        numberCam = i
        break

# proverka model panel
chek_modelPanel = mc.getPanel(wf=True)

# obyavlyaem peremennie camer
persp = 'persp'
stereo = 'SCAM01_' + numberCam[2:] + ':camx_C_001_STCAShape'
#print "stereo " + stereo 

# opredelyaem imya aktivnoi cameri
try:
    active_panel = mc.getPanel(wf=True)
    active_camera = (ui.ModelPanel(active_panel)).getCamera()
    print active_camera
except:
    mc.confirmDialog(title='error', message='pleas select view', button=['OK'], dismissString='OK')
    sys.exit()

# uslovie
if active_camera == persp:
    mel.eval('lookThroughModelPanel ' + stereo + ' ' + chek_modelPanel)
elif active_camera == stereo:
    mel.eval('lookThroughModelPanel persp ' + chek_modelPanel) 
else:
    print 'error'