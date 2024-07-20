import pygame
from Levels import Level
pygame.init()
Title_font = pygame.font.Font("Fonts/NeonSans.ttf",50)
Cyborg_font = pygame.font.Font("Fonts/E1234.ttf", 20)
Game_font = pygame.font.SysFont("Orbitron", 30, True, False)

class Cutscence:
    def __init__(self):
        self.Level = Level()
        self.Lv1_Cutscene1 = False
        self.Lv2_Wrong_Choice_Death = False
        self.TS_Scene = False
        self.TS_Unlocked = False
        self.TL_Scene = False
        self.TP_Scene = False
        self.Lv2_Second_time = False
        self.OptionButton = pygame.Rect(423,33,100,40)
        self.Screen = pygame.display.get_surface()
        self.Stage = "Start"
        self.pressed = False
        self.Text1_DIsplay = False
        self.Text2_Display = False
        self.Door = pygame.image.load("Maps\Orginal_Set\Objects\DoorLocked.png").convert_alpha()
        self.Door = pygame.transform.scale_by(self.Door,1/2)
        self.Door_rect = self.Door.get_rect(center = (self.Screen.get_width()/2,self.Screen.get_height()/2))
        self.Fade_in = False
        self.Future_Hall = pygame.image.load("Chrono_imgs/Futuristic_Hallway.png").convert_alpha()
        self.Future_Hall = pygame.transform.scale_by(self.Future_Hall,5)
        self.Future_Hall_rect = self.Future_Hall.get_rect(topleft = (0,0))
        self.Portal = pygame.image.load("Chrono_imgs/Wormhole.png").convert_alpha()
        self.MF = pygame.image.load("Chrono_imgs/Mysterious_figure.png").convert_alpha()
        self.MF = pygame.transform.scale_by(self.MF,1.5)
        self.Portal_rect = self.Portal.get_rect(center = (self.Future_Hall_rect.centerx,self.Future_Hall_rect.centery - 10))
        self.MF_rect = self.MF.get_rect(center = (self.Portal_rect.centerx,self.Portal_rect.centery + 80))
        self.BlackScreen = pygame.Surface(self.Screen.get_size(),flags=pygame.SRCALPHA)
        self.BlackScreen_rect = self.BlackScreen.get_rect(topleft = (0,0))
        self.TextBox = pygame.Rect(0,500,800,300)
        self.alpha = 0
        self.direction = 1
        self.Text = ""
        self.Text2 = ""
        self.TL_unlocked = False
        self.Text3 = ""
        self.ForwardScene = False
        self.ForwardUnlocked = False
        self.Finish_Text = Title_font.render("Good JOb",True,"Black")
        self.Finish_Text_rect = self.Finish_Text.get_rect(center = (self.Screen.get_width()/2,self.Screen.get_height()/2))
        self.NextStage = ''
        self.TextBox_Text = Game_font.render(self.Text,True,"White")
        self.TextBox_Text2 = Game_font.render(self.Text2,True,"White")
        self.TextBox_Text3 = Game_font.render(self.Text3,True,"White")
        self.TextBox_Text_rect = self.TextBox_Text.get_rect(topleft = self.TextBox.topleft)
        self.TextBox_Text_rect2 = self.TextBox_Text2.get_rect(topleft = self.TextBox_Text_rect.bottomleft)
        self.TextBox_Text_rect3 = self.TextBox_Text3.get_rect(topleft = self.TextBox_Text_rect2.bottomleft)
        self.Title = pygame.image.load("Chrono_imgs/Title_Screen.png").convert_alpha()
        self.Title_rect = self.Title.get_rect(center = (self.Screen.get_width()/2,self.Screen.get_height()/2))
        self.Startbutton = pygame.Rect(self.Screen.get_width()/2 - 90,self.Screen.get_height()/2 + 100,200,100)
        self.StartText = Title_font.render("Start", True, "darkorchid4")
        self.StartText_rect = self.StartText.get_rect(center = self.Startbutton.center)
        self.Next_Text = Game_font.render("Press any key to countinue",True,"Purple")
        self.Next_Text_rect = self.Next_Text.get_rect(bottomleft = (520,630))

    def Stages(self,Slowdown):
        match self.Stage:
            case "Start":
                self.Screen.fill("#1E201F")
                self.Screen.blit(self.Title,self.Title_rect)
                pygame.draw.rect(self.Screen, "Silver", self.Startbutton)
                self.Screen.blit(self.StartText,self.StartText_rect)
                self.Startclick()
            
            case "Black":
                self.Text = ""
                self.Screen.blit(self.BlackScreen,self.BlackScreen_rect)
                self.Fade(self.NextStage,self.Fade_in)
            
            case "Level 1":
                self.alpha = 0
                self.Level.Draw_Level(self.Level.Level_1)
            
            case "LV1-Cave":
                self.Level.Draw_Level(self.Level.LV1_Cave)
    
            case "Level 2":
                self.Level.Draw_Level(self.Level.Level_2)

            case "LV2_WC":
                self.Level.Draw_Level(self.Level.LV2_WC)

            case "Level 3":
                self.Level.Draw_Level(self.Level.Level_3)
                if not self.ForwardUnlocked:pygame.display.get_surface().blit(self.Level.ForwardSymbol, self.Level.ForwardSymbol_rect)
            
            case "Level 4":
                self.Level.Draw_Level(self.Level.Level_4)
            
            case "Level 5":
                self.Level.Draw_Level(self.Level.Level_5)
            
            case "Level 6":
                self.Level.Draw_Level(self.Level.Level_6)
                if not self.TS_Unlocked: pygame.display.get_surface().blit(self.Level.TimeSlow,self.Level.TimeSlow_rect)
            
            case "Level 7":
                self.Level.Draw_Level(self.Level.Level_7)
            
            case "Level 8":
                self.Level.Draw_Level(self.Level.Level_8)
            
            case "Level 9":
                self.Level.Draw_Level(self.Level.Level_9)
            
            case "Level 10":
                self.Level.Draw_Level(self.Level.Level_10)
            
            case "Level 11":
                self.Level.Draw_Level(self.Level.Level_11)
            
            case "Level 12":
                self.Level.Draw_Level(self.Level.Level_12)
            
            case "Level 13":
                self.Level.Draw_Level(self.Level.Level_13,Slowdown)
            
            case "Level 14":
                self.Level.Draw_Level(self.Level.Level_14)
            
            case "Level 15":
                self.Level.Draw_Level(self.Level.Level_15)
                if not self.TL_unlocked: self.Screen.blit(self.Level.TimeLoop,self.Level.TimeLoop_rect)
            
            case "Level 15W":
                self.Level.Draw_Level(self.Level.Level_15W)
            
            case "Level 15R":
                self.Level.Draw_Level(self.Level.Level_15R)
            
            case "Level 16":
                self.Level.Draw_Level(self.Level.Level_16,Slowdown)
            
            case "Level 17":
                self.Level.Draw_Level(self.Level.Level_17)
            
            case "Level 18":
                self.Level.Draw_Level(self.Level.Level_18)

            case "Level 19":
                self.Level.Draw_Level(self.Level.Level_19)
            
            case "Level 20":
                self.Level.Draw_Level(self.Level.Level_20)
            
            case "Finish":
                self.Screen.fill("Yellow")
                self.Screen.blit(self.Finish_Text,self.Finish_Text_rect)

    def Startclick(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.Startbutton.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.Stage = "Black"
                    self.Fade_in = False
                    self.NextStage = "Level 1"
                    self.pressed = False

    def Cutscene_Text(self, Index, Text, TextBox):
        if Index < len(Text):
            TextBox += Text[Index]
        return TextBox

    def Fade(self,Next, Fade_in):
        self.BlackScreen.fill((0,0,0,self.alpha))
        if self.alpha < 255: self.alpha += 1
        else:
            if Fade_in:
                if self.alpha > 0: self.alpha -= 1
                else: self.Stage = Next
            else: self.Stage = Next; self.alpha = 0

    def Cyborg_Text(self, Text:str, TextColor:str, Next:bool = False,Text2 = ""):
        pygame.draw.rect(pygame.display.get_surface(),"Black",self.TextBox)
        self.Text = Text
        self.Text2 = Text2
        self.TextBox_Text = Game_font.render(self.Text,True,TextColor)
        self.TextBox_Text2 = Game_font.render(self.Text2,True,TextColor)
        pygame.display.get_surface().blit(self.TextBox_Text,self.TextBox_Text_rect)
        pygame.display.get_surface().blit(self.TextBox_Text2,self.TextBox_Text_rect2)
        if Next: pygame.display.get_surface().blit(self.Next_Text,self.Next_Text_rect)

    def Interactions(self, Text):
        Button_Text = Game_font.render(str(Text),True,"Black")
        Button_Text_rect = Button_Text.get_rect(center = self.OptionButton.center)
        pygame.draw.rect(self.Screen,("Silver"),self.OptionButton)
        self.Screen.blit(Button_Text,Button_Text_rect)