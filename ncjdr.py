#Importing library and changing name to libtcod
import libtcodpy as libtcod

#Game window values
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

#Map values
MAP_WIDTH = 80
MAP_HEIGHT = 45

#Room values
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3

#Player's Field of View
FOV_ALGO = 0 #defaulf FOV algorithm included in libtcod
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

#Walls/Ground coloring using libtcod's included library
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

#Checks if a tile is blocked or not
def is_blocked(x, y):
	#first test the map tiles
	if map[x][y].blocked:
		return True
	#now check for any blocking objects
	for object in objects:
		if object.blocks and object.x == x and object.y == y:
			return True
	return False

#Creates monsters, etc and places then in rooms
def place_objects(room):
		#choose random number of monsters
		num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

		for i in range(num_monsters):
			#choose random spot for this monster
			x = libtcod.random_get_int(0, room.x1, room.x2)
			y = libtcod.random_get_int(0, room.y1, room.y2)

			#chances: 20% monster A, 40% monster B, 10% monster C, 30% monster D
			choice = libtcod.random_get_int(0, 0, 100)
			if choice < 20:
				#create human
				monster = Object(x, y, 'h', libtcod.desaturated_green)
			elif choice < 20+40:
				#create a kobold
				monster = Object(x, y, 'k', libtcod.dark_orange)
			elif choice < 20+40+10:
				#create troll
				monster = Object(x, y, 'T', libtcod.darker_green)
			else:
				#create orc
				monster = Object(x, y, 'o', libtcod.desaturated_green)
			objects.append(monster)

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

	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)

	def intersect(self, other):
		#returns true if this rectangle connects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
			self.y1 <= other.y2 and self.y2 >= other.y1)

#Map Tile Class
class Tile:
	#a map tile and it's properties
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		self.explored = False
		if block_sight is None:
			block_sight = blocked
		self.block_sight = block_sight

class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
	def __init__(self, x, y, char, name, color, blocks=False):
		self.name = name
		self.blocks = blocks
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
		#only show if it's visible to the player        
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			#set the color and then draw the character that represents this object at its position
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self):
        #erase the character that represents this object #Clears the space where the character walks
		libtcod.console_put_char(con, self.x, self.y, '.', libtcod.BKGND_NONE)

def handle_keys():
	global fov_recompute
	key = libtcod.console_wait_for_keypress(True) #This line makes the game wait until the player presses a key. Rendering it turn-based.
	#Checks for pressed keys and then changes the player coordinates on either 'x' or 'y' axis.
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		player.move(0, -1)
		fov_recompute = True
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0, 1)
		fov_recompute = True
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1, 0)
		fov_recompute = True
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1, 0)
		fov_recompute = True
	#ALT+Enter: toggle fullscreen
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return True #exit game
#TURN BASED GAMES USE console_check_for_keypress
#Draw stuff before handling key input so that the game doesn't load with a blank screen.


#Uses list comprehension
def make_map():
	global map, player

	map = [[ Tile(True)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]

	rooms = []
	num_rooms = 0

	for r in range(MAX_ROOMS): #Random width and height
		w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#Random position without going out of the boundaries of the map.
		x = libtcod.random_get_int(0, 0, MAP_WIDTH - w -1)
		y = libtcod.random_get_int(0, 0, MAP_HEIGHT -h -1)

		#"Rect" class makes rectangles easier to work with
		new_room = Rect(x, y, w, h)

		#Run through room and see if it intersects with others
		failed = False

		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
		if not failed:
			#This means there are no intersections, so this room is valid
			#paint it to the map's tiles
			create_room(new_room)
			#center coordinates of new room, will be used later.
			(new_x, new_y) = new_room.center()

			if num_rooms == 0:
				#This is the first room. Player starts here
				player.x = new_x
				player.y = new_y

			else:
				#all rooms after the first:
				#connect it to the previous room with a tunnel

				#center coordinates of the previous room
				(prev_x, prev_y) = rooms[num_rooms -1].center()

				#draw a coin (random number that is either 1 or 0)
				if libtcod.random_get_int(0, 0, 1) == 1:
					#first move horizontally, then vertically
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, prev_x)
				else:
					#first move vertically, then horizontally
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, prev_y)
			#adds monsters, etc to the room
			place_objects(new_room)
			#finally, append to the new room list
			rooms.append(new_room)
			num_rooms += 1

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

#Renders Objects
def render_all():
	global fov_map, color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground
	global fov_recompute

	if fov_recompute:
		#recompute FOV if needed (player moved, etc)
		fov_recompute = False
		libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)


		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				wall = map[x][y].block_sight
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				if not visible:
					#if not visible now, player can only see if it's explored
					if map[x][y].explored:
					#it's out of player's FOV
						if wall:
							libtcod.console_put_char_ex(con, x, y, '#', color_dark_wall, libtcod.black)
						else:
							libtcod.console_put_char_ex(con, x, y, '.', color_dark_ground, libtcod.black)
				else:	
					if wall: #it's visible
						libtcod.console_put_char_ex(con, x, y, '#', color_light_wall, libtcod.black)
					else:
						libtcod.console_put_char_ex(con, x, y, '.', color_light_ground, libtcod.black )
					map[x][y].explored = True #Thanks to this, explored regions are visible on screen,
							#but in a different color than what is in FOV

	#draw all objects in list (objects variable)
	for object in objects:
			object.draw()
	#blit the contents of "con" to the root console
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

####Initialization############################


player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
objects = [player]
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#Starts the window (Last parameter decides if fullscreen or not
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT,) #Creates another off-screen terminal window (Used for GUI menus)


#Call make_map function
make_map()

#Tells libtcod's FOV module which tiles block sight
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

fov_recompute = True

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



