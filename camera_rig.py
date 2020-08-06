import pymel.core as pm
import re


def config_cam():
    scene = pm.sceneName()
    pat = re.compile(r"(sq\d{4})\w\D{2}(\d{4})", re.IGNORECASE)
    cam = ''
    def cam_name(camera_in):
        tr, cam = camera_in[0], pm.PyNode(camera_in[0].getShape())
        print(cam)
        tr.rename(camera_name)
        cam.rename(camera_name + 'Shape')
        return tr, cam

    if not scene:
        pm.warning('Open animation scene!')
        camera_name = 'test_camera'
    else:
        res = pat.search(scene)
        if res:
            camera_name = '{}_sh{}'.format(*res.groups())
    
    try:
        sel = pm.ls(sl=1)
        if sel[0].getShape().nodeType() == 'camera':
            print('scenario 1')
            tr, cam = cam_name(sel)
    except IndexError:
        print('scenario 2')    
        tr, cam = cam_name(pm.camera())
        print(cam, camera_name)
    finally:
        if cam.nodeType() == 'camera':
            # camera settings
            cam.displayFilmGate.set(1)
            cam.displayResolution.set(1)
            cam.bestFitClippingPlanes.set(0)
            cam.nearClipPlane.set(0.5)
            cam.farClipPlane.set(8000)
            
            cam.verticalFilmAperture.set(1)
            cam.verticalFilmAperture.lock()
            cam.horizontalFilmAperture.set(1.85)
            cam.horizontalFilmAperture.lock()
            
            cam.filmFit.set(2)
            cam.overscan.set(1.25)
            # cam.overscan.lock()
            
            cam.displayGateMaskColor.set((0.0, 0.0, 0.0))
            cam.displayGateMaskOpacity.set(1.0)
        else:
            pm.warning('Select camera!')