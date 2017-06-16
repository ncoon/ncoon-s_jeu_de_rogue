#Importing library and changing name to libtcod
import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

#Map values

MAP_WIDTH = 80
MAP_HEIGHT = 45

#Walls

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

class Tile:
	#a map tile and it's properties
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked

		if block_sight is None:
			block_sight = blocked
		self.block_sight = block_sight

class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color

	def move(self, dx, dy):
	#move by the given amount
		self.x += dx
		self.y += dy

	def draw(self):
        #set the color and then draw the character that represents this object at its position
		libtcod.console_set_default_foreground(con, self.color)
		libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self):
        #erase the character that represents this object
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def handle_keys():
	global playerx, playery
	key = libtcod.console_wait_for_keypress(True) #This line makes the game wait until the player presses a key. Rendering it turn-based.
	#Checks for pressed keys and then changes the player coordinates on either 'x' or 'y' axis.
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		playery -= 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		playery += 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		playerx -= 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		playerx += 1
	#ALT+Enter: toggle fullscreen
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return True #exit game

#TURN BASED GAMES USE console_check_for_keypress
#Draw stuff before handling key input so that the game doesn't load with a blank screen.

#Initialization

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
object = [npc, player]
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#Starts the window (Last parameter decides if fullscreen or not
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT,) #Creates another off-screen terminal window (Used for GUI menus)

#Sets player coordinates to the center of the screen
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2


#MAIN LOOP - Keeps running game logic so long as window is not closed.
while not libtcod.console_is_window_closed():

	for object in objects:
		objects.draw()


	libtcod.console_set_default_foreground(con, libtcod.white) #Sets the text color in game, 0 dictates the terminal window printed to.
	libtcod.console_put_char(con, playerx, playery, '@', libtcod.BKGND_NONE) #Prints character '@' to coordinates 'playerx,playery' (Middle of the terminal window). The first 0 indicates the terminal window, once again. 
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	libtcod.console_flush() #Forces the terminal to print changes to the screen at the end of the main loop.

	for object in objects:
		objects.clear()
	libtcod.console_put_char(con, playerx, playery, ' ', libtcod.BKGND_NONE) #Clears the last character position on the screen.

	exit = handle_keys()
	if exit:
		break



