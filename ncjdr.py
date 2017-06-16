#Importing library and changing name to libtcod
import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

#Map values

MAP_WIDTH = 80
MAP_HEIGHT = 45

#Uses list comprehension

def make_map():
	global map

	map = [[ Tile(False)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]

	map[30][22].blocked = True
	map[30][22].block_sight = True
	map[50][22].blocked = True
	map[50][22].block_sight = True


#Walls

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

#Renders Objects
def render_all():
	global color_light_wall
	global color_light_ground

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			wall = map[x][y].block_sight
			if wall:
				libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
			else:
				libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
	#draw all objects in list (objects variable)
	for object in objects:
		object.draw()
	#blit the contents of "con" to the root console
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


#Map Tile Class
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
		if not map[self.x + dx][self.y + dy].blocked:
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
	key = libtcod.console_wait_for_keypress(True) #This line makes the game wait until the player presses a key. Rendering it turn-based.
	#Checks for pressed keys and then changes the player coordinates on either 'x' or 'y' axis.
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		player.move(0, -1)
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0, 1)
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1, 0)
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1, 0)
	#ALT+Enter: toggle fullscreen
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return True #exit game

#TURN BASED GAMES USE console_check_for_keypress
#Draw stuff before handling key input so that the game doesn't load with a blank screen.

####Initialization


player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
objects = [npc, player]
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#Starts the window (Last parameter decides if fullscreen or not
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT,) #Creates another off-screen terminal window (Used for GUI menus)


#Call make_map function
make_map()
#MAIN LOOP - Keeps running game logic so long as window is not closed.

while not libtcod.console_is_window_closed():

	#render at the screen
	render_all()

	libtcod.console_flush() #Forces the terminal to print changes to the screen at the end of the main loop.

	#erase all objects at old location, before moving.
	for object in objects:
		object.clear()

	exit = handle_keys()
	if exit:
		break



