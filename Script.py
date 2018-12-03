import os
import bpy
import csv
import mathutils
import math

directory = bpy.path.abspath("//")

print(directory)

models = []
mtls = []
textures = []
placementCSVs = []
tilePlacementCSV = None

tilename = "lordaeronscenario"

masterscale = 0.01

tilesize = 533.333

for filename in os.listdir(directory):
    if filename.endswith(".obj"):
        models.append(filename) 
        print("OBJ: " + filename)
        
    elif filename.endswith(".mtl"):
        mtls.append(filename)
        print("MTL: " + filename)
        
    elif filename.endswith(".png"):
        textures.append(filename)
        print("PNG: " + filename)
        
    elif "ModelPlacementInformation.csv" in filename:
        if tilename in filename:
            tilePlacementCSV = filename
            
        else:
            placementCSVs.append(filename)
            print("CSV: " + filename)
            continue
    else:
        print("Not needed file: " + filename)

# import tile

for model in models:
    if tilename in model:
        fp = os.path.join(directory, model)
        imported_object = bpy.ops.import_scene.obj(filepath = fp)
        obj_object = bpy.context.selected_objects[0]
        obj_object.scale = (masterscale, masterscale, masterscale)
        obj_object.rotation_mode = 'XYZ'
        obj_object.location += mathutils.Vector((-32 * tilesize * masterscale, 32 * tilesize * masterscale, 0))

# open the tile csv
reader = csv.reader(open(os.path.join(directory, tilePlacementCSV)), delimiter = ";")

i = 0
for row in reader:
    # skip the first row
    if i == 0:
        i = i + 1
        continue
    else:
        i = i + 1
    
    # amount of objects that should be loaded
    if i > 40:
        break
    
    print("ROW: " + str(row))
    
    modelname = str(row[0])
    posX = float(row[1]) * masterscale
    posY = float(row[2]) * masterscale
    posZ = float(row[3]) * masterscale
    rotX = float(row[4])
    rotY = float(row[5])
    rotZ = float(row[6])
    scale = float(row[7]) * masterscale

    # TODO: check if object already is in the scene
    
    for model in models:
        if modelname in model:
            obj = model
        else:
            continue
    
    fp = os.path.join(directory, obj)
    
    imported_object = bpy.ops.import_scene.obj(filepath = fp)
    
    for obj in bpy.context.selected_objects:
        obj.scale = (scale, scale, scale)
        obj.rotation_mode = 'XYZ'
        obj.rotation_euler = (0, 0, math.radians(180))
        obj.location = mathutils.Vector((-posX, posZ, posY))
        obj.rotation_mode = 'XYZ'
        obj.rotation_euler = (math.radians(rotX + 90), math.radians(rotZ), math.radians(rotY - 90))

print(i)
