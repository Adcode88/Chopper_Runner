import pygame
import sys
from random import randint

pygame.init() #initialise

#git commit test 1

#collision
def collision(player, obstacles):
    if(obstacles):
        for obstacle_rect in obstacles:
            if(player.colliderect(obstacle_rect)): #method colliderect detects collisions between rectangles
                death_sound.set_volume(0.5)   
                death_sound.play()
                bgm.set_volume(0)
                pygame.time.set_timer(pygame.USEREVENT,7000)
                return False         
    return True

#obstacle movement
def obstacle_movement(obstacle_list):
    if(obstacle_list):
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8
        
            if(obstacle_rect.bottom) == 600:
                screen.blit(spikyball_surface,obstacle_rect)
            else:
                screen.blit(bat_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]

        return obstacle_list

    else:
        return []

#score setup
def disp_score():
    current_time = pygame.time.get_ticks() - sub_time
    score = current_time//400
    score_surface = font2.render(f'SCORE: {score} ', True, 'Green') #creating surface using text_font information (name, antialiasing, colour)
    score_rect = score_surface.get_rect(center=(1200,80))
    pygame.draw.rect(screen, (25,25,25), score_rect) #draw rectangle around score_rect (display surface, colour, rectangle, border width, border radius) here internal rectangle
    pygame.draw.rect(screen, (25,25,25), score_rect,50) #draw rectangle around score_rect (display surface, colour, rectangle, border width, border radius) here border
    screen.blit(score_surface,score_rect) #text printing
    return score

#test_surface = pygame.Surface((140,80)) #creating surface for objects on display surface

#sounds
jump_sound = pygame.mixer.Sound('sounds/jumpsoundeffect.mp3')
death_sound = pygame.mixer.Sound('sounds/deathsoundeffect.mp3')
bgm = pygame.mixer.Sound('sounds/archers2soundtrack.mp3')
jump_sound.set_volume(0.5)
death_sound.set_volume(0.5)
bgm.set_volume(0.5)
bgm.play(loops = -1)

screen = pygame.display.set_mode((1400,783)) #display screen creation
pygame.display.set_caption("First Game") #screen/game name
clock = pygame.time.Clock() #creating object clock of class 

#background setup
background_surface = pygame.image.load('graphics/animebackground.png').convert_alpha() #importing image as surface

#font setup
font2 = pygame.font.Font('font/font2.ttf', 80) #creating font information(font type, font size) font type imported from ttf file

#timing mechanism part 2
sub_time = 0

#score message mehcanism
score = 0

#player info
player_surface = pygame.image.load('graphics/chopper.png').convert_alpha() #importing convert image as surface
player_rect = player_surface.get_rect(bottomleft = (150,600)) #creating a rectangle around player_surface, (position of player_surface in player_rect = (position of player_rect_point))
player_gravity = 0

#obstacle info
spikyball_surface = pygame.image.load('graphics/spikyball.png').convert_alpha() #importing spiky ball image as surface
bat_surf = pygame.image.load('graphics/batside1.png').convert_alpha()

obstacle_rect_list = []

game_active = False #game_active is a variable which controls the state of the game

#timer mechanism
obstacle_timer = pygame.USEREVENT + 1 # +1 is needed as some events are reserved for pygame
pygame.time.set_timer(obstacle_timer,1500) #triggers every (obstacle_timer_,x) x miliseconds


while(True):


    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit condition
            pygame.quit() #opposite of pygame.init()
            sys.exit()
        
        if(event.type == pygame.USEREVENT):
            bgm.set_volume(0.5)

        if(game_active):

            #jump if space or key up
            if event.type == pygame.KEYDOWN: #checks whether any key is pressed
                if ((event.key == pygame.K_SPACE or event.key == pygame.K_UP) and (player_rect.bottom >= 600)): #checks whether up key or space key pressed
                    jump_sound.play()
                    player_gravity = -23 #falling mechanism (jump height)

            #jump if mouse button clicking on player_rect
            if event.type == pygame.MOUSEBUTTONDOWN: #checks whether mouse is pressed
                if ((player_rect.collidepoint(event.pos) and (player_rect.bottom >= 600))): #checks for collision between event.pos and player_rect (whether mouse is on player)
                    jump_sound.play()
                    player_gravity = -23 #falling mechanism (jump height)
            
            #exit if pressed e
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_e):
                    game_active = False

            if(event.type == obstacle_timer and game_active):
                if(randint(0,2)):
                    obstacle_rect_list.append(spikyball_surface.get_rect(midbottom = (randint(1200,1700),600)))
                else:
                    obstacle_rect_list.append(bat_surf.get_rect(midbottom = (randint(1450,1600),450)))
                    

        else: 
            #here game_active is false and thus this is the condition of instructions to follow when game is lost or ended amnually
            #restart if pressed space
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                game_active = True
                 

    if(game_active):

        bgm.set_volume(0.5)
        death_sound.set_volume(0)
    
        #background setup
        screen.blit(background_surface,(0,-200)) #blit = block image transfer

        #score text setup
        score = disp_score()

        #pygame.draw.line(screen, 'Orange', (0,0), pygame.mouse.get_pos(), 10) #line that follows mouse
        #pygame.draw.ellipse(screen, 'Blue', pygame.Rect(112, 425, 200, 200)) #draw ellipse (display surface, colour, Rectangle(left, top, width, height))

        #player motion
        if(player_rect.bottom >= 600):
            player_rect.bottom = 600 #floor mechanism
        screen.blit(player_surface,player_rect) #displaying player at position of player_rect such that player is in player_rect
        player_gravity += 0.985 #falling mechanism
        player_rect.top += player_gravity #falling mechanism

        #obstacle motion
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        game_active = collision(player_rect, obstacle_rect_list)

    else:
        #to avoid collision when restarting
        obstacle_rect_list.clear() #clear rect list
        player_rect.bottom = 600 #reset position of chopper

        #base screen
        screen.fill('#FFC90E') #fill screen with orange colour

        #score mechanism part 2
        sub_time = pygame.time.get_ticks() 

        #game over screen
        if(score != 0): 
            chopper_surf = pygame.image.load('graphics/chopperfinal.png').convert_alpha() #importing chopper final image as surface
            gameover_surf = font2.render('GAME OVER', True, 'Black') #creating surface using text_font information (name, antialiasing, colour)
            restart_surf = font2.render("Press Space To Restart", True, 'Blue')
            scoreshow_surf = font2.render(f'Your Score Was: {score}', True, 'Blue')
            
            chopper_rect = chopper_surf.get_rect(center = (680,350)) 
            gameover_rect = gameover_surf.get_rect(center = (700,70))
            restart_rect = restart_surf.get_rect(center = (700,700))
            scoreshow_rect = scoreshow_surf.get_rect(center = (700,180))

            screen.blit(chopper_surf,chopper_rect)
            screen.blit(gameover_surf,gameover_rect)
            screen.blit(restart_surf,restart_rect)
            screen.blit(scoreshow_surf,scoreshow_rect)

        #starting screen
        else:
            backchop_surf = pygame.image.load('graphics/chopback.jpg').convert_alpha()
            title_surf = font2.render(f'Run Chopper Run!', True, 'Blue')
            start_surf = font2.render("Press Space To Start", True, 'Red')         

            title_rect = title_surf.get_rect(center = (900,300))
            start_rect = start_surf.get_rect(center = (900,500))

            screen.blit(backchop_surf,(0,0))
            screen.blit(title_surf,title_rect)
            screen.blit(start_surf,start_rect)

    #if(player_rect.collidepoint(pygame.mouse.get_pos())): #checks whether mouse is inside player_rect
    #    print(pygame.mouse.get_pressed()) #prints status of buttons being clicked

    #keys = (pygame.key.get_pressed()) #store key pressed status in keys
    #if(keys[pygame.K_SPACE]): #checks if space is true in keys
    #    print('jump')

    pygame.display.update() #updates screen
    clock.tick(60) #controlling fps

#git commit test 2
