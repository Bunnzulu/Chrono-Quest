import pygame, sys
from Player import Player
from Cutscenes import Cutscence, Game_font
pygame.init()
WIDTH,HEIGHT = 800,640#800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chrono Quest")
Clock = pygame.time.Clock()
Cooldown_Timer = pygame.USEREVENT + 1
pygame.time.set_timer(Cooldown_Timer,1000)
Cyborg_Text_Timer = pygame.USEREVENT + 2
pygame.time.set_timer(Cyborg_Text_Timer,100)
Rewind_Forward_Timer = pygame.USEREVENT + 3
pygame.time.set_timer(Rewind_Forward_Timer, 5000)
#100 looks good for Cyborg Text

class Main:
    def __init__(self):
        self.Player = Player()
        self.Cutscences = Cutscence()
        self.Showtime = 100
        self.MovingBlockSpeed = -2
        self.MovingBlockSpeed2 = 2
        self.MovingBlockSpeedSquare = pygame.math.Vector2(2,2)
        self.MovingBlockSpeedSquare2 = pygame.math.Vector2(2,2)
        self.MovingBlockSpeed_y = 2
        self.forward_x, self.forward_y = 0,0
        self.RewindUnlocked = False
        self.Forward = False
        self.Rewind_pos = (0,0)
        self.TSUSED =False
        self.TSShownCooldown = False
        self.TPShownCooldown = False
        self.LV1_Keycode_Interface = False
        self.TPUSED = False
        self.LV8K1_unlocked = False
        self.LV8K2_unlocked = False
        self.LV8K3_unlocked = False
        self.LV8K4_unlocked = False
        self.PlayerStop = False
        self.Door = False
        self.PlayerPause = False
        self.RewindTime = False
        self.pressed = False
        self.count = 0
        self.Time_Stop = False
        self.Player_feet_rect = pygame.Rect(self.Player.rect.midleft,(40,44))
        self.TSCooldown,self.TSTime = 30,10
        self.TPCooldown,self.TPTime = 45,10
        self.TLTime = 15
        self.Time_loop = False
        self.Bullets = pygame.sprite.Group()
        self.TLInfo = {"Player_pos":(0,0), "Stage":"","Tiles":"","Died":self.Player.Died,"Bullets":self.Bullets.sprites()}
        self.PowerStatus = self.TSTime
        self.TLUsed = False
        self.PowerStatus2 = self.TPTime
        self.PowerStatus_color = "Green"
        self.PowerStatus_color2 = "Green"
        self.PowerStatus_Text = Game_font.render(str(self.PowerStatus),True,self.PowerStatus_color)
        self.PowerStatus_Text2 = Game_font.render(str(self.PowerStatus2),True,self.PowerStatus_color2)
        self.TLStatus_Text = Game_font.render(str(self.TLTime),True,"Green")
        self.PowerStatus_rect = self.PowerStatus_Text.get_rect(center = (285,62))
        self.PowerStatus_rect2 = self.PowerStatus_Text2.get_rect(center = (478,62))
        self.TLStatus_rect = self.TLStatus_Text.get_rect(center = (125,61))
        self.SlowDown = 1
        self.FastShooters = self.Cutscences.Level.LV9FastShooter
        self.Shooters = self.Cutscences.Level.Lv7Shooters
        self.DeathDoor = ""
        self.PlayerGroup = pygame.sprite.GroupSingle()
        self.PlayerGroup.add(self.Player)
        self.Index = 0
        self.Yes = False
        self.No = False
        self.TPParticles_on = False
        self.LV17bullets = pygame.sprite.Group()
        self.Yes_rect = pygame.Rect(self.Cutscences.TextBox.centerx - 50,self.Cutscences.TextBox.centery - 100, 50,50)
        self.No_rect = pygame.Rect(self.Cutscences.TextBox.centerx + 50,self.Cutscences.TextBox.centery - 100, 50,50)
        self.Yes_Text = Game_font.render("Yes",True,"Green")
        self.Yes_Text_rect = self.Yes_Text.get_rect(center = self.Yes_rect.center)
        self.No_Text = Game_font.render("No",True,"Red")
        self.No_TexT_rect = self.No_Text.get_rect(center = self.No_rect.center)
        self.Collideing_Tiles = self.Cutscences.Level.Level_1
        self.Player.rect.center = (0,0)
    
    def Draw(self):
        self.Player_feet_rect = pygame.Rect(self.Player.rect.midleft,(40,44))
        self.PowerStatus_Text = Game_font.render(str(self.PowerStatus),True,self.PowerStatus_color)
        self.PowerStatus_Text2 = Game_font.render(str(self.PowerStatus2),True,self.PowerStatus_color2)
        self.TLStatus_Text = Game_font.render(str(self.TLTime),True,"Green")
        self.Cutscences.Stages(self.SlowDown)
        if self.SlowDown == 0.5 or self.TSShownCooldown:
            SCREEN.blit(self.PowerStatus_Text,self.PowerStatus_rect)
        if self.SlowDown == 0 or self.TPShownCooldown:
            SCREEN.blit(self.PowerStatus_Text2,self.PowerStatus_rect2)
        if self.TLUsed:
            SCREEN.blit(self.TLStatus_Text,self.TLStatus_rect)
        if self.RewindTime: self.Gray_Screen()
        self.Player_Draw_Control()
        self.Level_Logic()
        self.Player_death()
        self.Player_Respawn()
        self.Player_Particles()
        self.Bullets.draw(SCREEN)
        print(self.SlowDown)
        self.Bullets.update(self.SlowDown)
        self.LV17bullets.draw(SCREEN)
        self.LV17bullets.update(self.SlowDown)
    
    def Player_Draw_Control(self):
        if self.Cutscences.Stage in ("Start","Black","Finish"): self.Player.rect.center = self.Cutscences.Level.Player_pos
        # elif self.Cutscences.Stage in ("Level 1", "LV1-Cave", "Level 2", "LV2_WC", "Level 3", "Level 4", "Level 5"):
        else:
            self.PlayerGroup.draw(SCREEN)
            self.Player_Respawn()
            self.Player_death()
            if self.Cutscences.Lv1_Cutscene1:
                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"Blue")
                    self.Cutscences.TextBox_Text2 = Game_font.render(self.Cutscences.Text2,True,"Blue")
                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                    SCREEN.blit(self.Cutscences.TextBox_Text2,self.Cutscences.TextBox_Text_rect2)
            if self.Cutscences.Stage == "LV2_WC":
                self.PlayerStop = True
                if 100 >= self.Showtime >= 80:
                    self.Player.rect.center = (161,323)
                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                    self.Cutscences.Text = "Noooooooooo"
                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"Blue")
                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                elif 70 >= self.Showtime >= 40:
                    self.Player.rect.center = (174,381)
                    if self.Showtime == 70: self.PlayerGroup.update(self.Collideing_Tiles)
                elif 30 >= self.Showtime >= 0:
                    self.Player.rect.center = (226,478)
                    if self.Showtime == 30: self.PlayerGroup.update(self.Collideing_Tiles)
                elif -1 >= self.Showtime >= -40:
                    self.RewindTime = True
                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                    self.Cutscences.Text = "What"
                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"Blue")
                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                    self.Cutscences.Lv2_Wrong_Choice_Death = True
                elif -50 >= self.Showtime >= -80:
                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                    self.Cutscences.Text = "Just happened"
                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"Blue")
                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                elif -80 >= self.Showtime >= -130:
                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                    self.Cutscences.Text = "Congrats, player unlocked rewind. Press R to go back 5 seconds in time"
                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"White")
                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                elif -140 >= self.Showtime >= -180:
                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                    self.Cutscences.Text = "Did I just go back in time"
                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"Blue")
                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                elif -190 >= self.Showtime:
                    self.RewindTime = False
                    self.PlayerStop = False
                    self.RewindUnlocked =True
                    self.Cutscences.Stage = "Level 2"
                    self.Player.rect.center = (48,271)
                    self.Collideing_Tiles = self.Cutscences.Level.Level_2
                    self.Showtime = 100.5
                self.Showtime -= 0.5
            if not self.PlayerStop and not self.PlayerPause: self.PlayerGroup.update(self.Collideing_Tiles)
    #Level 1
    def Door_Interactions(self):
        if not self.Player.Died:
            if self.Cutscences.Stage == "Level 1":
                for Door in self.Cutscences.Level.Lv1Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv1ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv1OpenDoors.sprites(): 
                            if Door.Name == "Finish_Door":
                                self.Open_Door_Interaction("Level 2",(35,348),self.Cutscences.Level.Level_2)
                            else:
                                self.Open_Door_Interaction("LV1-Cave",(35,348),self.Cutscences.Level.LV1_Cave)
            
            elif self.Cutscences.Stage == "LV1-Cave":
                for Door in self.Cutscences.Level.LV1CaveOpenDoors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        self.Open_Door_Interaction("Level 1",(703,328),self.Cutscences.Level.Level_1)
            
            elif self.Cutscences.Stage == "Level 2":
                for Door in self.Cutscences.Level.Lv2Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv2ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv2OpenDoors.sprites():
                            if not self.Cutscences.Lv2_Wrong_Choice_Death:
                                self.DeathDoor = Door.Name
                                self.Open_Door_Interaction("LV2_WC", (48,271), self.Cutscences.Level.LV2_WC)
                            else:
                                if Door.Name == self.DeathDoor:
                                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                                    self.Cutscences.Text = "I dont want to do that again"
                                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"Blue")
                                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                                else:
                                    self.Open_Door_Interaction("Level 3", (48,271), self.Cutscences.Level.Level_3)

            elif self.Cutscences.Stage == "Level 3":
                for Door in self.Cutscences.Level.Lv3Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv3ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv3OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 4", (23,430), self.Cutscences.Level.Level_4)

            elif self.Cutscences.Stage == "Level 4":
                for Door in self.Cutscences.Level.Lv4Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv4ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv4OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 5", (28,40), self.Cutscences.Level.Level_5)
            
            elif self.Cutscences.Stage == "Level 5":
                for Door in self.Cutscences.Level.Lv5Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv5ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv5OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 6", (0,0), self.Cutscences.Level.Level_6)
            
            elif self.Cutscences.Stage == "Level 6":
                for Door in self.Cutscences.Level.Lv6Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv6ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv6OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 7", (30,95), self.Cutscences.Level.Level_7)
            
            elif self.Cutscences.Stage == "Level 7":
                for Door in self.Cutscences.Level.Lv7Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv7ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv7OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 8", (33,400), self.Cutscences.Level.Level_8)
            
            elif self.Cutscences.Stage == "Level 8":
                for Door in self.Cutscences.Level.Lv8Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv8ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv8OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 9", (31,89), self.Cutscences.Level.Level_9)
            
            elif self.Cutscences.Stage == "Level 9":
                self.Shooters = self.Cutscences.Level.Lv9Shooters
                for Door in self.Cutscences.Level.Lv9Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv9ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv9OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 10", (0,0), self.Cutscences.Level.Level_10)
            
            elif self.Cutscences.Stage == "Level 10":
                for Door in self.Cutscences.Level.Lv10Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv10ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv10OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 11", (31,109), self.Cutscences.Level.Level_11)
            
            elif self.Cutscences.Stage == "Level 11":
                for Door in self.Cutscences.Level.Lv11Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv11ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv11OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 12", (9,149), self.Cutscences.Level.Level_12)
            
            elif self.Cutscences.Stage == "Level 12":
                for Door in self.Cutscences.Level.Lv12Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv12ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv12OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 13", (38,89), self.Cutscences.Level.Level_13)
            
            elif self.Cutscences.Stage == "Level 13":
                for Door in self.Cutscences.Level.Lv13Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv13ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv13OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 14", (40,549), self.Cutscences.Level.Level_14)
            
            elif self.Cutscences.Stage == "Level 14":
                for Door in self.Cutscences.Level.Lv14Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv14ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv14OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 15", (32,67), self.Cutscences.Level.Level_15)
            
            elif self.Cutscences.Stage == "Level 15":
                for Door in self.Cutscences.Level.Lv15Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv15ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv15OpenDoors.sprites():
                            if Door.Name != "Door3": self.Open_Door_Interaction("Level 15W", (18,501), self.Cutscences.Level.Level_15W)
                            else:
                                self.Open_Door_Interaction("Level 15R", (18,501), self.Cutscences.Level.Level_15R)
            
            elif self.Cutscences.Stage == "Level 15W":
                for Door in self.Cutscences.Level.Lv15WClosedDoors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        self.Closed_Door_Interaction("Wrong way")
            
            elif self.Cutscences.Stage == "Level 15R":
                for Door in self.Cutscences.Level.Lv15ROpenDoors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        self.Open_Door_Interaction("Level 16", (28,40), self.Cutscences.Level.Level_16)
            
            elif self.Cutscences.Stage == "Level 16":
                for Door in self.Cutscences.Level.Lv16Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv16ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv16OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 17", (38,89), self.Cutscences.Level.Level_17)   

            elif self.Cutscences.Stage == "Level 17":
                for Door in self.Cutscences.Level.Lv17Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv17ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv17OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 18", (31,109), self.Cutscences.Level.Level_18)     

            elif self.Cutscences.Stage == "Level 18":
                for Door in self.Cutscences.Level.Lv18Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv18ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv18OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 19", (38,382), self.Cutscences.Level.Level_19)

            elif self.Cutscences.Stage == "Level 19":
                for Door in self.Cutscences.Level.Lv19Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv19ClosedDoors.sprites():self.Closed_Door_Interaction()
                        elif Door in self.Cutscences.Level.Lv19OpenDoors.sprites():
                            self.Open_Door_Interaction("Level 20", (34,34), self.Cutscences.Level.Level_19)

            elif self.Cutscences.Stage == "Level 20":
                for Door in self.Cutscences.Level.Lv20Doors.sprites():
                    if pygame.sprite.collide_rect(Door, self.PlayerGroup.sprite):
                        self.Cutscences.Interactions("Try")
                        if Door in self.Cutscences.Level.Lv20OpenDoors.sprites():
                            self.Open_Door_Interaction("Finish",(40,4),self.Cutscences.Level.Level_20)
            
    def Gray_Screen(self):
        SCREEN.fill("Gray")
        self.PlayerStop = True
    
    def Closed_Door_Interaction(self,Text:str ="This Door Seems to be locked" ):
        mouse_pos = pygame.mouse.get_pos()
        if self.Cutscences.OptionButton.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    self.PlayerStop = True
        if self.PlayerStop:
            if self.Showtime > 0:
                pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                self.Cutscences.TextBox_Text = Game_font.render(Text,True,"White")
                SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)  
                self.Showtime -= 1  
            else: self.PlayerStop = False; self.Showtime = 100

    def Open_Door_Interaction(self, Destination:str,pos:tuple, Tiles):
        mouse_pos = pygame.mouse.get_pos()
        if self.Cutscences.OptionButton.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.Door = True
                    self.pressed = False
        if self.Door:
            pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
            self.Cutscences.TextBox_Text = Game_font.render("This seems open, Open Door?",True,"White")
            SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
            pygame.draw.rect(SCREEN,"Silver",self.Yes_rect)
            pygame.draw.rect(SCREEN,"Silver",self.No_rect)
            SCREEN.blit(self.Yes_Text, self.Yes_Text_rect)
            SCREEN.blit(self.No_Text,self.No_TexT_rect)
            self.Check_No_Option()
            self.Check_Yes_Option()
            if self.No: self.Door = False; self.No = False
            elif self.Yes:
                self.Time_Stop = False
                self.Yes = False
                self.Door = False
                self.Bullets.empty()
                self.Cutscences.Stage = Destination
                self.Player.rect.center,self.Cutscences.Level.Player_pos = pos,pos
                self.Collideing_Tiles = Tiles

    def Check_Yes_Option(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.Yes_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.Yes = True
                    self.pressed = False
    
    def Check_No_Option(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.No_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.No = True
                    self.pressed = False

    def Puzzle_Keys(self):
        if self.Cutscences.Stage == "Level 1":
            for Lock in self.Cutscences.Level.Lv1Locks.sprites():
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    if Lock.Name == "KeyCode":
                        self.LV1_puzzle()
                        if self.LV1_Keycode_Interface:
                            self.Cutscences.Level.L1_KeyCode(SCREEN)
                            if self.Cutscences.Level.Exit: 
                                self.LV1_Keycode_Interface = False
                                self.Cutscences.Level.Exit = False
                    else: self.DoorInt_Interactions("green")
        elif self.Cutscences.Stage == "LV1-Cave":
            if self.Player.rect.colliderect(self.Cutscences.Level.Lv1PasswordPaper_rect):
                pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                self.Cutscences.TextBox_Text = Game_font.render("There seems to be something on the floor. Inspect?",True,"White")
                SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                pygame.draw.rect(SCREEN,"Silver",self.Yes_rect)
                pygame.draw.rect(SCREEN,"Silver",self.No_rect)
                SCREEN.blit(self.Yes_Text, self.Yes_Text_rect)
                SCREEN.blit(self.No_Text,self.No_TexT_rect)
                self.Check_No_Option()
                self.Check_Yes_Option()
                if self.No:self.No = False
                elif self.Yes:
                    self.Cutscences.Level.Paper = True
                    self.Yes = False
                self.Cutscences.Level.LV1Cave_Paper()
                if self.Cutscences.Level.Paper:
                    pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                    self.Cutscences.TextBox_Text = Game_font.render(self.Cutscences.Text,True,"Blue")
                    SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)
                    if len(self.Cutscences.Text) >= 58: SCREEN.blit(self.Cutscences.Next_Text,self.Cutscences.Next_Text_rect)    
        elif self.Cutscences.Stage == "Level 3":
            for Lock in self.Cutscences.Level.Lv3Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            if self.Player.rect.colliderect(self.Cutscences.Level.ForwardSymbol_rect) and not self.Cutscences.ForwardUnlocked:
                self.PlayerPause = True
                self.Cutscences.Cyborg_Text("Another Medallion?", "Blue")
                self.Showtime -= 0.5
                if pygame.KEYDOWN and self.Showtime <= 40:
                    self.Cutscences.ForwardScene = True
                if self.Cutscences.ForwardScene:
                    self.Cutscences.Cyborg_Text("Player has unlocked Forward, press F to move 5 seconds into the future.", "White",Text2="CAUTION-UNSTABLE")
                    if pygame.KEYDOWN and self.Showtime <= -10: 
                        self.Cutscences.ForwardUnlocked = True
                        self.PlayerPause = False
                        self.Showtime = 100
            self.Death(self.Cutscences.Level.LV3_DeadlyBlocks)
        elif self.Cutscences.Stage == "Level 4":
            for Lock in self.Cutscences.Level.Lv4Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV4DeadlyBlocks)
            self.HoverBlocks(98,430,self.Cutscences.Level.LV4MovingBlocks)
        elif self.Cutscences.Stage == "Level 5":
            for Lock in self.Cutscences.Level.Lv5Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.HoverBlocks(250,642,self.Cutscences.Level.LV5MovingBlocks)
            self.Death(self.Cutscences.Level.LV5DeadlyBlocks)
        elif self.Cutscences.Stage == "Level 6":
            for Lock in self.Cutscences.Level.Lv6Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.PlayerPause = False
            if self.Player.rect.colliderect(self.Cutscences.Level.TimeSlow_rect) and not self.Cutscences.TS_Unlocked:
                self.PlayerPause = True
                self.Showtime -= 0.5
                if self.Showtime <= 90:
                    self.Cutscences.TS_Scene = True
                if self.Cutscences.TS_Scene:
                    self.Cutscences.Cyborg_Text("Player has unlocked Time Slow, press S to slow down time for 10 seconds", "White","Cooldown:30s")
                if self.Showtime <= -10: 
                    self.Cutscences.TS_Unlocked = True
                    self.PlayerPause = False
                    self.Showtime = 100
            self.Death(self.Cutscences.Level.LV6DeadlyBlocks)
            self.HoverBlocks(98,162,self.Cutscences.Level.LV6MovingBlocks2)
            self.HoverBlocks2(192,352,self.Cutscences.Level.LV6MovingBlocks1)
            self.HoverBlocksSquare((544,192),(416,192),(544,448),(416,448),self.Cutscences.Level.LV6MovingBlocksSquare)
        elif self.Cutscences.Stage == "Level 7":
            for Lock in self.Cutscences.Level.LV7Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV7DeadlyBlocks)
            self.HoverBlocks(158,609,self.Cutscences.Level.LV7MovingBlocks)
        elif self.Cutscences.Stage == "Level 8":
            for Lock in self.Cutscences.Level.LV8Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    if (Lock.Name == "K1" and not self.LV8K1_unlocked) or (Lock.Name == "K2" and not self.LV8K2_unlocked) or (Lock.Name == "K3" and not self.LV8K3_unlocked) or (Lock.Name == "K4" and not self.LV8K4_unlocked):
                        self.DoorInt_Interactions("Red")
                    elif (Lock.Name == "K1" and self.LV8K1_unlocked) or (Lock.Name == "K2" and self.LV8K2_unlocked) or (Lock.Name == "K3" and self.LV8K3_unlocked) or (Lock.Name == "K4" and self.LV8K4_unlocked):
                        self.DoorInt_Interactions("Green")
                if (self.LV8K1_unlocked and Lock.Name == "K1") or (self.LV8K2_unlocked and Lock.Name == "K2") or (self.LV8K3_unlocked and Lock.Name == "K3") or (self.LV8K4_unlocked and Lock.Name == "K4"):
                    Lock.image = self.Cutscences.Level.Lv1Locks.sprites()[1].image
            self.HoverBlocksSquare((416,160),(192,160),(416,416),(192,416),self.Cutscences.Level.LV8MovingBlocks)
            for Block in self.Cutscences.Level.LV8MovingBlocks.sprites():
                if self.Player.rect.bottom == Block.rect.top and Block.rect.colliderect(self.Player_feet_rect):
                    match Block.Name:
                        case "K1":self.LV8K1_unlocked = True
                        case "K2":self.LV8K2_unlocked = True
                        case "K3":self.LV8K3_unlocked = True
                        case "K4":self.LV8K4_unlocked = True
            if self.LV8K1_unlocked and self.LV8K2_unlocked and self.LV8K3_unlocked and self.LV8K4_unlocked:
                for Door in self.Cutscences.Level.Lv8ClosedDoors.sprites():
                    if Door.Name == "Finish_Door":
                        self.Cutscences.Level.Lv8OpenDoors.add(Door)
                        self.Cutscences.Level.Lv8ClosedDoors.remove(Door)
        elif self.Cutscences.Stage == "Level 9":
            for Lock in self.Cutscences.Level.LV9Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV9DeadlyBlocks)
            self.HoverBlocks(225,547,self.Cutscences.Level.LV9MovingBlocks2)
            self.HoverBlocks_y(95,254,self.Cutscences.Level.LV9MovingBlocks1)
        elif self.Cutscences.Stage == "Level 10":
            for Lock in self.Cutscences.Level.LV10Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV10DeadlyBlocks)
            self.HoverBlocks_y(160,450,self.Cutscences.Level.LV10MovingBlocks)
            if self.Player.rect.colliderect(self.Cutscences.Level.TimeStop_rect) and not self.Cutscences.Level.TPunlocked:
                self.PlayerPause = True
                self.Showtime -= 0.5
                if self.Showtime <= 90:
                    self.Cutscences.TP_Scene = True
                if self.Cutscences.TP_Scene:
                    self.Cutscences.Cyborg_Text("Player has unlocked Time Pause, press P to pause time for 10 seconds", "White","Cooldown:45s")
                if self.Showtime <= -10: 
                    self.Cutscences.Level.TPunlocked = True
                    self.PlayerPause = False
                    self.Showtime = 100
            if self.Cutscences.Level.LV10SawDisplay:
                self.Death(self.Cutscences.Level.LV10Saws1)
            else:
                self.Death(self.Cutscences.Level.LV10Saws2)
        elif self.Cutscences.Stage == "Level 11":
            for Lock in self.Cutscences.Level.LV11Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV11DeadlyBlocks)
            self.Death(self.Cutscences.Level.LV11Saw)
            self.Cutscences.Level.LV11Saw.add(self.Cutscences.Level.LV11Saws.sprites()[self.Index])
        elif self.Cutscences.Stage == "Level 12":
            for Lock in self.Cutscences.Level.Lv12Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV12DeadlyBlocks)
            if self.Cutscences.Level.LV12BlackActiver.sprite.rect.colliderect(self.Player_feet_rect) and self.Player.rect.bottom == self.Cutscences.Level.LV12BlackActiver.sprite.rect.top:
                self.Cutscences.Level.LV12Black_on = True
            elif self.Cutscences.Level.LV12WhiteActiver.sprite.rect.colliderect(self.Player_feet_rect) and self.Player.rect.bottom == self.Cutscences.Level.LV12WhiteActiver.sprite.rect.top:
                self.Cutscences.Level.LV12Black_on = False
            if not self.Cutscences.Level.LV12Black_on:
                self.HoverBlocks_y(164,511,self.Cutscences.Level.LV12WhiteMovingBlocks)
            elif self.Cutscences.Level.LV12Black_on:
                self.HoverBlocks_y(91,475,self.Cutscences.Level.LV12BlackMovingBlocks)
            self.HoverBlocks(398,600,self.Cutscences.Level.LV12MovingBlocks1)
            self.HoverBlocks2(381,578,self.Cutscences.Level.LV12MovingBlocks2)
        elif self.Cutscences.Stage == "Level 13":
            for Lock in self.Cutscences.Level.LV13Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV13DeadlyBlocks)
        elif self.Cutscences.Stage == "Level 14":
            self.Shooters = self.Cutscences.Level.Lv14Shooters
            self.FastShooters = self.Cutscences.Level.LV14FastShooters
            for Lock in self.Cutscences.Level.LV14Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV14DeadlyBlocks)
            self.HoverBlocksSquare((577,96),(58,96),(577,448),(58,448),self.Cutscences.Level.LV14MovingBlocks)
        elif self.Cutscences.Stage == "Level 15":
            for Lock in self.Cutscences.Level.Lv15Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            if self.Player.rect.colliderect(self.Cutscences.Level.TimeLoop_rect) and not self.Cutscences.TL_unlocked:
                self.PlayerPause = True
                self.Showtime -= 0.5
                if self.Showtime <= 90:
                    self.Cutscences.TL_Scene = True
                if self.Cutscences.TL_Scene:
                    self.Cutscences.Cyborg_Text("Time Loop unlocked,Press L to start loop, Use Now!", "White","No Cooldown")
                if self.Showtime <= -10: 
                    self.Cutscences.TL_unlocked = True
                    self.PlayerPause = False
                    self.Showtime = 100
        elif self.Cutscences.Stage == "Level 15W":
            self.Death(self.Cutscences.Level.LV15WDeadlyBlocks)
        elif self.Cutscences.Stage == "Level 15R":
            self.Death(self.Cutscences.Level.LV15RDeadlyBlocks)
        elif self.Cutscences.Stage == "Level 16":
            for Lock in self.Cutscences.Level.Lv16Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.HoverBlocks(197,381,self.Cutscences.Level.LV16MovingBlocks)
            self.Death(self.Cutscences.Level.LV16DeadlyBlocks)
        elif self.Cutscences.Stage == "Level 17":
            for Lock in self.Cutscences.Level.LV17Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV17DeadlyBlocks)
        elif self.Cutscences.Stage == "Level 18":
            for Lock in self.Cutscences.Level.LV18Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV18DeadlyBlocks)
            self.HoverBlocksSquare((373,122),(223,122),(373,272),(223,272),self.Cutscences.Level.LV18Saws)
            self.HoverBlocksSquare2((590,122),(481,122),(590,272),(481,272),self.Cutscences.Level.LV18Saws2)
        elif self.Cutscences.Stage == "Level 19":
            self.Shooters = self.Cutscences.Level.Lv19Shooters
            for Lock in self.Cutscences.Level.LV19Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV19DeadlyBlocks)
            self.HoverBlocks(83,647,self.Cutscences.Level.LV19MovingBlocks)
        elif self.Cutscences.Stage == "Level 20":
            for Lock in self.Cutscences.Level.LV20Locks:
                if pygame.sprite.collide_rect(self.PlayerGroup.sprite, Lock):
                    self.Cutscences.Interactions("Inspect")
                    self.DoorInt_Interactions("Green")
            self.Death(self.Cutscences.Level.LV20DeadlyBlocks)
            
    def DoorInt_Interactions(self, SignColor:str):
        mouse_pos = pygame.mouse.get_pos()
        if self.Cutscences.OptionButton.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    self.PlayerStop = True
        if self.PlayerStop:
            if self.Showtime > 0:
                pygame.draw.rect(SCREEN,"Black",self.Cutscences.TextBox)
                self.Cutscences.TextBox_Text = Game_font.render(f"This seems to emit a {SignColor} glow",True,"White")
                SCREEN.blit(self.Cutscences.TextBox_Text,self.Cutscences.TextBox_Text_rect)  
                self.Showtime -= 1  
            else: self.PlayerStop = False; self.Showtime = 100
    
    def LV1_puzzle(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.Cutscences.OptionButton.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    self.LV1_Keycode_Interface = True

    def HoverBlocks(self, Limit1:int, Limit2:int, HoverBlocks:pygame.sprite.Group):
        for Index,Tile in enumerate(HoverBlocks.sprites()):
                Tile.rect.x += ((self.MovingBlockSpeed)*self.SlowDown)
                if Index == 0 and (Tile.rect.x <= Limit1 or Tile.rect.x >= Limit2):
                    self.MovingBlockSpeed = -(self.MovingBlockSpeed)
    
    def HoverBlocks2(self, Limit1:int, Limit2:int, HoverBlocks:pygame.sprite.Group):
        for Tile in HoverBlocks.sprites():
                Tile.rect.x += (self.MovingBlockSpeed2*self.SlowDown)
                if Tile.rect.x <= Limit1 or Tile.rect.x >= Limit2:
                    self.MovingBlockSpeed2 = -(self.MovingBlockSpeed2)

    def HoverBlocks_y(self,Limit1:int, Limit2:int, HoverBlocks:pygame.sprite.Group):
        for Tile in HoverBlocks.sprites():
            Tile.rect.y += (self.MovingBlockSpeed_y*self.SlowDown)
            if Tile.rect.y <= Limit1 or Tile.rect.y >= Limit2:
                self.MovingBlockSpeed_y = -(self.MovingBlockSpeed_y)

    def HoverBlocksSquare(self, TR:int,TL:int,BR:int,BL:int,HoverBlock:pygame.sprite.Group):
        for block in HoverBlock.sprites():
            if block.rect.topleft[0] > TL[0] and block.rect.topleft[1] == TR[1]: #Its y is 1 higher than intended:
                block.rect.x += (-(self.MovingBlockSpeedSquare.x)*self.SlowDown)
            elif (block.rect.topleft[0] == TL[0]) and block.rect.topleft[1] < BL[1]:
                block.rect.y += (self.MovingBlockSpeedSquare.y*self.SlowDown)
            elif block.rect.topleft[0] < BR[0] and block.rect.topleft[1] == BL[1]:
                block.rect.x += (self.MovingBlockSpeedSquare.x*self.SlowDown) 
            elif block.rect.topleft[0] == BR[0] and block.rect.topleft[1] > TR[1]:
                block.rect.y += (-(self.MovingBlockSpeedSquare.y)*self.SlowDown)
        for block in HoverBlock.sprites():
            if block.rect.topleft[1] + 1 == TR[1]:
                block.rect = block.image.get_rect(topleft = (block.rect.topleft[0],TR[1]))
            elif block.rect.topleft[0] + 1 == TL[0]:
                block.rect = block.image.get_rect(topleft = (TL[0],block.rect.topleft[1]))
            elif block.rect.topleft[1] - 1 == BL[1]:
                block.rect = block.image.get_rect(topleft = (block.rect.topleft[0],BL[1]))
            elif block.rect.topleft[0] - 1 == BR[0]:
                block.rect = block.image.get_rect(topleft = (BR[0],block.rect.topleft[1]))
    
    def HoverBlocksSquare2(self, TR:int,TL:int,BR:int,BL:int,HoverBlock:pygame.sprite.Group):
        for block in HoverBlock.sprites():
            if block.rect.topleft[0] > TL[0] and block.rect.topleft[1] == TR[1]: #Its y is 1 higher than intended:
                block.rect.x += (-(self.MovingBlockSpeedSquare2.x)*self.SlowDown)
            elif (block.rect.topleft[0] == TL[0]) and block.rect.topleft[1] < BL[1]:
                block.rect.y += (self.MovingBlockSpeedSquare2.y*self.SlowDown)
            elif block.rect.topleft[0] < BR[0] and block.rect.topleft[1] == BL[1]:
                block.rect.x += (self.MovingBlockSpeedSquare2.x*self.SlowDown) 
            elif block.rect.topleft[0] == BR[0] and block.rect.topleft[1] > TR[1]:
                block.rect.y += (-(self.MovingBlockSpeedSquare2.y)*self.SlowDown)
        for block in HoverBlock.sprites():
            if block.rect.topleft[1] + 1 == TR[1]:
                block.rect = block.image.get_rect(topleft = (block.rect.topleft[0],TR[1]))
            elif block.rect.topleft[0] + 1 == TL[0]:
                block.rect = block.image.get_rect(topleft = (TL[0],block.rect.topleft[1]))
            elif block.rect.topleft[1] - 1 == BL[1]:
                block.rect = block.image.get_rect(topleft = (block.rect.topleft[0],BL[1]))
            elif block.rect.topleft[0] - 1 == BR[0]:
                block.rect = block.image.get_rect(topleft = (BR[0],block.rect.topleft[1]))

    def Level_Logic(self):
        if self.Cutscences.Stage in ("Level 1", "LV1-Cave"):
            if self.Cutscences.Level.LV1Success:
                for Door in self.Cutscences.Level.Lv1ClosedDoors.sprites():
                    if Door.Name == "Finish_Door":
                        self.Cutscences.Level.Lv1OpenDoors.add(Door)
                        self.Cutscences.Level.Lv1ClosedDoors.remove(Door)
        self.Door_Interactions()
        self.Puzzle_Keys()
    
    def Death(self,DeathBlocks:pygame.sprite.Group):
        if not self.Time_Stop:
            for deathblock in DeathBlocks.sprites():
                if self.Player.rect.colliderect(deathblock): self.Player.Died = True

    def RoboShoot(self,Shooters:pygame.sprite.Group):
        for monster in Shooters.sprites():
            self.Bullets.add(monster.Bullet())

    def LV17Shoot(self):
        for monster in self.Cutscences.Level.Lv17Shooters.sprites():
            self.LV17bullets.add(monster.Bullet())

    def RoboBullets(self):
        for bullet in self.Bullets.sprites():
                if not self.Time_Stop:
                    if self.Player.rect.colliderect(bullet.rect):
                        self.Player.Died = True
                for block in self.Collideing_Tiles.sprites():
                    if bullet.rect.y < -40 or block.rect.colliderect(bullet.rect) or bullet.rect.x < -40: 
                        bullet.kill()
 
    def LV17RoboBullets(self):
        for bullet in self.LV17bullets.sprites():
            if self.Player.rect.colliderect(bullet.rect):
                if self.Player.Direction.y < 0:
                    self.Player.rect.top = bullet.rect.bottom
                    self.Player.Direction.y = 0 # so that we dont hover on the ceiling
                if self.Player.Direction.y > 0:
                    self.Player.rect.bottom = bullet.rect.top
                    self.Player.Direction.y = 0 # so we dont fall through the floor
                    self.Player.Jump = False
            for block in self.Collideing_Tiles.sprites():
                if bullet.rect.y < -40 or block.rect.colliderect(bullet.rect) or bullet.rect.x < -40: 
                    bullet.kill()

    def Player_death(self):
        if self.Player.Died:
            if self.Player.rect.centery > 610:
                self.Player.Died = False
                self.Player.image = self.Player.Idle1image
                self.Player.rect.center = self.Cutscences.Level.Player_pos
                self.Player.TPParticle.particles.clear()

    def Player_Particles(self):
        if self.TSUSED:
            self.Player.TSParticles()
        elif self.TPParticles_on:
            self.Player.TPParticles()
        else:
            self.Player.TPParticle.particles.clear()

    def Player_Respawn(self):
        if self.Player.rect.centery > 640 or self.Player.rect.centery < -300:
            if not self.Player.Died: self.Player.rect.center = self.Cutscences.Level.Player_pos

main = Main()         
TurretGun = pygame.USEREVENT + 4
pygame.time.set_timer(TurretGun,800)
FastGun = pygame.USEREVENT + 5
pygame.time.set_timer(FastGun,1800)
LV10SawDisplay = pygame.USEREVENT + 6
pygame.time.set_timer(LV10SawDisplay,500)
PARTICLEEVENT = pygame.USEREVENT +7
pygame.time.set_timer(PARTICLEEVENT,10)
LV11SawDisplay = pygame.USEREVENT + 8
pygame.time.set_timer(LV11SawDisplay,250)
LV13BoxFall = pygame.USEREVENT + 9
pygame.time.set_timer(LV13BoxFall,1300)
LV16BoxFall = pygame.USEREVENT + 10
pygame.time.set_timer(LV16BoxFall,5000)
LV17TurretGun = pygame.USEREVENT + 11
pygame.time.set_timer(LV17TurretGun,1600)
timer_set = False
slow_set = False
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == Cyborg_Text_Timer and main.Cutscences.Stage == "LV1-Cave" and main.Cutscences.Level.Paper:
            main.Cutscences.Text = main.Cutscences.Cutscene_Text(main.Index,"Looks like a code and a weird medallion,    looks cool tho",main.Cutscences.Text)
            main.Index += 1
        
        if e.type == pygame.KEYDOWN and len(main.Cutscences.Text) >= 58 and main.Cutscences.Stage == "LV1-Cave"and main.Cutscences.Level.Paper:
            main.Index = 0
            main.Cutscences.Level.Paper = False
            main.Cutscences.Text = ""
        
        if e.type == Rewind_Forward_Timer:
            main.Rewind_pos = main.Player.rect.center

        if e.type == PARTICLEEVENT:
            if main.TPParticles_on and not main.Player.Died:
                for offset,Color in ((-36,"Gold"),(-28,"Silver"),(-20,"Gold"),(-12,"Silver"),(-4,"Gold"),(4,"Silver"),(12,"Gold"),(20,"Silver"),(28,"Gold"),(36,"Silver")):
                    main.Player.TPParticle.add_particles(offset,Color)

        if main.Cutscences.Stage in ("Level 7","Level 9","Level 14","Level 19"):
            if not main.Time_Stop:
                if e.type == TurretGun:
                    main.RoboShoot(main.Shooters)
                if main.Cutscences.Stage in ("Level 9","Level 14"):
                    if e.type == FastGun:
                        main.RoboShoot(main.FastShooters)
                main.RoboBullets()
        if main.Cutscences.Stage == "Level 17":
            if not main.Time_Stop:
                if e.type == LV17TurretGun:
                    main.LV17Shoot()
            main.LV17RoboBullets()

        if main.Cutscences.Stage == "Level 10":
            if e.type == LV10SawDisplay and not main.Time_Stop:
                main.Index = 0
                main.Cutscences.Level.LV10SawDisplay = not(main.Cutscences.Level.LV10SawDisplay)
        if main.Cutscences.Stage == "Level 11":
            if e.type == LV11SawDisplay and not main.Time_Stop:
                main.Index += 1
                if main.Index >= len(main.Cutscences.Level.LV11Saws): main.Index = 0
        
        if main.Cutscences.Stage == "Level 13":
            if e.type == LV13BoxFall and not main.Time_Stop:
                for Box in (main.Cutscences.Level.LV13Box1,main.Cutscences.Level.LV13Box2,main.Cutscences.Level.LV13Box3,main.Cutscences.Level.LV13Box4,main.Cutscences.Level.LV13Box5,main.Cutscences.Level.LV13Box6):
                    main.Cutscences.Level.LV13Boxes.add(Box.NewBlock())
        
        if main.Cutscences.Stage == "Level 16":
            if e.type == LV16BoxFall and not main.Time_Stop:
                main.Cutscences.Level.LV16Boxes.add(main.Cutscences.Level.LV16Box.NewBlock())

        if main.Cutscences.TS_Unlocked and (main.TSUSED or main.TSShownCooldown):
            if main.TSTime == 0:
                main.TSShownCooldown = True
                main.SlowDown = 1
                main.TSUSED = False
                main.PowerStatus = (f"Cooldown: {main.TSCooldown}")
                main.PowerStatus_color = "Red"
                if not timer_set:
                    pygame.time.set_timer(TurretGun,800)
                    pygame.time.set_timer(FastGun,1800)
                    pygame.time.set_timer(LV10SawDisplay,500)
                    pygame.time.set_timer(LV13BoxFall,1300)
                    pygame.time.set_timer(LV16BoxFall,5000)
                    pygame.time.set_timer(LV17TurretGun,1600)
                    timer_set = True    
            if e.type == Cooldown_Timer:
                if main.TSTime > 0:
                    main.TSTime -= 1
                    main.PowerStatus = main.TSTime
                elif main.TSCooldown > 0 and main.TSShownCooldown:
                    main.TSCooldown -= 1
                    main.PowerStatus = (f"Cooldown: {main.TSCooldown}")
                if main.TSCooldown == 0:
                    main.TSCooldown = 30
                    main.TSTime = 10
                    main.TSUSED = False
                    timer_set = False
                    main.TSShownCooldown = False
                    main.PowerStatus_color = "Green"
                    main.PowerStatus = main.TSTime

        if main.Cutscences.Level.TPunlocked and main.TPUSED:
            if main.TPTime == 0:
                main.TPShownCooldown = True
                main.PowerStatus2 = (f"Cooldown: {main.TPCooldown}")
                main.PowerStatus_color2 = "Red"
                main.TPParticles_on = False
                if not slow_set: main.SlowDown = 1; slow_set = True
                main.Time_Stop = False
            if e.type == Cooldown_Timer:
                if main.TPTime > 0:
                    main.TPTime -= 1
                    main.PowerStatus2 = main.TPTime
                elif main.TPCooldown > 0 and main.TPShownCooldown:
                    main.TPCooldown -= 1
                    main.PowerStatus2 = (f"Cooldown: {main.TPCooldown}")
                if main.TPCooldown == 0:
                    main.TPCooldown = 45
                    main.TPTime = 10
                    main.TPUSED = False
                    main.TPShownCooldown = False
                    main.PowerStatus_color2 = "Green"
                    main.PowerStatus2 = main.TPTime

        if main.Cutscences.TL_unlocked and main.TLUsed:
            if main.TLTime == 0:
                main.Player.rect.center=main.TLInfo['Player_pos']
                main.Cutscences.Stage= main.TLInfo['Stage']
                main.Collideing_Tiles = main.TLInfo['Tiles'] 
                main.Player.Died = main.TLInfo['Died']
                main.Bullets.empty()
                for sprite in main.TLInfo["Bullets"]:
                    main.Bullets.add(sprite)
                main.TLUsed = False
                main.Time_loop = False
                main.TLTime = 15
            if e.type == Cooldown_Timer:
                if main.TLTime > 0:
                    main.TLTime -= 1
                    main.TLStatus_Text = main.TLTime

        if e.type == pygame.KEYDOWN:
            if not main.Player.Died:
                if main.RewindUnlocked:
                    if e.key == pygame.K_r and not main.Time_Stop:
                        main.Gray_Screen()
                        main.Player.rect.center = main.Rewind_pos
                        main.PlayerStop = False
                if main.Cutscences.ForwardUnlocked:
                    if e.key == pygame.K_f and main.Rewind_pos is not None and not main.Time_Stop:
                        main.forward_x = main.Player.rect.center[0] + (main.Player.rect.center[0] - main.Rewind_pos[0])
                        main.forward_y = main.Player.rect.center[1] + (main.Player.rect.center[1] - main.Rewind_pos[1])
                        if main.forward_y > 541: main.forward_y = 541
                        if main.forward_y < 0: main.forward_y = 0
                        main.Player.rect.center = (main.forward_x, main.forward_y)
                if main.Cutscences.TS_Unlocked:
                    if e.key == pygame.K_s:
                        if main.TSTime == 10 and not main.Time_Stop:
                            main.SlowDown = 0.5
                            main.TSUSED = True
                            pygame.time.set_timer(TurretGun,1600)
                            pygame.time.set_timer(FastGun,3600)
                            pygame.time.set_timer(LV10SawDisplay,1000)
                            pygame.time.set_timer(LV11SawDisplay,500)
                            pygame.time.set_timer(LV13BoxFall,2600)
                            pygame.time.set_timer(LV16BoxFall,10000)
                            pygame.time.set_timer(LV17TurretGun,3200)
                if main.Cutscences.Level.TPunlocked:
                    if e.key == pygame.K_p:
                        if not main.TSUSED and not main.TPUSED:
                            main.SlowDown = 0
                            main.TPParticles_on = True
                            main.Time_Stop = True
                            main.TPUSED = True
                if main.Cutscences.TL_unlocked:
                    if e.key == pygame.K_l:
                        if not main.TLUsed and not main.Time_Stop:
                            main.TLInfo['Player_pos'] = main.Player.rect.center
                            main.TLInfo['Stage'] = main.Cutscences.Stage
                            main.TLInfo['Tiles'] = main.Collideing_Tiles
                            main.TLInfo['Died'] = main.Player.Died
                            main.TLInfo["Bullets"] = main.Bullets.sprites()
                            main.Time_loop = True
                            main.TLUsed = True

    main.Draw()
    Clock.tick(60)
    pygame.display.update()