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

Solids = {}

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
    transformFn = lambda p: map(sum,zip(p,base)) # translate to current pos
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

# non-Platonic solids
Solids["PYRAMID"] = {"v": np.array([  [0,1,0],
                                      [-1,0,1],
                                      [-1,0,-1],
                                      [1,0,-1],
                                      [1,0,1]]),
                     "f": np.array([ [0,1,2],
                                     [0,2,3],
                                     [0,3,4],
                                     [0,1,4],
                                     [1,2,3,4]])}


