import bpy
import bmesh
import re
import math
import os

def get_variable(line):
    key, value = re.split(r'\s+', line.strip())
    if(len(value.split(".")) > 1):
        infos[key] = float(value)
    else:
        infos[key] = int(value)

def create_verts(y, line, bm):
    if(y % invert_res != 0):
        return
    scale = 1 / 1000
    values = re.split(r'\s+', line.strip())
    for x in range(infos['ncols']):
        if(x % invert_res != 0):
            continue
        value = float(values[x])
        vert = [0, 0, -1]
        vert[0] = (infos['xllcorner'] + x * infos['cellsize']) * scale
        vert[1] = (infos['yllcorner'] - y * infos['cellsize']) * scale
        if(value != infos['NODATA_value']):
            vert[2] = value * scale
        bm.verts.new((vert[0], vert[1], vert[2]))

def create_faces(bm):
    nbRow = math.ceil(infos['nrows'] / invert_res)
    nbCol = math.ceil(infos['ncols'] / invert_res)
    for y in range(nbRow - 1):
        for x in range(nbCol - 1):
            bm.faces.new([
                bm.verts[x + nbCol *  y],
                bm.verts[x + nbCol *  y + 1],
                bm.verts[x + nbCol * (y + 1) + 1],
                bm.verts[x + nbCol * (y + 1)]])

def get_side_verts(i):
    m = { "top": [], "right": [], "bottom": [], "left": [] }
    nbRow  = math.ceil(infos["nrows"] / invert_res)
    nbCol  = math.ceil(infos["ncols"] / invert_res)
    size = nbRow * nbCol
    for x in range(nbCol):
        m["top"].append(x + i * size)
        m["bottom"].append(x + (nbRow - 1) * nbCol + i * size)
    for y in range(nbRow):
        m["left"].append(y * nbCol + i * size)
        m["right"].append(y * nbCol + nbCol - 1 + i * size)
    return m

def get_neighbor(x, y):
    return meshes.get(str(x) + "_" + str(y), None)

def create_bottom_face(x, y, current, bm):
    neighbor = get_neighbor(x, y)
    if(neighbor != None):
        size = len(current["bottom"])
        for i in range(size - 1):
            bm.faces.new([
                bm.verts[current["bottom"][i]],
                bm.verts[current["bottom"][i + 1]],
                bm.verts[neighbor["top"][i + 1]],
                bm.verts[neighbor["top"][i]]])
                
def create_left_face(x, y, current, bm):
    neighbor = get_neighbor(x, y)
    if(neighbor != None):
        size = len(current["left"])
        for i in range(size - 1):
            bm.faces.new([
                bm.verts[current["left"][i]],
                bm.verts[current["left"][i + 1]],
                bm.verts[neighbor["right"][i + 1]],
                bm.verts[neighbor["right"][i]]])
                
def create_bottom_left_face(x, y, step, current, bm):
    l  = get_neighbor(x - step, y       )
    b  = get_neighbor(x       , y - step)
    bl = get_neighbor(x - step, y - step)
    if(l != None and b != None and bl != None):
        bm.faces.new([
            bm.verts[l["right"][len(l["right"]) - 1]],
            bm.verts[current["bottom"][0]],
            bm.verts[b["top"][0]],
            bm.verts[bl["right"][0]]])

def create_missing_faces(obj):
    step = infos["cellsize"] * infos['ncols']
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    for name, value in meshes.items():
        x_str, y_str = name.split("_")
        x = float(x_str)
        y = float(y_str)
        create_left_face(x - step, y, value, bm)
        create_bottom_face(x, y - step, value, bm)
        create_bottom_left_face(x, y, step, value, bm)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()

def merge_objects(obj_1, obj_2):
    if(previous == None):
        return
    bpy.context.view_layer.objects.active = obj_1
    obj_1.select_set(True)
    obj_2.select_set(True)
    bpy.ops.object.join()

def create_object(i):
    mesh = bpy.data.meshes.new("Mesh")
    obj =  bpy.data.objects.new("Object", mesh)
    bm = bmesh.new()
    bm.from_mesh(mesh)

    with open(folder + "/" + filenames[i], "r") as file:
        for index, line in enumerate(file, 1):
            if(index < 7):
                get_variable(line)
            else: 
                create_verts(index - 7, line, bm)
    bm.verts.ensure_lookup_table()
    create_faces(bm)
    bm.to_mesh(mesh)
    bm.free()
    bpy.context.collection.objects.link(obj)
    return obj

folder = "path/to/datas"
invert_res = 59
previous = None
filenames = sorted(os.listdir(folder))
size = len(filenames)
meshes = {}
print("\033c", end="")
infos = {
        "ncols"       : 0,
        "nrows"       : 0, 
        "xllcorner"   : 0,
        "yllcorner"   : 0,
        "cellsize"    : 0,
        "NODATA_value": 0}

for i in range(size - 1, -1, -1):
    current = create_object(i)
    name = str(infos["xllcorner"]) + "_" + str(infos["yllcorner"])
    meshes[name] = get_side_verts(i)
    if(previous != None):
        bpy.context.view_layer.objects.active = current
        current.select_set(True)
        previous.select_set(True)
        bpy.ops.object.join()
    previous = current

create_missing_faces(previous)
