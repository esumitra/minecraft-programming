# Python functions for drawing
import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import minecraftstuff as minecraftstuff
import numpy as np

# Circles and Spheres
# requires mc and mcdrawing to be defined as follows
# TODO: pass in mc and make drawings a class that is initialized with mc created in notebook
mc = minecraft.Minecraft.create()
mcdrawing = minecraftstuff.MinecraftDrawing(mc)

# functions and variables/constants
phi = 1.618
Solids = {}
def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

# circle drawing functions
def drawMyCircle(radius=5,blockId=block.WOOD.id):
    pos = mc.player.getTilePos()
    mcdrawing.drawCircle(pos.x,
                         pos.y+25,
                         pos.z,
                         radius,
                         blockId)

def drawMySphere(radius=5,blockId=block.WOOD.id):
    pos = mc.player.getTilePos()
    mcdrawing.drawSphere(pos.x, 
                         pos.y + 25, 
                         pos.z, 
                         radius, 
                         blockId)

def drawMyHollowSphere(radius=5,blockId=block.WOOD.id):
    pos = mc.player.getTilePos()
    mcdrawing.drawHollowSphere(pos.x, 
                               pos.y + 25, 
                               pos.z, 
                               radius, 
                               blockId)

# drawMyCircle()
# drawMyCircle(9)
# drawMyCircle(13,block.DIAMOND_BLOCK.id)


# Platonic Solids
def facePoints2Vec(fp):
    return reduce(lambda acc,p: acc + [minecraft.Vec3(p[0],p[1],p[2])],fp,[])

# return a list of shapes given vertex points and 
# number of points/face for platonic solid
def shapesFromPoints(v, facePoints, transformFn = lambda x: x):
    return [facePoints2Vec(map(lambda i: transformFn(v[i]), fp)) for fp in facePoints]


# TODO
# calculate number of edges and verify
# Eulers theorem before processing to avoid drawing errors
# V - E + F = 2
# for a jupyter repl, define the following:
# from __future__ import print_function
# replOriginFn = lambda: [0,0,0]
# replDrawFn = lambda f,bid: print(f)
# drawSolid("PYRAMID", 5, block.WOOD.id, replOriginFn, replDrawFn)
def drawSolid(shape,length=5,blockId=block.DIAMOND_BLOCK.id,
             originFn = lambda: map(sum,zip(list(mc.player.getTilePos()),[0,25,0])),
              drawFn = lambda f,bid: mcdrawing.drawFace(f, True, bid)):
    base = originFn()
    v = length * Solids[shape]["v"]
    f = Solids[shape]["f"]
    transformFn = lambda p: map(compose(int,sum),zip(p,base)) # translate to current pos
    faces = shapesFromPoints(v,f,transformFn)
    
    # draw or print solid coordinates
    for face in faces:
        drawFn(face, blockId)

def drawShape(shape,length=5,blockId=block.DIAMOND_BLOCK.id,
             originFn = lambda: map(sum,zip(list(mc.player.getTilePos()),[0,25,0])),
              drawFn = lambda f,bid: mcdrawing.drawFace(f, False, bid)):
    base = originFn()
    v = length * Solids[shape]["v"]
    f = Solids[shape]["f"]
    transformFn = lambda p: map(compose(int,sum),zip(p,base)) # translate to current pos, ints needed?
    faces = shapesFromPoints(v,f,transformFn)
    
    # draw or print solid coordinates
    for face in faces:
        drawFn(face, blockId)


# Platonic Solids definitions
# v = vertices, f = faces
Solids["TETRAHEDRON"] = {"v": np.array([  [1,1,1],
                                          [1,-1,-1],
                                          [-1,1,-1],
                                          [-1,-1,1]]),
                         "f": np.array([[0,1,2],
                                        [0,1,3],
                                        [0,2,3],
                                        [1,2,3]])}

Solids["OCTAHEDRON"] = {"v": np.array([[1,0,0],
                                       [0,1,0],
                                       [-1,0,0],
                                       [0,-1,0],
                                       [0,0,1],
                                       [0,0,-1]]),
                         "f": np.array([[0,1,4],
                                        [1,2,4],
                                        [2,3,4],
                                        [3,0,4],
                                        [0,1,5],
                                        [1,2,5],
                                        [2,3,5],
                                        [3,0,5]])}

Solids["CUBE"] = {"v": np.array([[1,1,1],
                                 [1,1,-1],
                                 [1,-1,-1],
                                 [1,-1,1],
                                 [-1,1,1],
                                 [-1,1,-1],
                                 [-1,-1,-1],
                                 [-1,-1,1]]),
                  "f": np.array([[0,1,2,3],
                                 [0,3,7,4],
                                 [4,5,6,7],
                                 [1,2,6,5],
                                 [2,3,7,6],
                                 [0,1,5,4]])}

Solids["DODECAHEDRON"] = {
    "v": np.array([
        [0,1.0/phi,phi],
        [1,1,1],
        [phi,0,1.0/phi],
        [1,-1,1],
        [0,-1.0/phi,phi],
        [-1,-1,1],
        [-1.0/phi,-phi,0],
        [1.0/phi,-phi,0],
        [1,-1,-1],
        [phi,0,-1.0/phi],
        [1,1,-1],
        [1.0/phi,phi,0],
        [-1.0/phi,phi,0],
        [-1,1,-1],
        [0,1.0/phi,-phi],
        [-1,1,1],
        [-phi,0,1.0/phi],
        [-phi,0,-1.0/phi],
        [-1,-1,-1],
        [0,-1.0/phi,-phi]]),
    "f": np.array([
        [0,1,2,3,4],
        [4,5,6,7,3],
        [2,3,7,8,9],
        [0,1,11,12,15],
        [1,2,9,10,11],
        [8,9,10,14,19],
        [0,4,5,16,15],
        [5,6,18,17,16],
        [6,7,8,19,18],
        [10,11,12,13,14],
        [12,13,17,16,15],
        [13,14,19,18,17]])}

Solids["ICOSAHEDRON"] = {
    "v": np.array([
        [0,-phi,1],
        [phi,-1,0],
        [1,0,phi],
        [-1,0,phi],
        [-phi,-1,0],
        [0,-phi,-1],
        [1,0,-phi],
        [phi,1,0],
        [0,phi,1],
        [-phi,1,0],
        [-1,0,-phi],
        [0,phi,-1]]),
    "f": np.array([
        [0,1,2],
        [0,2,3],
        [0,3,4],
        [0,4,5],
        [0,5,1],
        [11,8,9],
        [11,9,10],
        [11,10,6],
        [11,6,7],
        [11,7,8],
        [8,3,9],
        [9,3,4],
        [9,4,10],
        [4,5,10],
        [10,5,6],
        [5,6,1],
        [1,6,7],
        [1,7,2],
        [2,7,8],
        [2,8,3]])}


# non-Platonic solids
Solids["PYRAMID"] = {
    "v": np.array([
        [0,1,0],
        [-1,0,1],
        [-1,0,-1],
        [1,0,-1],
        [1,0,1]]),
    "f": np.array([
        [0,1,2],
        [0,2,3],
        [0,3,4],
        [0,1,4],
        [1,2,3,4]])}


