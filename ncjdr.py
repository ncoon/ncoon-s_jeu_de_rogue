#Importing library and changing name to libtcod
import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

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


libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#Starts the window (Last parameter decides if fullscreen or not
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)

#Sets player coordinates to the center of the screen
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2

#MAIN LOOP - Keeps running game logic so long as window is not closed.
while not libtcod.console_is_window_closed():
	libtcod.console_set_default_foreground(0, libtcod.white) #Sets the text color in game, 0 dictates the terminal window printed to.
	libtcod.console_put_char(0, playerx, playery, '@', libtcod.BKGND_NONE) #Prints character '@' to coordinates 'playerx,playery' (Middle of the terminal window). The first 0 indicates the terminal window, once again. 
	libtcod.console_flush() #Forces the terminal to print changes to the screen at the end of the main loop.

	libtcod.console_put_char(0, playerx, playery, ' ', libtcod.BKGND_NONE) #Clears the last character position on the screen.

	exit = handle_keys()
	if exit:
		break



