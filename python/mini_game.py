# Minecraft mini game
from __future__ import print_function
import sys
sys.path.append('/Users/esumitra/workspaces/mc/mcpipy')
sys.path.append('/Users/esumitra/workspaces/python/minecraft-programming/python')
import minecraftstuff as minecraftstuff
import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import threading
import numpy as np
import copy
import itertools
import scipy.spatial.distance as sd

# -----------------
# Shape definitions
# -----------------
phi = 1.618
Solids = {}

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

Solids["DODECAHEDRON"] = {"v": np.array([
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
                                 [0,-1.0/phi,-phi]
                                ]),
                  "f": np.array([[0,1,2,3,4],
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
                                 [13,14,19,18,17]
                                ])}

Solids["ICOSAHEDRON"] = {"v": np.array([
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
                                [2,8,3]
                                ])}

# ---------------
# shape functions
# ---------------
def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

# functions for detecting edges
def distanceIndices(dist_elem):
    keyFn = lambda x: x[0]
    giter2ListFn = lambda x: (x[0],list(x[1]))
    grouped_lists = map(giter2ListFn, itertools.groupby(sorted(list(itertools.izip(dist_elem,itertools.count(0))), key = keyFn), key = keyFn))
    indexFn = lambda x: x[1]
    # 1st item is distance from point to itself = 0
    # 2nd item is points with minimal distance
    # tuple._1 = distance
    # tuple._2 = (distance,point index) tuple
    return map(indexFn,grouped_lists[1][1])

def edgeVectors(vs):
    distance_matrix = np.round(sd.squareform(sd.pdist(vs, 'euclidean')),decimals=2)
    dist_groups = [distanceIndices(point_data) for point_data in distance_matrix]
    return dist_groups

# functions and definitions to draw Platonic Solids
def facePoints2Vec(fp, coordsFn):
    return reduce(lambda acc,p: acc + [coordsFn(p[0],p[1],p[2])],fp,[])

# return a list of shapes given vertex points and 
# number of points/face for platonic solid
def shapesFromPoints(v, facePoints, transformFn, coordsFn):
    return [facePoints2Vec(map(lambda i: transformFn(v[i]), fp),coordsFn) 
            for fp in facePoints]

# jupyter REPL functions
# replOriginFn = lambda: [0,0,0]
# drawFn = lambda f,bid: print(f)
# replCoordsFn = lambda x,y,z: (x,y,z)
# drawGame("CUBE", 8, [45],87,replOriginFn,replDrawFn,replDrawFn,replCoordsFn)
def drawGame(shape,length=8,
             blockList=[block.GOLD_ORE.id, block.COAL_ORE.id,block.REDSTONE_ORE.id],
             vertexBlock=block.GLOWING_OBSIDIAN.id,
             originFn = lambda: map(sum,zip(list(mc.player.getTilePos()),[0,25,0])),
             drawFaceFn = lambda face,blockId: mcdrawing.drawFace(face, True, blockId),
             drawVertexFn = lambda (x,y,z), blockId: mc.setBlock(x,y,z,blockId),
             coordsFn = lambda x,y,z: minecraft.Vec3(x,y,z)):
    base = originFn()
    v = length * Solids[shape]["v"]
    f = Solids[shape]["f"]
    transformFn = lambda p: map(compose(int,sum),zip(p,base)) # translate to current pos, ints needed
    faces = shapesFromPoints(v,f,transformFn, coordsFn)
    blocks = itertools.cycle(blockList)
    # draw faces
    for face in faces:
        blockId = blocks.next()
        drawFaceFn(face, blockId)
    # draw vertices
    vertices = map(transformFn, v)
    for vertex in vertices:
        drawVertexFn(vertex,vertexBlock)
    return {"faces":faces, 
            "vertices":vertices,
            "edges":edgeVectors(vertices),
            "vertexBlock":vertexBlock}

def drawPaths(points, blockId = block.TNT.id):
    pointPairs = list(itertools.izip(points,points[1:]))
    for ppair in pointPairs:
        (x1,y1,z1) = ppair[0]
        (x2,y2,z2) = ppair[1]
        mcdrawing.drawLine(x1,y1,z1,x2,y2,z2,blockId,1)

# ------------------------
# game mechanics functions
# ------------------------
 
# returns True if a vertex is hit
def isVertexHit(vs,hit_coords):
    return hit_coords in vs

def isConnected(edges, pindex1,pindex2):
    connected_points = edges[pindex1]
    return pindex2 in connected_points

def onVertexHit(gdata,hit_coords):
    vindex = gdata["vertices"].index(hit_coords)
    path = gdata["path"]
    if (path != []):
        prev_v = gdata["vertices"][path[-1]]
        current_v = gdata["vertices"][vindex]
        if isConnected(gdata["edges"],vindex, path[-1]):
            # add vertex to path
            if vindex not in path:
                mc.postToChat("You scored a hit!")
                mcdrawing.drawLine(prev_v[0],prev_v[1],prev_v[2],current_v[0],current_v[1],current_v[2],gdata["vertexBlock"])
                path.append(vindex)
    else:
        mc.postToChat("You scored a hit!")
        # add vertex to path
        path.append(vindex)
    print(path)

def isLevelComplete(gdata):
    if gdata["path"] == []:
        return False
    vindexes = range(len(gdata["vertices"]))
    for i in vindexes:
        if i not in gdata["path"]:
            return False
    return True

def onLevelComplete(gdata):
    mc.postToChat("Congratulations! You completed the level.")
    time.sleep(1)
    path_points = [gdata["vertices"][vindex] for vindex in gdata["path"]]
    drawPaths(path_points)

# TODO: parameterize event poll function and provide a REPL poller for testing
def runGame(gdata):
    gdata["game_state"] = [0] * len(gdata["vertices"])
    gdata["path"] = []
    while not isLevelComplete(gdata):
        time.sleep(0.2)
        for hitBlock in mc.events.pollBlockHits():
            hit_coords = [hitBlock.pos.x,hitBlock.pos.y,hitBlock.pos.z]
            if isVertexHit(gdata["vertices"],hit_coords):
                onVertexHit(gdata,hit_coords)
    onLevelComplete(gdata)

# in Jupyter REPL
# mc = minecraft.Minecraft.create()
# mcdrawing = minecraftstuff.MinecraftDrawing(mc)
# drawpos = copy.deepcopy(mc.player.getTilePos())
# mc.player.setTilePos(drawpos.x, drawpos.y, drawpos.z)
# gdata = drawGame("CUBE", 8, [block.GLASS.id],block.GLOWING_OBSIDIAN.id)
# drawGame("TETRAHEDRON", 8, [block.AIR.id],block.AIR.id)
# gdata = drawGame("TETRAHEDRON")
# runGame(gdata)

# module minecraft objects
mc = minecraft.Minecraft.create()
mcdrawing = minecraftstuff.MinecraftDrawing(mc)

# --------------------------------------
# class encapsulating data and functions
# --------------------------------------

class ShapeGame(object):
    def __init__(self,shape):
        self.gdata = drawGame(shape)
        self.gdata["is_running"] = False
        self.run_thread = None

    def startGame(self):
        self.gdata["is_running"] = True
        #self.run_thread = threading.Thread(target = runGame, args = (self.gdata,))
        #self.run_thread.start()
        #self.run_thread.join()
        runGame(self.gdata)

    def stopGame(self):
        self.gdata["is_running"] = False
