import mcpi.minecraft as minecraft
import mcpi.block as block
import time

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()

# relative co-ordinate system
# find a clear field before running this program :)
# ----- h1
# |   |
# |   |
# |   |
# v1  v2

# build v1
mc.setBlock(pos.x, pos.y, pos.z+2, block.STONE.id)
mc.setBlock(pos.x, pos.y+1, pos.z+2, block.STONE.id)
mc.setBlock(pos.x, pos.y+2, pos.z+2, block.STONE.id)
mc.setBlock(pos.x, pos.y+3, pos.z+2, block.STONE.id)
mc.setBlock(pos.x, pos.y+4, pos.z+2, block.STONE.id)

# build v2
mc.setBlock(pos.x+4, pos.y, pos.z+2, block.STONE.id)
mc.setBlock(pos.x+4, pos.y+1, pos.z+2, block.STONE.id)
mc.setBlock(pos.x+4, pos.y+2, pos.z+2, block.STONE.id)
mc.setBlock(pos.x+4, pos.y+3, pos.z+2, block.STONE.id)
mc.setBlock(pos.x+4, pos.y+4, pos.z+2, block.STONE.id)

# build h1
mc.setBlock(pos.x+1, pos.y+4, pos.z+2, block.STONE.id)
mc.setBlock(pos.x+2, pos.y+4, pos.z+2, block.STONE.id)
mc.setBlock(pos.x+3, pos.y+4, pos.z+2, block.STONE.id)


