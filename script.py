import bpy

context = bpy.context
scene = context.scene

#project trackers onto the mesh
def AddDepth(depthObj):
    for tracker in bpy.data.objects:
        if tracker.type == 'EMPTY':
            bpy.context.view_layer.objects.active = tracker
            bpy.context.object.constraints["Follow Track"].depth_object = bpy.data.objects[depthObj]

#Create bones where trackers are projected                 
def AddBones():
    for tracker in bpy.data.objects:
        if tracker.type == 'EMPTY':
            bpy.context.view_layer.objects.active = tracker
            bpy.ops.object.armature_add(enter_editmode=False, 
                                              location=tracker.matrix_world.translation)

#Lock bone positions to corresponding trackers
def LockBoneLocations():
    pose = bpy.context.object.pose
    bones = pose.bones

    for i in range(len(bones)):
        trackName = "Track."+str(i).zfill(3)
        boneName = "Bone."+str(i).zfill(3)
        
        print("now locking " + boneName + " to " + trackName + "...", end='')
        
        if trackName in bpy.data.objects and boneName in bones:
            nc = bones[boneName].constraints.new(type="COPY_LOCATION")
            nc.target = bpy.data.objects[trackName]
            print("success!")
        else:
            print("failed. " + trackName + " does not exist.")


def SetBoneInfluence(_influence):
    pose = bpy.context.object.pose
    bones = pose.bones

    for i in range(len(bones)):
        boneName = "Bone."+str(i).zfill(3)
        
        if boneName in bones:
            bones[boneName].constraints["Copy Location"].influence = _influence
          
AddDepth("DepthMap")  
AddBones()
LockBoneLocations()
SetBoneInfluence(0.8)
