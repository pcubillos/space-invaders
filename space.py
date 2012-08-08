#! /usr/bin/env python

import os, sys, pygame
from pygame.locals import *
from numpy import random, zeros
import objects, config


def where_alive(lista):
    alive = []
    for element in lista:
        if element.isAlive and element.state == 0:
            alive.append(element)
    return alive, len(alive)

def index_alive(lista):
    alive = []
    for i in range(len(lista)):
        if lista[i].isAlive:
            alive.append(i)
    if len(alive) > 0:
        return alive, True
    else:
        return alive, False

def where_ammo(lista):
    avail = []
    for element in range( len(lista) ):
        if not lista[element].isAlive:
            avail.append(element)
    return avail, len(avail)

def plot_text(font, texto, screen, position, color):
    the_text = font.render( texto.strip(), True, color )
    rect = the_text.get_rect()
    rect.midtop = position
    screen.blit(the_text, rect)

def hit( left, bottom, right, top, left2, bottom2, right2=None, top2=None ):
    # 6 params > bullet
    if not right2: right2 = left2   
    if not top2: top2 = bottom2 - 4

    if left <= right2  and right  >= left2 and \
       top  <= bottom2 and bottom >= top2:
        return True
    else:
        return False

def hit( rect, rect2 ):
    if rect[0] <= rect2[2] and rect[2] >= rect2[0] and \
       rect[3] <= rect2[1] and rect[1] >= rect2[3]:
        return True
    else:
        return False

class State:

    """
    A generic game state class that can handle events and display
    itself on a given surface.
    """
    level = 1
    option = 1
    n_options = 5
    fps = 0
    pygame.font.init()
    font_fps = pygame.font.SysFont(None, config.font_size_fps)

    def handle(self, event):
        """
        Default event handling only deals with quitting.
        """
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_LEFT:
                pass
            if event.key == K_RIGHT:
                pass
            if event.key == K_SPACE:
                pass
            if event.key == K_x:
                pass
            if event.key == K_c:
                pass

        if event.type == KEYUP:
            if event.key == K_LEFT:
                pass
            if event.key == K_RIGHT:
                pass
            if event.key == K_SPACE:
                pass
            if event.key == K_x:
                pass
            if event.key == K_c:
                pass

    def display(self, screen):
        """
        Used to display the State after it has already been displayed
        once. The default behavior is to do nothing.
        """
        # the background
        screen.blit(game.background, game.bg_rect)

        # the stars
        game.stars_y = (game.stars_y + game.stars_v*0.2) % config.screen_size[1]
        for i in range(config.n_stars):
            game.stars_x[i] = game.stars_x[i] if not game.stars_v[i] else \
                             game.stars_x[i] + 0.1*int((random.rand()-0.5)*2.1)
            pygame.draw.aaline(screen, config.color_stars,        \
                     (int(game.stars_x[i]),int(game.stars_y[i])), \
                     (int(game.stars_x[i]),int(game.stars_y[i]))  )
        # plot fps
        plot_text(self.font_fps, "%i fps" % self.fps, screen, \
                  config.fps_position, config.font_color_fps)



class Play(State):
    enemigos = []

    def __init__(self, level=1, stage=1):
        self.waiting = True
        self.time_waiting = config.waiting_time/2
        self.stage = stage
        self.level = level
        self.n_enemies = config.total_enemies
        self.font_wait = pygame.font.SysFont(None, config.wait_size)
        # Create hero
        self.hero = objects.starship(level)

        # Create enemies
        del self.enemigos[:]
        for i in range(config.total_enemies):
            self.enemigos.append(objects.enemy1(i))

        # probabilities
        self.pb_release_time  = 0.0
        self.pb_release_kills = 0.0

        # stage and score
        self.font_ss = pygame.font.Font(None, config.font_size_ss)

    def restart(self, level=1, stage=1):
        self.stage = stage
        self.level = level
        self.n_enemies = config.total_enemies

        for i in range(self.n_enemies):
            if(random.rand() < 0.035*(self.stage + self.level - 5) ):
#            if(random.rand() < 0.5 ):
                self.enemigos[i] = objects.enemy2(i) 
            else:
                self.enemigos[i] = objects.enemy1(i)

            self.pb_release_time  = 0.0
            self.pb_release_kills = 0.0    

        if stage == 1:
            self.hero = objects.starship(level)
            for i in range(self.n_enemies):
                self.enemigos[i] = objects.enemy1(i) 

    def update(self, game):
        if not self.waiting:
            self.release_enemy()
            for enemigo in self.enemigos:
                enemigo.shoot(5e-4*self.level + 5e-4*(self.stage-1) +    \
                              5e-4*(config.total_enemies - self.n_enemies) )
            self.check_hits()
            self.check_catch()
        # Update hero
        self.hero.update()

        # Update enemy
        for enemigo in self.enemigos:
            enemigo.update()

        # Go to next state
        if self.hero.lives == 0:
            game.nextState = GameOver(game.score)
            game.score = 0

        if self.n_enemies == 0 and not self.waiting:
            self.waiting = True
            self.time_waiting = config.waiting_time

        if self.time_waiting >= 0:
#            if self.time_waiting == 0:
            if self.time_waiting == config.waiting_time*3/4:
                self.restart(self.level, self.stage + 1)
            if self.time_waiting == 0:
                self.waiting = False
            self.time_waiting -= 1

    def display(self, screen):
        State.display(self, screen)

        # plot stage message
        if self.waiting and self.time_waiting < config.waiting_time/2:
            plot_text(self.font_wait, "STAGE %i" % self.stage, screen, \
                          config.wait_position, config.wait_color)

        # plot score and stage
        plot_text(self.font_ss, "stage: %i" % self.stage, screen, \
                  config.stage_position, config.font_color_ss)
        plot_text(self.font_ss, "score: %i" % game.score, screen, \
                  config.score_position, config.font_color_ss)

        self.hero.draw(screen)
        for enemigo in self.enemigos:
            enemigo.draw(screen)

        pygame.display.flip()

    def handle(self, event, screen):
        State.handle(self, event)

        # Pressing
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if self.hero.isAlive:
                    self.hero.dv = -config.velocity
                    self.hero.moving_l = True

            if event.key == K_RIGHT:
                if self.hero.isAlive:
                    self.hero.dv = config.velocity
                    self.hero.moving_r = True

            if event.key == K_SPACE and not self.waiting:
                if not self.hero.hold and self.hero.isAlive:
                    avail, n_avail = where_ammo(self.hero.ammo)
                    if n_avail > 0:
                        self.hero.ammo[avail[0]] = objects.bullet( \
                                        self.hero.coo_x[4], self.hero.coo_y[4])
                        self.hero.hold = True
                        self.hero.ammo_holded = avail[0]

            if event.key == K_x and not self.waiting:
                if self.hero.isAlive:
                    for j in range(config.n_bombs):
                        if self.hero.special[0][j].isAlive and \
                                self.hero.special[0][j].status == 1:
                            self.hero.special[0][j].changeStatus(2)

            if event.key == K_c and not self.waiting:
                if self.hero.isAlive:
                    b = False
                    for t in [2, 1]:
                        for j in range(config.n_bombs):
                            if self.hero.special[1][j].isAlive and \
                                    self.hero.special[1][j].status == t:
                                if b: 
                                    break
                                self.hero.special[1][j].changeStatus( \
                                    self.hero.special[1][j].status + 1)
                                b = True
            if event.key == K_RETURN:
                print 'save!'
                pygame.image.save(screen, 'screencap.png')
        # Releasing
        if event.type == KEYUP:
            if event.key == K_LEFT:
                if self.hero.isAlive: 
                    self.hero.dv =  config.velocity if self.hero.moving_r else 0
                    self.hero.moving_l = False

            if event.key == K_RIGHT:
                if self.hero.isAlive:
                    self.hero.dv = -config.velocity if self.hero.moving_l else 0
                    self.hero.moving_r = False

            if event.key == K_SPACE:
                if(self.hero.hold):
                    self.hero.hold = False
                    self.hero.ammo[self.hero.ammo_holded].hooked = False

            if event.key == K_x:
                pass
            if event.key == K_c:
                pass

    def release_enemy(self):
        if random.rand() < (self.pb_release_time + self.pb_release_kills):
            vivos, n_vivos = where_alive(self.enemigos)
            self.enemigos[int(random.rand()*n_vivos)].state = 1
        if self.pb_release_time < 0.0038 and self.pb_release_kills > 0.0011:
            self.pb_release_time += 0.000001

    def create_bomb(self, pos_x, pos_y):
        i = int(random.rand()*config.type_bombs);
       # i=0;
       # System.out.println(" CREATE "+i);
        for j in range(config.n_bombs):
            if not ( self.hero.special[i][j].isAlive and 
#                     random.rand() < (0.143-(self.level-1)*0.012) ):
                         True ):
                if i == 0:
                    self.hero.special[i][j] = objects.laser(pos_x, pos_y)
                elif i == 1:
                    self.hero.special[i][j] = objects.cluster(pos_x, pos_y)
                else:
                    self.hero.special[i][j] = objects.rocket(pos_x, pos_y)
                break

    def check_hits(self):
        # hero bullets to enemies
        vivos, are_they = index_alive(self.hero.ammo)
        for i in vivos:
            if not are_they:
                break
            malditos, estan_vivos = index_alive(self.enemigos)
            for j in malditos:
                if not estan_vivos:
                    break
                if hit(self.enemigos[j].get_rect(), \
                       self.hero.ammo[i].get_rect()):
                    self.hero.ammo[i].isAlive = False
                    self.enemigos[j].kill()
                    game.score += 100
                    self.n_enemies -= 1
                    self.pb_release_kills = 6e-4 * \
                        ( config.total_enemies - self.n_enemies )
                    self.create_bomb(self.hero.ammo[i].x, self.hero.ammo[i].y)
                    if self.n_enemies == 0:
                        pass
                    break

        # enemy bullets to hero
        if self.hero.isAlive:
            for i in range(config.total_enemies):
                balas, are_they = index_alive(self.enemigos[i].ammo)
                for j in balas:
                    if not are_they:
                        break
                    if hit(self.enemigos[i].ammo[j].get_rect(), \
                           self.hero.get_rect()) or             \
                       hit(self.enemigos[i].ammo[j].get_rect(), \
                           self.hero.get_rect(True)):
                        self.hero.kill()
                        self.enemigos[i].ammo[j].isAlive = False
#                        hero.stop();
#                        break;

        # colision   
        for i in range(config.total_enemies):  
            if self.enemigos[i].isAlive and self.hero.isAlive:
                if hit(self.enemigos[i].get_rect(), self.hero.get_rect()) or \
                   hit(self.enemigos[i].get_rect(), self.hero.get_rect(True)):
                    self.enemigos[i].kill()
                    self.hero.kill()
                    game.score += 100
                    self.hero.stop()
                    self.n_enemies -= 1
                    self.pb_release_kills = 6e-4 * \
                        ( config.total_enemies - self.n_enemies )
                    if self.n_enemies == 0:
                        pass
                    break

        for i in range(config.type_bombs): # type bomb
            for j in range(config.n_bombs):
                if self.hero.special[i][j].isAlive:
                    malditos, estan_vivos = index_alive(self.enemigos)
                    for k in malditos:
                        if self.hero.special[i][j].checkHit( \
                            self.enemigos[k].get_rect()):
# enemigos[k].x[1], enemigos[k].x[4], enemigos[k].y[2], enemigos[k].y[0]):
                            self.enemigos[k].kill()
                            game.score += 100
                            self.n_enemies -= 1
                            self.pb_release_kills = 6e-4 * \
                                ( config.total_enemies - self.n_enemies )

    def check_catch(self):   # hero catch bombs
        for i in range(config.type_bombs):
            for j in range(config.n_bombs):
                if self.hero.special[i][j].isAlive and \
                   self.hero.special[i][j].status == 0:                        
                    if hit(self.hero.special[i][j].get_rect(), \
                           self.hero.get_rect() )              \
                    or hit(self.hero.special[i][j].get_rect(), \
                           self.hero.get_rect(True)):
                        if self.hero.special[i][abs(j-1)].status != 1:
                            self.hero.special[i][j].changeStatus(1)
                        else:
                            self.hero.special[i][j].isAlive = False

class Paused(State):
    
    finished = 0 # Has the user ended the pause?
    image = None # Set this to a file name if you want an image
    text = '' # Set this to some informative text

    def handle(self, event, screen):
        State.handle(self, event)
        if event.type in [MOUSEBUTTONDOWN]:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > 142 and mouse_pos[0] < 202 and \
               mouse_pos[1] > 257 and mouse_pos[1] < 277:
                self.finished = 1
        
        if event.type in [KEYDOWN]:
            if event.key == K_DOWN:
                self.option = min(self.option + 1, self.n_options)
            if event.key == K_UP:
                self.option = max(self.option - 1, 1) 
            if event.key == K_RETURN:
                self.finished = 1

    def update(self, game):
        if self.finished:
            game.nextState = self.nextState()

    def display(self, screen):
        State.display(self, screen)

        # Create a Font object with the default appearance, and specified size:
        font_title = pygame.font.SysFont(None, config.font_startUp_title)
        font_body  = pygame.font.SysFont(None, config.font_startUp)
        font_title.set_italic(1)
        
        # If there is an image to display...
        if self.image:
            image = pygame.image.load(self.image).convert()
            r = image.get_rect()
            top += r.height // 2
            r.midbottom = center, top - 20
            screen.blit(image, r)

        aalias = True

        # Big text
        for i in range(len(self.text_big)-1):
            texto = font_title.render(self.text_big[i].strip(), aalias, \
                                      config.color_text)
            r = texto.get_rect()
            r.topleft = config.title_x_pos + i*config.title_deltaX, \
                        config.title_y_pos + i*config.title_deltaY
            screen.blit(texto, r)

        # Text
        for i in range(len(self.text)):
            texto = font_body.render(self.text[i].strip(), aalias, \
                                    config.color_text)
            r = texto.get_rect()
            r.topleft = config.texto_x_pos,  \
                         config.texto_y_pos + i*config.texto_deltaY
            screen.blit(texto, r)

        # Cursor
        texto = font_body.render(self.text_big[-1].strip(), aalias, \
                                 config.color_text)
        r = texto.get_rect()
        r.topleft = config.cursor_x_pos, \
                    config.cursor_y_pos + self.option*config.texto_deltaY
        screen.blit(texto, r)

        # draw rectangle if necessary
        if self.rectangle: 
            pygame.draw.rect(screen, config.color_text, self.rectangle, 1)

        # Display all the changes:
        pygame.display.flip()

class GameOver(Paused):

    def __init__(self, score):
        self.n_options = 2
        self.image    = None
        self.text_big = ["Play again? ", "Final Score: %i" % score,">>" ]
        self.text     = ["Yeah", "Nope" ]
        self.rectangle = None

    def update(self, game):
        if self.finished:
            if self.option == 2: 
                sys.exit()
            else:                
                game.nextState = StartUp()
            

class StartUp(Paused):

    n_options = 5
    image    = None
    text_big = ["CHOOSE LEVEL: ", "GO", ">>" ]
    text     = ["sumamente sencillo", "puc", "nenita", "hard", "extreme" ]
    rectangle = 142, 257, 60, 20

    def update(self, game):     
        if self.finished:         
            game.nextState = Play(self.option, 1)
            


class Game:
    
    """
    A game object that takes care of the main event loop, including
    changing between the different game states.
    """

    def __init__(self, *args):
        # Get the directory where the game and the images are located:
        path = os.path.abspath(args[0])
        dir = os.path.split(path)[0]
        # Move to that directory (so that the image files may be
        # opened later on):
        os.chdir(dir)
        # Start with no state:
        self.state = None
        # Move to StartUp in the first event loop iteration:
        self.nextState = StartUp()
        self.background = None
        self.bg_rect = None
        self.score = 0

        # the stars
        self.stars_x = random.rand(config.n_stars)*config.screen_size[0]
        self.stars_y = random.rand(config.n_stars)*config.screen_size[1]
        self.stars_v = zeros(config.n_stars)
        for i in range(config.n_stars):
            self.stars_v[i] = int( 0.5 + random.rand()*config.stars_vel )

    def run(self):
        """
        This method sets things in motion. It performs some vital
        initialization tasks, and enters the main event loop.
        """
        pygame.init()

        # Sounds
#        self.sound_blast = pygame.mixer.Sound("blast.wav")
#        self.sound_bomb  = pygame.mixer.Sound("bombfall.wav")
#        self.sound_laser = pygame.mixer.Sound("laser.wav")
        

        # Decide whether to display the game in a window or to use the
        # full screen:
        flag = 0 # Default (window) mode
        
        if config.full_screen:
            flag = FULLSCREEN # Full screen mode
        screen_size = config.screen_size
        screen = pygame.display.set_mode(screen_size, flag)

        self.background = pygame.image.load(config.background_image).convert()
        self.background = pygame.transform.rotate(self.background, 180)
        self.background = pygame.transform.smoothscale(self.background, \
                                                       (809, 456) )

        self.bg_rect = self.background.get_rect()

        pygame.display.set_caption("Pato's Space Invaders")
        pygame.mouse.set_visible(True)

        # The main loop:
        while True:
            start_time = pygame.time.get_ticks()

            # (1) If nextState has been changed, move to the new state, and
            # display it (for the first time):
            if self.state != self.nextState:
                self.state = self.nextState

            # (2) Delegate the event handling to the current state:
            for event in pygame.event.get():
                self.state.handle(event, screen)

            # (3) Update the current state:
            self.state.update(self)

            # (4) Display the current state:
            self.state.display(screen)
             
            delta_time = pygame.time.get_ticks() - start_time
            if delta_time < config.time_speed:
                pygame.time.wait(config.time_speed - delta_time)
            self.state.fps = 1000/(pygame.time.get_ticks()-start_time)

if __name__ == '__main__':
    game = Game(*sys.argv)
    game.run()
