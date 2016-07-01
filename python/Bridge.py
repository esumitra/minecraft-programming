import mcpi.minecraft as minecraft
import mcpi.block as block
import time

mc = minecraft.Minecraft.create()

def isSafe(my_pos):
    b = mc.getBlock(my_pos.x, my_pos.y-1, my_pos.z)
    if b == block.AIR.id or b == block.WATER_STATIONARY.id or b == block.WATER_FLOWING.id:
        return False
    else:
        return True

while True:
    time.sleep(0.1)
    pos = mc.player.getTilePos()
    if  not isSafe(pos):
        # mc.postToChat("not safe")
        mc.setBlock(pos.x, pos.y-1, pos.z, block.GLASS.id)

    
