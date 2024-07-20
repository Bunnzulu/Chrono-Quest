import pygame
pygame.init()

WIDTH,HEIGHT = 800,800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
Clock = pygame.time.Clock()

class TSParticles:
    def __init__(self,Surronded_rect_pos:tuple,Flip:bool = False,Rotate:bool = False,Flip_x_y:tuple = (False,False),Rotated_angle:int = 360):
        self.Scalefactor = 4
        self.SRP = Surronded_rect_pos
        self.Flip = Flip
        self.PIndex = 0
        self.Rotate = Rotate
        self.Flip_x_y = Flip_x_y
        self.R = Rotated_angle
        self.Particle1 = pygame.image.load(f"Chrono_imgs/LT100.png").convert_alpha()
        self.Particle2 = pygame.image.load(f"Chrono_imgs/LT101.png").convert_alpha()
        self.Particle3 = pygame.image.load(f"Chrono_imgs/LT102.png").convert_alpha()
        self.Particle4 = pygame.image.load(f"Chrono_imgs/LT103.png").convert_alpha()
        self.Particle5 = pygame.image.load(f"Chrono_imgs/LT104.png").convert_alpha()
        self.Particle6 = pygame.image.load(f"Chrono_imgs/LT105.png").convert_alpha()
        self.Particle7 = pygame.image.load(f"Chrono_imgs/LT106.png").convert_alpha()
        self.Particles1 = [self.Particle1,self.Particle2,self.Particle3,self.Particle4,self.Particle5,self.Particle6,self.Particle7]
        self.Particles1 = [pygame.transform.rotozoom(image,360,1/self.Scalefactor) for image in self.Particles1]
        self.Particles1 = [self.Edit_particle(image) for image in self.Particles1]
        self.Particle = self.Particles1[int(self.PIndex)]
        self.Particle_rect = self.Particle.get_rect(topleft = Surronded_rect_pos)

    def emit(self):
        pygame.display.get_surface().blit(self.Particle,self.Particle_rect)
        self.Animations()

    def Edit_particle(self,image:pygame.Surface):
        if self.Flip:
            image = pygame.transform.flip(image,self.Flip_x_y[0],self.Flip_x_y[1])
        if self.Rotate:
            image = pygame.transform.rotate(image,self.R)
        return image
    
    def Animations(self):
        self.PIndex += 0.1
        if self.PIndex >= len(self.Particles1): self.PIndex = 0
        self.Particle = self.Particles1[int(self.PIndex)]

class TPParticles:
    def __init__(self,PL:int,pos:tuple):
        self.particles = []
        self.size = 8 #width and height
        self.Particle_Limit = PL
        self.pos = pos
    
    def emit(self): #Moves + draws particles
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x -= 1
                pygame.draw.rect(SCREEN,particle[1],particle[0])
    
    def add_particles(self,offset,color):#Adds particles
        pos_x ,pos_y = self.pos
        pos_y += offset
        particle_rect = pygame.Rect(pos_x - self.size/2,pos_y - self.size/2,self.size,self.size)
        self.particles.append((particle_rect,color))

    def delete_particles(self): #deletes particle
        particle_copy = [part for part in self.particles if part[0].x > self.Particle_Limit]
        self.particles = particle_copy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Scaleby = 6
        self.Idle1image = pygame.image.load("Chrono_Sprites\Idle (1).png").convert_alpha()
        self.Idle2image = pygame.image.load("Chrono_Sprites\Idle (2).png").convert_alpha()
        self.Idle3image = pygame.image.load("Chrono_Sprites\Idle (3).png").convert_alpha()
        self.Idle4image = pygame.image.load("Chrono_Sprites\Idle (4).png").convert_alpha()
        self.Idle5image = pygame.image.load("Chrono_Sprites\Idle (5).png").convert_alpha()
        self.Idle6image = pygame.image.load("Chrono_Sprites\Idle (6).png").convert_alpha()
        self.Idle7image = pygame.image.load("Chrono_Sprites\Idle (7).png").convert_alpha()
        self.Idle8image = pygame.image.load("Chrono_Sprites\Idle (8).png").convert_alpha()
        self.Idle9image = pygame.image.load("Chrono_Sprites\Idle (9).png").convert_alpha()
        self.Idle10image = pygame.image.load("Chrono_Sprites\Idle (10).png").convert_alpha()
        self.Idleimagess = [self.Idle1image, self.Idle2image,self.Idle3image, self.Idle4image,self.Idle5image,self.Idle6image,self.Idle7image,self.Idle8image, self.Idle9image,self.Idle10image]
        self.Idleimages = [pygame.transform.scale_by(image, 1/self.Scaleby) for image in self.Idleimagess]
        self.Idle2images = [pygame.transform.flip(image,True,False) for image in self.Idleimages]
        self.Right = True
        self.IdleIndex = 0

        self.Run1image = pygame.image.load("Chrono_Sprites\Run (1).png").convert_alpha()
        self.Run2image = pygame.image.load("Chrono_Sprites\Run (2).png").convert_alpha()
        self.Run3image = pygame.image.load("Chrono_Sprites\Run (3).png").convert_alpha()
        self.Run4image = pygame.image.load("Chrono_Sprites\Run (4).png").convert_alpha()
        self.Run5image = pygame.image.load("Chrono_Sprites\Run (5).png").convert_alpha()
        self.Run6image = pygame.image.load("Chrono_Sprites\Run (6).png").convert_alpha()
        self.Run7image = pygame.image.load("Chrono_Sprites\Run (7).png").convert_alpha()
        self.Run8image = pygame.image.load("Chrono_Sprites\Run (8).png").convert_alpha()
        self.RunIndex = 0
        self.Run2Index = 0
        self.RunImages = [self.Run1image, self.Run2image,self.Run3image, self.Run4image, self.Run5image,self.Run6image, self.Run7image,self.Run8image]
        self.RunImages = [pygame.transform.scale_by(image, 1/self.Scaleby) for image in self.RunImages]
        self.Run2Images = [pygame.transform.flip(image,True,False) for image in self.RunImages]

        self.Jump1image = pygame.image.load("Chrono_Sprites\Jump (1).png").convert_alpha()
        self.Jump2image = pygame.image.load("Chrono_Sprites\Jump (2).png").convert_alpha()
        self.Jump3image = pygame.image.load("Chrono_Sprites\Jump (3).png").convert_alpha()
        self.Jump4image = pygame.image.load("Chrono_Sprites\Jump (4).png").convert_alpha()
        self.Jump5image = pygame.image.load("Chrono_Sprites\Jump (5).png").convert_alpha()
        self.Jump6image = pygame.image.load("Chrono_Sprites\Jump (6).png").convert_alpha()
        self.Jump7image = pygame.image.load("Chrono_Sprites\Jump (7).png").convert_alpha()
        self.Jump8image = pygame.image.load("Chrono_Sprites\Jump (8).png").convert_alpha()
        self.Jump9image = pygame.image.load("Chrono_Sprites\Jump (9).png").convert_alpha()
        self.Jump10image = pygame.image.load("Chrono_Sprites\Jump (10).png").convert_alpha()
        self.JumpImages = [self.Jump1image,self.Jump2image,self.Jump3image,self.Jump4image,self.Jump5image,self.Jump6image,self.Jump7image,self.Jump8image,self.Jump9image,self.Jump10image]
        self.JumpImages = [pygame.transform.scale_by(image, 1/self.Scaleby) for image in self.JumpImages]
        self.Jump2Images = [pygame.transform.flip(image,True,False) for image in self.JumpImages]
        self.JumpIndex = 0

        self.Die1image = pygame.image.load("Chrono_Sprites\Dead (1).png").convert_alpha()
        self.Die2image = pygame.image.load("Chrono_Sprites\Dead (2).png").convert_alpha()
        self.Die3image = pygame.image.load("Chrono_Sprites\Dead (3).png").convert_alpha()
        self.Die4image = pygame.image.load("Chrono_Sprites\Dead (4).png").convert_alpha()
        self.Die5image = pygame.image.load("Chrono_Sprites\Dead (5).png").convert_alpha()
        self.Die6image = pygame.image.load("Chrono_Sprites\Dead (6).png").convert_alpha()
        self.Die7image = pygame.image.load("Chrono_Sprites\Dead (7).png").convert_alpha()
        self.Die8image = pygame.image.load("Chrono_Sprites\Dead (8).png").convert_alpha()
        self.Die9image = pygame.image.load("Chrono_Sprites\Dead (9).png").convert_alpha()
        self.Die10image = pygame.image.load("Chrono_Sprites\Dead (10).png").convert_alpha()
        self.Die11image = pygame.image.load("Chrono_Sprites/Player_Die4.png").convert_alpha()
        self.Die12image = pygame.image.load("Chrono_Sprites/Player_Die5.png").convert_alpha()
        self.Die13image = pygame.image.load("Chrono_Sprites/Player_Die6.png").convert_alpha()
        self.Die14image = pygame.image.load("Chrono_Sprites/Player_Die7.png").convert_alpha()
        self.Die15image = pygame.image.load("Chrono_Sprites/Player_Die8.png").convert_alpha()
        self.Die16image = pygame.image.load("Chrono_Sprites/Player_Die9.png").convert_alpha()
        self.Die17image = pygame.image.load("Chrono_Sprites/Player_Die10.png").convert_alpha()
        self.Die18image = pygame.image.load("Chrono_Sprites/Player_Die11.png").convert_alpha()
        self.DieImages = [self.Die1image,self.Die2image,self.Die3image,self.Die4image,self.Die5image,self.Die6image,self.Die7image,self.Die8image,self.Die9image,self.Die10image,self.Die11image,self.Die12image,self.Die13image,self.Die14image,self.Die15image,self.Die16image,self.Die17image,self.Die18image]
        self.DieImages = [pygame.transform.scale_by(image, 1/self.Scaleby) for image in self.DieImages]
        self.Die2Images = [pygame.transform.flip(image,True,False) for image in self.DieImages]
        self.DieIndex = 0
        self.Died = False

        self.image = self.Idleimages[self.IdleIndex]
        self.rect = self.image.get_rect(center = (400,400))
        self.Direction = pygame.math.Vector2(0,0)
        self.gravity = 1
        self.Jumpforce = 20
        self.Jump = False

        self.TS1N = TSParticles(self.rect.midright)
        self.TS2R = TSParticles(self.rect.bottomright,Rotate=True,Rotated_angle=120)
        self.TS3R = TSParticles(self.rect.midbottom, Rotate=True, Rotated_angle=270)
        self.TS4R = TSParticles(self.rect.bottomleft,Rotate=True,Rotated_angle=40)
        self.TS5F = TSParticles(self.rect.midleft,Flip=True,Flip_x_y=(True,False))
        self.TS6R = TSParticles(self.rect.topleft,Rotate=True,Rotated_angle=300)
        self.TS7R = TSParticles(self.rect.midtop,Rotate=True,Rotated_angle=80)
        self.TS8R = TSParticles(self.rect.topright,Rotate=True,Rotated_angle=30)

        self.TPParticle = TPParticles(self.rect.centerx - 60,self.rect.center)
    
    def Input(self):
        keys = pygame.key.get_pressed()
        if not self.Died:
            if keys[pygame.K_LEFT]:
                self.IdleIndex = 0
                self.RunIndex = 0
                self.Right = False
                if self.rect.x > 0: self.Direction.x = -2
                else: self.Direction.x = 0
                self.Animations()
            elif keys[pygame.K_RIGHT]:
                self.IdleIndex = 0
                self.Right = True
                self.Run2Index = 0
                if self.rect.x < 790: self.Direction.x = 2
                else: self.Direction.x = 0
                self.Animations()
            else:
                self.RunIndex = 0
                self.Run2Index = 0
                self.Direction.x = 0
                self.IdleIndex += 0.1
                if self.IdleIndex >= len(self.Idleimages): self.IdleIndex = 0
                if self.Right: self.image = self.Idleimages[int(self.IdleIndex)]
                elif not self.Right:self.image = self.Idle2images[int(self.IdleIndex)]
            if keys[pygame.K_SPACE] and not self.Jump:
                self.Direction.y = -self.Jumpforce
                self.Jump = True
                self.Animations()

    def Gravity(self):
        if not self.Died:
            self.Direction.y += self.gravity 
            self.rect.y += self.Direction.y

    def Horizontal_Collison(self,Tiles):
        for tile in Tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.Direction.x < 0:
                    self.rect.left = tile.rect.right
                if self.Direction.x > 0:
                    self.rect.right = tile.rect.left
    
    def Vertical_Collison(self, Tiles):
        for tile in Tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.Direction.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.Direction.y = 0 # so that we dont hover on the ceiling
                if self.Direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.Direction.y = 0 # so we dont fall through the floor
                    self.Jump = False

    def Animations(self):
        if not self.Died:
            if self.Jump:
                    self.Right = self.Right
                    self.JumpIndex += 0.1
                    if self.JumpIndex >= len(self.JumpImages): self.JumpIndex = 0
                    if self.Right:
                        self.image = self.JumpImages[int(self.JumpIndex)]
                    elif not self.Right:
                        self.image = self.Jump2Images[int(self.JumpIndex)]
            elif not self.Jump:
                if not self.Right:
                    self.Run2Index += 0.1
                    if self.Run2Index >= len(self.Run2Images): self.Run2Index = 0
                    self.image = self.Run2Images[int(self.Run2Index)]
                elif self.Right:
                    self.RunIndex += 0.1
                    if self.RunIndex >= len(self.RunImages): self.RunIndex = 0
                    self.image = self.RunImages[int(self.RunIndex)]
    
    def Death(self):
        if self.Died:
            self.Direction = pygame.math.Vector2(0,0)
            self.rect.y -= -2
            if self.DieIndex < len(self.DieImages):
                self.DieIndex += 0.1
            if self.DieIndex > len(self.DieImages) - 1:
                self.DieIndex = len(self.DieImages) - 1
            if self.Right:
                self.image = self.DieImages[int(self.DieIndex)]
            elif not self.Right:
                self.image = self.Die2Images[int(self.DieIndex)]
        else: self.DieIndex = 0

    def TSParticles(self):
        self.TS1N.emit()
        self.TS2R.emit()
        self.TS3R.emit()
        self.TS4R.emit()
        self.TS5F.emit()
        self.TS6R.emit()
        self.TS7R.emit()
        self.TS8R.emit()

    def TPParticles(self):
        self.TPParticle.Particle_Limit = self.rect.centerx - 60
        self.TPParticle.pos = (self.rect.left + 10,self.rect.midleft[1])
        self.TPParticle.emit()

    def update(self,Tiles):
        for p,rect_place in ((self.TS1N,self.rect.midright),(self.TS2R,self.rect.bottomright),(self.TS3R,(self.rect.midbottom[0] - 10,self.rect.midbottom[1])),(self.TS4R,(self.rect.bottomleft[0] - 50,self.rect.bottomleft[1])),(self.TS5F,(self.rect.midleft[0]-50,self.rect.midleft[1]- 10)),(self.TS6R,(self.rect.topleft[0] - 30,self.rect.topleft[1] - 50)),(self.TS7R,(self.rect.midtop[0] - 20,self.rect.midtop[1]-50)),(self.TS8R,(self.rect.topright[0],self.rect.topright[1] - 50))):
            p.Particle_rect = p.Particle.get_rect(topleft = rect_place)
        self.rect.x += self.Direction.x
        self.Horizontal_Collison(Tiles)
        self.Gravity()
        self.Vertical_Collison(Tiles)
        self.Input()
        self.Death()

