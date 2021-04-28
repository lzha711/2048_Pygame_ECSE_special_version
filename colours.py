# this file becomes unnecessary for image version game

LIGHT_PINK = (255,228,228)
DARK_GREY = (96,96,96)
WHITE = (255,255,255)

LIGHT_GREY  = (224,224,224)
LIGHT_YELLOW = (255,255,153)
ORANGE = (255,128,0)
LIGHT_ORANGE = (255,153,51)
PINK = (255,153,153)
GREEN = (0,153,76)
BLACK = (0,0,0)
RED = (255, 0, 0)

# the following is unnecessary with the alternative method
colour_dict = {
	0:WHITE,
	2:LIGHT_GREY,
	4:LIGHT_YELLOW,
	8:ORANGE,
	16:LIGHT_ORANGE,
	32:PINK,
	64:PINK,
	128:ORANGE,
	256:LIGHT_ORANGE,
	512:ORANGE,
	1024:LIGHT_ORANGE,
	2048:GREEN
	}

def getColour(i):
	return colour_dict[i]