######################################################
#
#    Mirror.py   
#
#    Blender 3D Game Engine
#
#    Tutorial for using Mirror.py can be found at www.tutorialsforblender3d.com
#
######################################################

# import bge module
import bge

# get the current controller
controller = bge.logic.getCurrentController()

# get object script is attached to
obj = controller.owner

# check to see variable Mirror has been created
if "Mirror" in obj:
				
	# update the mirror
	obj["Mirror"].refresh(True)

# if variable Mirror hasn't been created
else:

	# get current scene
	scene = bge.logic.getCurrentScene()

	# get the mirror material ID
	matID = bge.texture.materialID(obj, "MA" + obj['material'])

	# get the active camera
	cam = scene.active_camera 
					
	# use texture channel 1
	texChannel = 0

	# get the mirrortexture
	mirror = bge.texture.Texture(obj, matID, texChannel)
	
	# get the mirror source
	mirror.source = bge.texture.ImageMirror(scene, cam, obj, matID)

	# save mirror as an object variable
	obj["Mirror"] = mirror
	