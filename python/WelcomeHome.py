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

pos = mc.player.getTilePos()
print(pos.x)
print(pos.y)
print(pos.z)

# posting the position on run
'''
positionMessage = "x = " + str(pos.x) + " y = " + str(pos.y)  + " z = " + str(pos.z)
print(positionMessage)
mc.postToChat(positionMessage)
'''

# continuously display the position using a game loop
'''
while True:
    time.sleep(1)
    pos = mc.player.getTilePos()
    positionMessage = "x = " + str(pos.x) + " y = " + str(pos.y)  + " z = " + str(pos.z)
    mc.postToChat(positionMessage)
'''

# magic carpet tile - welcome home
'''
homeX = 145
homeZ = -514
while True:
    time.sleep(1)
    pos = mc.player.getTilePos()
    print("x = " + str(pos.x) + " z = " + str(pos.z))
    if (pos.x == homeX and pos.z == homeZ):
        mc.postToChat("welcome home")


'''
