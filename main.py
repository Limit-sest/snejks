import pygame
import pygame.freetype
from random import randint
from time import sleep,time
import pygame.mixer

pygame.init()
pygame.freetype.init()
pygame.mixer.init()

#TODO:
#	Body na obrazovce
#	Remíza	
#	Key queing
#
#	Mechaniky na ztizeni:
#		Normalni jidlo, stejne jako jablko tady -> pridava delku i body
#		jablko -> nepridava delku, pridava vice bodu


width, height = 1200, 760
#width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("S N E J K S")

menu_running = True
game_running = True

menu_sound = pygame.mixer.Sound("assets/snd_squeak.wav")
menu_confirm = pygame.mixer.Sound("assets/snd_select.wav")
apple_pickup = pygame.mixer.Sound("assets/snd_power.wav")
wall_place =  pygame.mixer.Sound("assets/snd_impact.wav")
game_collision = pygame.mixer.Sound("assets/snd_screenshake.wav")

title_font = pygame.freetype.Font("assets/title.ttf", 0)
text_font = pygame.freetype.Font("assets/text.ttf", 0)
cursor_font = pygame.freetype.Font("assets/cursor.ttf", 0)
cursor_color = 50
cursor_color_toggle = True
selected_option=0
options=[]







clock = pygame.time.Clock()

def shake_screen(screen, magnitude, duration):
    start_time = time()
    while time() - start_time < duration:
        # Create a temporary surface with an offset
        offset_x = randint(-magnitude, magnitude)
        offset_y = randint(-magnitude, magnitude)
        temp_surface = pygame.Surface((width, height))
        temp_surface.blit(screen, (offset_x, offset_y))
        
        screen.fill("black")  # Clear the screen
        screen.blit(temp_surface, (0, 0))  # Blit the temporary surface
        
        pygame.display.flip()

def title_text(surface, text, text_size, color):
    text_rect = title_font.get_rect(text, size = text_size)
    text_rect.centerx = surface.get_rect().centerx
    title_font.render_to(surface, text_rect, text, color, size = text_size)

def classic_text(text, surface = screen, color = "white", text_size = 75, pos_x = None, pos_y = None):
	text_rect = text_font.get_rect(text, size = text_size)
	if pos_y != None:
		text_rect.top = pos_y
	else:
		text_rect.centery = surface.get_rect().centery

	if pos_x != None:
		text_rect.left = pos_x
	else:
		text_rect.centerx = surface.get_rect().centerx

	text_font.render_to(surface, text_rect, text, color, size = text_size)
	return text_rect.topleft
    
def cursor():
	global cursor_color_toggle
	global cursor_color

	if cursor_color == 50:
		cursor_color_toggle = True
		cursor_color += 0.1
	elif cursor_color >= 200:
		cursor_color_toggle = False
		cursor_color -= 0.1
	else:
		if cursor_color_toggle == True:
			cursor_color += 0.1
		if cursor_color_toggle == False:
			cursor_color -= 0.1

	cursor_x=options[selected_option][0]
	cursor_y=options[selected_option][1]
	#pygame.draw.rect(screen,"red",(cursor_x,cursor_y,75,75))
	cursor_font.render_to(screen,(cursor_x-75,cursor_y),"X",(255,cursor_color,cursor_color),size=75)

def game():
	pass

def player_count_menu():
	pass

def game_over(winner):
		global selected_option
		global game_running
		global options
		global menu_running
		selected_option = 0
		snake_color_str = ["green", "blue", "yellow", "aqua"]
		snake_color =  [(125,255,125),(125,125,255),(255, 255, 125),(125, 255, 255)]

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				elif event.type == pygame.KEYDOWN:# Key register
					if event.key == pygame.K_UP or event.key == pygame.K_w:
						menu_sound.play()
						selected_option -= 1
					if event.key == pygame.K_DOWN or event.key == pygame.K_s:
						menu_sound.play()
						selected_option += 1
					if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN or event.key == pygame.K_q:
						menu_confirm.play()
						if selected_option == 0:
							game(1)
							game_running = False
							break
						if selected_option == 1:
							menu_running = True
							snake_menu()
			if menu_running == False:
				game_running = False
				break

			screen.fill(pygame.Color("black"))
			if winner == "game":
				title_text(screen,"game over!",200,(255,125,125))
			else:
				text = snake_color_str[winner] + " snake wins!"
				title_text(screen,text,150,snake_color[winner])
			if selected_option == -1:
				selected_option = len(options)-1
			if selected_option == len(options):
				selected_option = 0
			options.clear()
			options.append(classic_text("Retry", pos_y=425))
			options.append(classic_text("Menu", pos_y=500))
			cursor()
			pygame.display.flip()

def game(player_count):
	size = 20

	global game_running


	snake = [[[0,0],[size,0],[size*2,0]],
	[[width-size,height-size],[width-size*2,height-size],[width-size*3,height-size]],
	[[width-size,0],[width-size*2,0],[width-size*3,0]],
	[[size,height-size],[size*2,height-size],[size*3,height-size]]]

	changedir = ["right", "left", "left", "right"]
	direction = ["right", "left", "left", "right"]
	prekazky = [[],[],[],[]]
	keys = [[pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_e],[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT],[pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_o], [pygame.K_KP5, pygame.K_KP2, pygame.K_KP1, pygame.K_KP3, pygame.K_KP0]]
	snake_color =  [(0,255,0),(0,0,255),(255, 255, 0),(0, 255, 255)]
	
	prekazky_color = [(0,125,0),(0,0,125),(125, 125, 0),(0, 125, 125)]
	place_trigger = randint(15,30)
	start_player_count = player_count
	players = []
	for i in range(player_count):
		players.append(i)

	speed =  10
	apple = [randint(0,(width-size)//size)*size, randint(0,(height-size)//size)*size]

	def is_apple_valid():
		for y4 in players:
			for i in range(len(snake[y4])):
				if apple == snake[y4][i]:
					return False
			for i in range(len(prekazky[y4])):
				if apple == prekazky[y4][i]:
					return False
		return True
	
	def eliminate(player):
		players.remove(player)
		prekazky[player].extend(snake[player][:len(snake[player])])
		snake[player].clear()
		game_collision.play()
		shake_screen(screen,5,0.25)
		if len(players) == 1 and start_player_count > 1:
			game_over(players[0])

		if len(players) == 0:
			game_over("game")

	while game_running:
		screen.fill("black")
		#draw apple
		pygame.draw.rect(screen,"red",(apple[0],apple[1],size,size))
		for y in players:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_running = False
				elif event.type == pygame.KEYDOWN:# Key register
					if player_count >= 2:
						for y2 in players:
							if event.key == keys[y2][0]:
								changedir[y2] = "up"
							if event.key == keys[y2][1]:
								changedir[y2] = "down"
							if event.key == keys[y2][2]:
								changedir[y2] = "left"
							if event.key == keys[y2][3]:
								changedir[y2] = "right"
							if event.key == keys[y2][4]:
								if len(snake[y2]) > 3:
									prekazky[y2].extend(snake[y2][:len(snake[y2])-3])
									del snake[y2][:len(snake[y2])-3]
									wall_place.play()
									place_trigger = randint(10,20)
									speed += 0.5
					elif player_count == 1:#možnost pro ovládání ↑↓←→ a WSAD w singleplayeru
						for y2 in range(2):
							if event.key == keys[y2][0]:
								changedir[0] = "up"
							if event.key == keys[y2][1]:
								changedir[0] = "down"
							if event.key == keys[y2][2]:
								changedir[0] = "left"
							if event.key == keys[y2][3]:
								changedir[0] = "right"
					if event.key == pygame.K_ESCAPE:
						game_running = False

			if len(players) == 1 and start_player_count > 1:
				game_over(players[y])

			if len(players) == 0:
				game_over("game")

			#draw snake[y]
			for i in range(len(snake[y])):
				pygame.draw.rect(screen,snake_color[y],(snake[y][i][0],snake[y][i][1],size,size))

			#draw prekazky[y]
			for i in range(len(prekazky[y])):
				pygame.draw.rect(screen,prekazky_color[y],(prekazky[y][i][0],prekazky[y][i][1],size,size))
			
			#overeni pohybu
			if changedir[y] == "right" and direction[y] != "left":
				direction[y] = changedir[y]
			if changedir[y] == "left" and direction[y] != "right":
				direction[y] = changedir[y]
			if changedir[y] == "up" and direction[y] != "down":
				direction[y] = changedir[y]
			if changedir[y] == "down" and direction[y] != "up":
				direction[y] = changedir[y]

			#pohyb
			if direction[y] == "left":
				snake[y].append([snake[y][-1][0]-size, snake[y][-1][1]])
				snake[y].pop(0)
			elif direction[y] == "right":
				snake[y].append([snake[y][-1][0]+size, snake[y][-1][1]])
				snake[y].pop(0)
			elif direction[y] == "down":
				snake[y].append([snake[y][-1][0], snake[y][-1][1]+size])
				snake[y].pop(0)
			elif direction[y] == "up":
				snake[y].append([snake[y][-1][0], snake[y][-1][1]-size])
				snake[y].pop(0)

			#jablko
			if snake[y][-1] == apple:
				apple = [randint(0,(width-size)//size)*size, randint(0,(height-size)//size)*size]
				
				while is_apple_valid() == False:
					apple = [randint(0,(width-size)//size)*size, randint(0,(height-size)//size)*size]

				snake[y].insert(0,[snake[y][0][0], snake[y][0][1]])
				snake[y].insert(0,[snake[y][0][0], snake[y][0][1]])
				apple_pickup.play()
			
			#self destruct
			for i in range(len(snake[y])-1):
				if snake[y][-1] == snake[y][i]:
					clock.tick(10)
					eliminate(y)
					break

			#pacman effect
			for i in range(len(snake[y])):
				if snake[y][i][0] >= width:
					if player_count > 1: snake[y][i][0] = 0 
					else: eliminate(y)
				if snake[y][i][0] < 0:
					if player_count > 1: snake[y][i][0] = width-size
					else: eliminate(y)
				if snake[y][i][1] >= height:
					if player_count > 1: snake[y][i][1] = 0
					else: eliminate(y)
				if snake[y][i][1] < 0:
					if player_count > 1: snake[y][i][1] = height-size
					else: eliminate(y)

			#prekazky[y] destruct
			for y5 in players:
				for i in range(len(prekazky[y5])):
					if snake[y][-1] == prekazky[y5][i]:
						clock.tick(10)
						eliminate(y)
						break

			#prekazky place	(1 player)
			if len(snake[y]) >= place_trigger and player_count == 1:
				prekazky[y].extend(snake[y][:len(snake[y])-3])
				del snake[y][:len(snake[y])-3]
				wall_place.play()
				place_trigger = randint(15,30)
				speed += 1
			
			#player destruct
			for y3 in players:
				if y3 != y:
					for i in range(len(snake[y])):
						if snake[y][-1] == snake[y3][-1]:
							eliminate(y3)
							eliminate(y)
							break
						elif snake[y][i] == snake[y3][-1] and snake[y][i] != snake[y][-1]:
							eliminate(y3)
							break
				else:
					continue
		

		pygame.display.flip()
		clock.tick(speed)

def player_count_menu():
	global selected_option
	while True:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				break
			elif event.type == pygame.KEYDOWN:# Key register
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					selected_option -= 1
					menu_sound.play()
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					selected_option += 1
					menu_sound.play()
				if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
					menu_confirm.play()
					if selected_option == 0:
						return 1
					if selected_option == 1:
						return 2
					if selected_option == 2:
						return 3
					if selected_option == 3:
						return 4


		screen.fill("black")

		#overeni selection

		title_text(screen,"select player count",130,"white")
		options.clear()
		options.append(classic_text("1 Player",pos_y=350))
		options.append(classic_text("2 Players",pos_y=425))
		options.append(classic_text("3 Players",pos_y=500))
		options.append(classic_text("4 Players",pos_y=575))

		if selected_option == -1:
			selected_option = len(options)-1
		if selected_option == len(options):
			selected_option = 0

		cursor()
			

		pygame.display.flip()

###################################- M E N U -###########################################
def snake_menu():
	

	global game_running
	global menu_running
	global selected_option
	while menu_running:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				menu_running = False
			elif event.type == pygame.KEYDOWN:# Key register
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					selected_option -= 1
					menu_sound.play()
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					selected_option += 1
					menu_sound.play()
				if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
					menu_confirm.play()
					if selected_option == 0:
						game_running = True
						game(1)
					if selected_option == 1:
						menu_running = False


		screen.fill("black")

		#overeni selection

		title_text(screen,"snejks",250,"white")
		options.clear()
		options.append(classic_text("Play",pos_y=350))
		options.append(classic_text("Quit",pos_y=425))

		if selected_option == -1:
			selected_option = len(options)-1
		if selected_option == len(options):
			selected_option = 0

		cursor()
			

		pygame.display.flip()

	if pygame.mixer.get_busy() == True:
		sleep(0.1)

if __name__ == "__main__":
	snake_menu()