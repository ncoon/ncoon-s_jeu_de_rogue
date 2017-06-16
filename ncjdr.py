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

	map = [[ Tile(True)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]

	room1 = Rect(20, 15, 10, 15)
	room2 = Rect(20, 15, 10, 15)
	create_room(room1)
	create_room(room2)
	player.x = 25
	player.y = 23
	create_h_tunnel(25, 55, 23)
#	create_v_tunnel(25, 55, 23)

#Create tunnels Vertically and Horizontally
def create_h_tunnel(x1, x2, y):
	global map
	for x in range(min(x1, x2), max(x1, x2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
def create_v_tunnel(y1, y2, x):
	global map
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].block = False
		map[x][y].block_sight = False


#Walls
color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

#Renders Objects
def render_all():
	global color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			wall = map[x][y].block_sight
			if wall:
				libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.black)
			else:
				libtcod.console_put_char_ex(con, x, y, '.', libtcod.grey, libtcod.black )
	#draw all objects in list (objects variable)
	for object in objects:
		object.draw()
	#blit the contents of "con" to the root console
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

#Clears the space where the character walks
def clear(self):
	if libtcod.map_is_in_fov(fov_map, self.x, self.y):
		libtcod.console_put_char_ex(con, self.x, self.y, '.', libtcod.grey, libtcod.dark_blue)

#Create Rooms
def create_room(room):
	global map
	#go through the tiles in rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2): #Makes it so that two rooms will never overlap (Always have a space in between)
			map[x][y].blocked = False
			map[x][y].block_sight = False 

#Rectangles on the map
class Rect:
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h


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



