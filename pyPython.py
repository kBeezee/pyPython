import libtcodpy as libtcod

#actual size of the window
SCREEN_WIDTH = 75
SCREEN_HEIGHT = 50
 
#size of the map
MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT
 
LIMIT_FPS = 22 #20 frames-per-second maximum

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

oldX = 0
oldY = 0

initSnakeLen = 10
mySnakeLength = initSnakeLen
class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked):
        self.blocked = blocked
    
class Object:
    #this is a generic object: it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color, blocks=True):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
 
    def move(self, dx, dy):
      global mySnakeLength
      global food
      global map
      
      self.x += dx
      self.y += dy
      
      #eat food
      for object in food:
	if object.x == self.x and object.y == self.y:
	    food.pop()

	    while True:  
	      rany = libtcod.random_get_int(0, 2, MAP_HEIGHT - 2)
	      ranx = libtcod.random_get_int(0, 2, MAP_WIDTH - 2)
	      if map[rany][ranx].blocked == False:
		break
	  
	    eatIt = Item(ranx, rany, '$', 'food', libtcod.yellow)
	    food = [eatIt]
	    eatIt.draw
	    
	    sb = Object(self.x - dx, self.y - dy, '#', 'snake', libtcod.white)
	    objects.insert(1, sb)
	    
	    #print 'Ate It'
	    mySnakeLength += 1
	    break
	
	myLevel = (mySnakeLength - initSnakeLen) / 10
	define_map(myLevel)
	
	#die if need be.
	global sHead
	for idx, val in enumerate(objects):
	  if idx == 0:
	    sHead = val
	  elif sHead.x == playerInitX and sHead.y == playerInitY:
	    break
	  else:
	    if sHead.x == val.x and sHead.y == val.y:
	      return 'dead'
	      break
	#check to see if we hit something impassible.
	for idx, val in enumerate(map):
	  if map[sHead.y][sHead.x].blocked:
	    return 'dead'
	  
      #remove the last part of the body
      objects.pop()
      
      #put the new part of hte body where the head just was.
      sb = Object(self.x - dx, self.y - dy, '#', 'snake', libtcod.white)
      objects.insert(1, sb)
      return 'alive'
      
    def draw(self):
	#set the color and then draw the character that represents this object at its position
      libtcod.console_set_default_foreground(con, self.color)
      libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
      #erase the character that represents this object
      libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

class Item:
  def __init__(self, x, y, char, name, color, blocks=False):
    self.x = x
    self.y = y
    self.char = char
    self.name = name
    self.color = color
    self.blocks = blocks
  
  def draw(self):
    #set the color and then draw the character that represents this object at its position
    libtcod.console_set_default_foreground(con, self.color)
    libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

  def clear(self):
    #erase the character that represents this object
    libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def make2dList(rows, cols):
  a=[]
  for row in xrange(rows): a += [[0]*cols]
  return a

def define_map(level):
  global map
#this is ugly, I want to put all of the below in its own file
#when the time comes.
#and switch its format to use this:
#http://bytebaker.com/2008/11/03/switch-case-statement-in-python/
  
  #start w/ a blank slate.
  map = [[ Tile(False)  
  for x in range(MAP_WIDTH+1) ]
    for y in range(MAP_HEIGHT+1) ]
  
  if level == 1:
    for x in range(MAP_HEIGHT):
      map[x][0] = Tile(True)
      map[x][MAP_WIDTH-1] = Tile(True)
    for y in range(MAP_WIDTH):
      map[0][y] = Tile(True)
      map[MAP_HEIGHT-1][y] = Tile(True)

  elif level == 2:
    for x in range(MAP_HEIGHT):
      if x < MAP_HEIGHT - 7 and x > 7:
	map[x][MAP_WIDTH / 3] = Tile(True)
	map[x][MAP_WIDTH - MAP_WIDTH / 3] = Tile(True)
	
  elif level == 3:
    for x in range(MAP_HEIGHT):
      map[x][0] = Tile(True)
      map[x][MAP_WIDTH-1] = Tile(True)
    for y in range(MAP_WIDTH):
      map[0][y] = Tile(True)
      map[MAP_HEIGHT-1][y] = Tile(True)
    for x in range(MAP_HEIGHT):
      if x < MAP_HEIGHT - 7 and x > 7:
	map[x][MAP_WIDTH / 3] = Tile(True)
	map[x][MAP_WIDTH - MAP_WIDTH / 3] = Tile(True)
  
  elif level == 4:
    for x in range(MAP_HEIGHT):
      map[x][MAP_WIDTH / 2] = Tile(True)
    for y in range(MAP_WIDTH):
      map[MAP_HEIGHT / 2][y] = Tile(True)
  
def make_map(level=0):
  map = make2dList(MAP_WIDTH+1, MAP_HEIGHT+1)
  define_map(level)

def render_all():
  global color_dark_ground, color_dark_wall
  
  for x in range(MAP_WIDTH):
    for y in range(MAP_HEIGHT):
      if map[y][x].blocked == False:
	libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
      else:
	libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
	
  for object in objects:
    object.draw()
  
  for object in food:
    object.draw()
  
  line = 'Your Score: ' + str(mySnakeLength - initSnakeLen)
  libtcod.console_print_ex(con, 5, SCREEN_HEIGHT-1, libtcod.BKGND_NONE, libtcod.LEFT, str(line))
  
  libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
  
def handle_keys():
    global oldX, oldY, event
    key = libtcod.console_check_for_keypress()  #real-time
    #key = libtcod.console_wait_for_keypress(True)  #turn-based

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  #exit game

    elif libtcod.console_is_key_pressed(libtcod.KEY_UP) and event <> 'dead':
      if oldX == 0 and oldY == 1:
	event = player_move_or_eat(0,1)
      else:
	event = player_move_or_eat(0, -1)
	oldX = 0
	oldY = -1
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) and event <> 'dead':
      if oldX == 0 and oldY == -1:
	event = player_move_or_eat(0, -1)
      else:
	event = player_move_or_eat(0, 1)
	oldX = 0
	oldY = 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) and event <> 'dead':
      if oldX == 1 and oldY == 0:
	event = player_move_or_eat(1,0)
      else:
	event = player_move_or_eat(-1, 0)
	oldX = -1
	oldY = 0
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) and event <> 'dead':
      if oldX == -1 and oldY == 0:
	event = player_move_or_eat(-1, 0)
      else:
	event = player_move_or_eat(1, 0)
	oldX = 1
	oldY = 0
    elif libtcod.console_is_key_pressed(libtcod.KEY_SPACE) and event == 'dead':
      event = 'restart'
    else:
      if event <> 'dead':
	event = player_move_or_eat(oldX, oldY)
    
    return event
def player_move_or_eat(dx, dy):
    global objects
    #this moves the head
    x = player.x + dx
    y = player.y + dy
    
    print len(map), len(map[y])
    #51, 76
    if x > SCREEN_WIDTH -1:
      player.x = 0
    if x <= 0:
      player.x = SCREEN_WIDTH -1
    
    if y > SCREEN_HEIGHT-1:
      player.y = 0
    if y <= 0:
      player.y = SCREEN_HEIGHT -1
      
    #test to see if the player lost.
    event = player.move(dx, dy)
    return event
    #this gets returned to handle keys which gets returned to the main loop
    
def playerLost():
  #bug: if you collide at your starting location, the code will let you live.
  #print 
  global oldX, oldY
  oldX = 0
  oldY = 0
  
  dead = libtcod.console_new(SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
  
  for x in range(MAP_WIDTH):
    for y in range(MAP_HEIGHT):
      libtcod.console_set_char_background(dead, x, y, libtcod.desaturated_red, libtcod.BKGND_SET)
  
  #cool, i think i got it...
  line = str('You died with a score of ') + str(mySnakeLength - initSnakeLen)
  libtcod.console_print_ex(dead, SCREEN_WIDTH/4, 4, libtcod.BKGND_NONE, libtcod.CENTER, str(line))
  line = str('Press Space to Play Again')
  libtcod.console_print_ex(dead, SCREEN_WIDTH/4 -1, 6, libtcod.BKGND_NONE, libtcod.CENTER, str(line))
  libtcod.console_clear(con)
  #libtcod.console_blit(dead, 0, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT, 0, 0, 0)
  #console_blit(src,xSrc,ySrc,xSrc,hSrc,dst,xDst,yDst,foregroundAlpha=1.0,backgroundAlpha=1.0)
  libtcod.console_blit(dead, 0, 0, 0, 0, 0, (SCREEN_WIDTH/4)+2, (SCREEN_HEIGHT/4)+2)
  libtcod.console_flush()

  
  
    
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
 
#generate map (at this point it's not drawn to the screen)
make_map()

#grab random numbers and then check if they are blocked
#if they are get new random number, this is a do until loop.
while True:
  ranx = libtcod.random_get_int(0, 5, SCREEN_WIDTH - 20)
  rany = libtcod.random_get_int(0, 5, SCREEN_HEIGHT - 20)
  if map[rany][ranx].blocked == False:
    break
  
#take our unblocked random numbers and place our snake head there.
playerInitX = ranx
playerInitY = rany
player = Object(playerInitX, playerInitY, '@', 'head', libtcod.white)

#the list of objects with just the player
objects = [player]

#add the body of the snake to the list.
for i in range(mySnakeLength):
  sb = Object(player.x, player.y, '#', 'snake', libtcod.white)
  objects.append(sb)

#place the first thing for the snake to eat.
while True:
  ranx = libtcod.random_get_int(0, 5, SCREEN_WIDTH - 20)
  rany = libtcod.random_get_int(0, 5, SCREEN_HEIGHT - 20)
  if map[rany][ranx].blocked == False:
    break
  
eatIt = Item(ranx, rany, '$', 'food', libtcod.yellow)
food = [eatIt]
eatIt.draw

global p_action, event

p_action = 'alive'
event = 'alive'
##here is the start of the loop
while not libtcod.console_is_window_closed():
  if p_action <> 'dead':
    render_all()
  else:
    playerLost()
    
  libtcod.console_flush()
  
  for object in objects:
    object.clear()

  p_action = handle_keys()
  
  if p_action == 'restart': 
    make_map()
    mySnakeLength = initSnakeLen
    #grab random numbers and then check if they are blocked
    #if they are get new random number, this is a do until loop.
    while True:
      ranx = libtcod.random_get_int(0, 5, SCREEN_WIDTH - 20)
      rany = libtcod.random_get_int(0, 5, SCREEN_HEIGHT - 20)
      if map[rany][ranx].blocked == False:
	break
      
    #take our unblocked random numbers and place our snake head there.
    playerInitX = ranx
    playerInitY = rany
    player = Object(playerInitX, playerInitY, '@', 'head', libtcod.white)

    #the list of objects with just the player
    objects = [player]

    #add the body of the snake to the list.
    for i in range(initSnakeLen):
      sb = Object(player.x, player.y, '#', 'snake', libtcod.white)
      objects.append(sb)

    #place the first thing for the snake to eat.
    ranx = libtcod.random_get_int(0, 5, SCREEN_WIDTH - 20)
    rany = libtcod.random_get_int(0, 5, SCREEN_HEIGHT - 20)

    eatIt = Item(ranx, rany, '$', 'food', libtcod.yellow)
    food = [eatIt]
    eatIt.draw

    global p_action, event

    p_action = 'alive'
    event = 'alive'
  
  if p_action == 'exit':
    print 'Quit'
    break

  #print 'End of Game Loop'