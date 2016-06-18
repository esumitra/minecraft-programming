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
mc.postToChat("Hello kids")
time.sleep(1)
