#Importing library and changing name to libtcod
import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#Starts the window (Last parameter decides if fullscreen or not
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)

#Keeps running game logic so long as window is not closed.
while not libtcod.console_is_window_closed():
	libtcod.console_set_default_foreground(0, libtcod.white) #Sets the text color in game, 0 dictates the terminal window printed to.
	libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE) #Prints character '@' to coordinates '1,1'. The first 0 indicates the terminal window, once again. 
	libtcod.console_flush() #Forces the terminal to print changes to the screen at the end of the main loop.



