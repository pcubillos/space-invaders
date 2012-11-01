import pygame, config, os
from numpy import *
from random import randrange

class enemy():

    def __init__(self, pos):
        self.coo_x = array( [75, 72, 77, 83, 88, 85, 83, 77])
        self.coo_y = array( [37, 32, 27, 27, 32, 37, 35, 35])
        self.coo_x += 40*(pos % 7)
        self.coo_y += 30*((pos+7)/7)

        self.isAlive = True
        self.state = 0
        self.dying_time = 6*10
        self.position = pos
        self.di = 0.15
        self.k0 = 0.0
        self.k1 = 0

        self.sound_expl = pygame.mixer.Sound("explosion.wav")

        if random.rand()<0.5:  
            self.dx = -1
        else:
            self.dx =  1

    def checkLimits(self):
        # left limit exeeded
        if self.coo_x[1] < -17:
            self.coo_x = array([-14, -17, -12,  -6,  -1,  -4,  -7, -12])
            self.dx = -self.dx
        # right limit exeeded
        elif self.coo_x[7] > 417:
            self.coo_x = array([404, 401, 406, 412, 417, 414, 411, 406])

    def update(self):
        if self.isAlive:
            if self.state == 0:  # engaged
                self.k0 += self.di # charge k0 till get over 1
                if int(abs(self.k0)) == 1:
                    self.coo_x += int(self.k0) # move
                    self.k1 += 1
                    self.k0  = 0.0
                    if self.k1 == 10: # change direction
                        self.di = -self.di
                        self.k1 -= self.k1

    def shoot(self, prob):
        for i in range(len(self.ammo)):
            if self.isAlive and not self.ammo[i].isAlive:
                if random.rand() < prob:
                    self.ammo[i] = bullet( (self.coo_x[2] + self.coo_x[3])/2, \
                                            self.coo_y[0] + 4                 )
                    self.ammo[i].hooked = False

    def draw(self, screen, color):
        if self.isAlive:
            pygame.draw.polygon(screen, color, \
                                zip(self.coo_x, self.coo_y), 1)
        elif self.dying_time > 0:
            self.dying_time -= 1
            self.r.midtop = (self.coo_x[1] + self.coo_x[4])/2, \
                            (self.coo_y[2] + self.coo_y[0])/2
            screen.blit(self.texto, self.r)
            
    def get_rect(self):
        return self.coo_x[1], self.coo_y[0], self.coo_x[4], self.coo_y[2]

    def kill(self):
        channel_exp = self.sound_expl.play()
        if channel_exp is not None:
            channel_exp.set_volume(0.7, 0.7)
        self.isAlive = False

################ ################ ################ ################ 

class enemy1(enemy):

    def __init__(self, pos):
        enemy.__init__(self, pos)
        font = pygame.font.Font(None, config.font_size_enemy)
        self.texto = font.render(config.death_msg.strip(), \
                                 True, config.color_enemy1 )
        self.r = self.texto.get_rect()

        self.n_ammo = 1
        self.ammo = []
        for i in range(self.n_ammo):
            self.ammo.append(bullet())

    def update(self):
        if self.isAlive:

            if self.state == 0:  # engaged
                enemy.update(self)

            elif self.state == 1:  # free
                if random.rand() >= 0.98: # change direction
                    self.dx =-self.dx
                self.coo_x += self.dx
                self.coo_y += 1
                self.checkLimits()
                if self.coo_y[2] > 450:
                    self.coo_y -= 466
                    
            elif self.state == 2:
                pass
                    
        for arma in self.ammo:
            if arma.isAlive:
                arma.move()

    def draw(self, screen):
        enemy.draw(self, screen, config.color_enemy1)
        for arma in self.ammo:
            if arma.isAlive:
                arma.drawBullet(screen, config.bullet_color)

################ ################ ################ ################ 

class enemy2(enemy):

    def __init__(self, pos):
        enemy.__init__(self, pos)
        font = pygame.font.Font(None, config.font_size_enemy)
        self.texto = font.render(config.death_msg.strip(), \
                                 True, config.color_enemy2 )
        self.r = self.texto.get_rect()
        self.n_ammo = 2
        self.ammo = []
        for i in range(self.n_ammo):
            self.ammo.append(bullet())

    def update(self):
        if self.isAlive:

            if self.state == 0:  # engaged
                enemy.update(self)

            elif self.state == 1:  # free
                if random.rand() >= 0.98: # change direction
                    self.dx =-self.dx
                self.coo_x += self.dx
                self.coo_y += 1
                self.checkLimits()
                if self.coo_y[2] > 450:
                    self.coo_y -= 466

            elif self.state == 2:
                pass
                    
        for arma in self.ammo:
            if arma.isAlive:
                arma.move()

    def shoot(self, prob):
        for i in range(self.n_ammo):
            if self.isAlive and not self.ammo[i].isAlive:
                if random.rand() < prob:
                    self.ammo[i] = bullet( self.coo_x[1 + i*4],  \
                                           self.coo_y[0] + 4 )
                    self.ammo[i].hooked = False

    def draw(self, screen):
        enemy.draw(self, screen, config.color_enemy2)
        for arma in self.ammo:
            if arma.isAlive:
                arma.drawBullet(screen, config.bullet_color)
	


################ ################ ################ ################ 

class starship:

    def __init__(self, nivel):
        self.coo_x = array( [193, 193, 193, 198, 200, 202, 207, 207, 207] )
        self.coo_y = array( [424, 419, 423, 421, 410, 421, 423, 419, 424] )
        self.dv = 0
        self.moving_l = False
        self.moving_r = False
        self.level = 6 - nivel
        self.lives = self.level
        self.isAlive = True
        self.hold = False
        self.ammo_holded = 0
        self.isdead = 6*12
        self.invincible = 0

        self.ammo =[[] for i in range(self.level)] # List of empty lists
        for i in range( len(self.ammo)):
            self.ammo[i] = bullet()

        self.special = [[[] for j in range(config.n_bombs)] \
                            for i in range(config.type_bombs)]
        for i in range(config.type_bombs):
            for j in range(config.n_bombs):
                self.special[i][j] = bomb()

        font = pygame.font.Font(None, config.font_size_hero)
        self.texto = font.render(config.death_msg_hero.strip(),
                                 True, config.color_hero)
        self.r = self.texto.get_rect()
        self.sound_doh = pygame.mixer.Sound("doh.wav")

    def update(self):
        self.coo_x += self.dv
        self.checkLimits()
        for i in range(len(self.ammo)):
            self.ammo[i].move(self.coo_x[4])
        for i in range(config.type_bombs):
            for j in range(config.n_bombs):
                self.special[i][j].move(self.coo_x[4])

        if not self.isAlive:
            self.isdead -= 1
            self.r.midtop = self.coo_x[4] - 5, 420
            if self.isdead == 0: # revive
                self.isdead = 6*12
                self.lives -= 1
                self.invincible = 3*12
                if self.lives != 0:
                    self.isAlive = True

        if self.invincible > 0:
            self.invincible -= 1

    def stop(self):
        self.dv = 0
        self.moving_l = False
        self.moving_r = False

    def draw(self, screen):
        if self.isAlive:
            pygame.draw.polygon(screen, config.color_hero, \
                                zip(self.coo_x, self.coo_y), 1)
        else:
            screen.blit(self.texto, self.r)

        for arma in self.ammo:
            if arma.isAlive:
                arma.drawBullet(screen)

        for i in range(config.type_bombs):
            for j in range(config.n_bombs):
                self.special[i][j].drawBomb(screen)

        for i in range(self.lives-1):
            pygame.draw.polygon(screen, config.color_hero, \
                 zip(config.lives_x + i*config.delta_liv, config.lives_y), 1)

        # plot hit area
#        rec = self.get_rect()
#        pygame.draw.rect(screen, (255,255,255), (rec[0], rec[3], \
#                            rec[2]-rec[0], rec[1]-rec[3]), 1)
#        rec = self.get_rect(True)
#        pygame.draw.rect(screen, (255,255,255), (rec[0], rec[3], \
#                            rec[2]-rec[0], rec[1]-rec[3]), 1)

    def checkLimits(self):
        if self.coo_x[0] < 1:
            self.coo_x = array( [1, 1, 1, 5, 8, 11, 15, 15, 15] )
            self.stop()
        elif self.coo_x[8] > config.screen_size[0]:
            self.coo_x = array([385, 385, 385, 389, 392, 395, 399, 399, 399])
            self.stop()

    def kill(self):
        channel_doh = self.sound_doh.play()
        if channel_doh is not None:
            channel_doh.set_volume(0.4, 0.4)
        self.stop()
        self.hold = False
        self.ammo[self.ammo_holded].hooked = False
        self.isAlive = False

    def get_rect(self, lower=False):
        if not lower:
            return self.coo_x[3], self.coo_y[3], self.coo_x[5], self.coo_y[4]
        else:
            return self.coo_x[0], self.coo_y[0], self.coo_x[8], self.coo_y[1]

################ ################ ################ ################ 

class bullet:

    def __init__(self, pos_x=-10, pos_y=-10):
        self.x = pos_x
        self.y = pos_y
        self.isAlive = True if not pos_x == -10 else False
        self.hooked = True

    def move(self, pos_x=None):
        if pos_x == None: # enemy
            self.y += 5
        else:             # hero
            if not self.hooked:
                self.y -= 5
            else:
                self.x = pos_x

        if self.y > config.screen_size[1] or self.y < 0:
            self.isAlive = False

    def drawBullet(self, screen, color=config.color_bullet ):
        pygame.draw.line(screen, color, (self.x, self.y), (self.x, self.y-5))

    def get_rect(self):
        return self.x, self.y, self.x , self.y - 4

################ ################ ################ ################ 

class bomb:

    def __init__(self, pos_x=-1, pos_y=-1):
        self.x = pos_x
        self.y = pos_y
        self.isAlive = True if not pos_x == -1 else False
        self.status = 0 

    def	move(self, pos_x):
        if self.status == 0: # Falling
            self.y += 2 
            if self.y > 450:
                self.isAlive = False 

        if self.status == 1: # Caught
            self.x = pos_x 
            self.y = 410 

#    def checkHit(x1, x2, y1, y2):
#        return False 	

#    def checkHit(x1, x2, y1, y2, g):
#        return False 
	
#    def drawBomb(Graphics g):
#        if self.status == 0:
#            g.drawRect(self.x-4, self.y-7, 8, 8) 

    def drawBomb(self, screen, color=config.color_bomb):
        if self.status == 0:
            pygame.draw.rect(screen, color, (self.x-4, self.y-7, 9, 9), 1)
        		
    def changeStatus(self, i):
        self.status = i 

    def get_rect(self):
        return self.x-4, self.y+2, self.x+5, self.y-7

################ ################ ################ ################ 

class laser(bomb):

    def __init__(self, pos_x, pos_y):
        bomb.__init__(self, pos_x, pos_y) 
        self.age    = 0 
        self.length = 2 
        self.sound = pygame.mixer.Sound("laser.wav")
        font = pygame.font.Font(None, config.font_size_bomb)
        self.texto = font.render(("L").strip(), True, config.color_laser)
        self.r = self.texto.get_rect()

    def changeStatus(self, i):
        bomb.changeStatus(self, i) 
        if i == 3:
            self.length = 300 
            channel_laser = self.sound.play()
            if channel_laser is not None:
                channel_laser.set_volume(0.4, 0.4)
			
    def move(self, pos_x):
        bomb.move(self, pos_x) 
        if self.status == 2:
            self.age += 1 
            self.length = self.age/4 
            self.x = pos_x
            if self.age > 30:
                self.changeStatus(3)
		
        if self.status == 3:
            self.age += 1
            self.y -= 30
            if self.age > 50:
                self.status = -1
                self.isAlive = False

    def drawBomb(self, screen, color=config.color_laser):
        bomb.drawBomb(self, screen, color)
        if self.status == 0:
            self.r.midbottom = self.x-1, self.y+2
            screen.blit(self.texto, self.r)

        if self.status == 1:
            self.r.midtop = 310, 30
            screen.blit(self.texto, self.r)
		
        if self.status == 2 or self.status == 3:
            screen.fill( config.color_laser, 
                        (self.x-1, self.y-self.length-1, 2, self.length) )
				
    def check_hit(self, x1, y2, x2, y1):
        if self.status == 2 or self.status == 3:
            if self.x-1 <= x2 and x1 <= self.x+1 and \
               self.y-2 >= y1 and y2 >= self.y-self.length-1:
                self.changeStatus(3) 
                return True
        return False
    
    def checkHit(self, rect):
        return self.check_hit(rect[0],rect[1],rect[2],rect[3])
	
################ ################ ################ ################ 

class rocket(bomb):

    def __init__(self, pos_x, pos_y):
        bomb.__init__(self, pos_x, pos_y)
        font = pygame.font.Font(None, config.font_size_hero)
        self.texto = font.render(("R").strip(), True, config.color_bomb)
        self.r = self.texto.get_rect()

    def move(self, pos_x):
        bomb.move(self, pos_x) 		
	
    def drawBomb(self, screen, color=config.color_bomb):
        if self.status == 0:
            pygame.draw.rect(screen, color, (self.x-4, self.y-7, 8, 8)) 
            self.r.midtop = self.x-2, self.y
            screen.blit(self.texto, self.r)

        if self.status == 1:
            self.r.midtop = 330, 30
            screen.blit(self.texto, self.r)
		
        if self.status == 2:
            pass
       
    def check_hit(self, x1, y2, x2, y1):
        return False 	

    def checkHit(self, rect):
        return self.check_hit(rect[0],rect[1],rect[2],rect[3])

################ ################ ################ ################ 

class cluster(bomb):
	
    def __init__(self, pos_x, pos_y):
        bomb.__init__(self, pos_x, pos_y) 
        self.radius = 1 
        self.sound_blast = pygame.mixer.Sound("blast.wav")
        self.sound_throw = pygame.mixer.Sound("bombfall.wav")
        font = pygame.font.Font(None, config.font_size_bomb)
        self.texto = font.render(("C"), True, config.color_cluster)
        self.r = self.texto.get_rect()

    def changeStatus(self, i):
        bomb.changeStatus(self, i) 
        if i == 2:
            channel_throw = self.sound_throw.play()
            if channel_throw is not None:
                channel_throw.set_volume(0.4, 0.4)
        if i == 3:
            self.sound_throw.stop() 
            channel_blast = self.sound_blast.play()
            
    def move(self, pos_x):
        bomb.move(self, pos_x) 
        if self.status == 2:
            self.y -= 2 
            if self.y < 0:
                self.isAlive = False 

        if self.status == 3:
            self.radius += 1 
			
            if self.radius > 45:
                self.status = -1 
                self.isAlive = False 

    def drawBomb(self, screen, color=config.color_cluster):
        bomb.drawBomb(self, screen, color)
        if self.status == 0:
            self.r.midbottom = self.x, self.y+2
            screen.blit(self.texto, self.r)

        if self.status == 1:
            self.r.midtop = 320, 30
            screen.blit(self.texto, self.r)

        if self.status == 2:
            pygame.draw.ellipse(screen, config.color_cluster, \
                               (self.x-1, self.y-3, 5, 6), 1 )
		
        if self.status == 3:
            pygame.draw.circle(screen, config.color_cluster, \
                               (self.x, self.y), (self.radius/2 + 2), 3)
            pygame.draw.circle(screen, config.color_cluster, \
                               (self.x, self.y), (self.radius/5 + 2), 2)
	
    def check_hit(self, x1, y2, x2, y1):
        if self.status == 2:
            if self.x-1 <= x2 and self.x+1 >= x1 and \
               self.y+3 >= y1 and self.y-2 <= y2:
                self.changeStatus(3) 
                return True 
		
        if self.status == 3:  
            if self.x < x1:
                if self.y < y1 or self.y > y2:
                    if pow(self.y-y1, 2) + pow(self.x-x1, 2) \
                       <= pow(self.radius/2.0, 2)            \
                    or pow(self.y-y2, 2) + pow(self.x-x1, 2) \
                       <= pow(self.radius/2.0, 2):
                        return True 
                elif self.x + self.radius/2.0 >= x1:
                    return True 
			
            elif self.x <= x2:
                if ( self.y + self.radius/2.0 >  y1 and \
                     self.y - self.radius/2.0 <= y1) or \
                   ( self.y + self.radius/2.0 >  y2 and \
                     self.y - self.radius/2.0 <= y2 ):
                    return True
				
            else:
                if self.y < y1 or self.y > y2:
                    if pow(self.y-y1, 2) + pow(self.x-x2, 2) \
                       <= pow(self.radius/2.0, 2)            \
                    or pow(self.y-y2, 2) + pow(self.x-x2, 2) \
                       <= pow(self.radius/2.0, 2):
                        return True 
                    
                elif self.x - self.radius/2.0 <= x2:
                    return True 			

        return False

    def checkHit(self, rect):
        return self.check_hit(rect[0],rect[1],rect[2],rect[3])
