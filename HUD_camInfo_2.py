import maya.cmds as mc

def CamName():
    stlTemp = mc.ls(sl=True)
    mc.select(all=True)
    list = mc.ls(sl=True)
    mc.select(cl=True)
    for i in list:
        name = i.split(":")
        if name[len(name)-1] == "cameraMain":
            selName = i
    if stlTemp:
        mc.select(selName)
    return selName

def textCam():
    ep = mc.getAttr(CamName() + ".ep")
    sc = mc.getAttr(CamName() + ".sc")
    qf = mc.getAttr(CamName() + ".Quantity Frame")
    name = "sq" + str(ep) + "   sh" + str(sc) + "     " + str(qf)+ "frm"
    return name

def CreateHud():
    obj_attr = ""
    if mc.ls(sl=True):
        obj_attr = '%s.Text_Info' % mc.ls(sl=True)[0]
        if mc.getAttr(obj_attr)==0:
            if mc.headsUpDisplay("HUD_KA1", ex=True) == True:
                mc.headsUpDisplay("HUD_KA1", rem=True)
        elif mc.getAttr(obj_attr)==1:
            mc.headsUpDisplay(
                "HUD_KA1",
                section=7,
                block=7,
                lfs = "large",
                dfs = "large",
                label="",
                command="textCam()",
                event="timeChanged",
                nodeChanges="attributeChange")


if mc.headsUpDisplay("HUD_KA1", ex=True) == True:
    mc.headsUpDisplay("HUD_KA1", rem=True)

mc.scriptJob(attributeChange=[CamName()+'.Text_Info', CreateHud])