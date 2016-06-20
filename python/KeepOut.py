# os specific code
import sys
if sys.platform == 'darwin':
    from mc import *
    mc = Minecraft()
else:
    from mcpi.minecraft import *
    mc = Minecraft.create()
# end os specific code
import time

# geo-fence
# orientation of player and fence should be aligned with axes
# moving right = increasing X
# moving down = increasing Z
FENCE_LEFT_X = 97
FENCE_TOP_Z = -526
FENCE_RIGHT_X = 104
FENCE_BOTTOM_Z = -518
HOME_X = FENCE_LEFT_X - 5
HOME_Z = FENCE_TOP_Z
HOME_Y = 1
inFence = 0

def isInFence(x,y,z):
    if (FENCE_LEFT_X < x and x < FENCE_RIGHT_X and
        FENCE_TOP_Z < z and z < FENCE_BOTTOM_Z):
        return True
    else:
        return False

while True:
    time.sleep(3)
    pos = mc.player.getTilePos()
    # print("x = " + str(pos.x) + " z = " + str(pos.z))
    if (isInFence(pos.x,pos.y,pos.z) == True):
        mc.postToChat("Tresspassing! Please leave.")
        inFence = inFence + 1
        
    if (inFence > 3):
        inFence = 0
        mc.postToChat("Ejecting ...")
        mc.player.setPos(HOME_X, HOME_Y, HOME_Z)


