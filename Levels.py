import pygame, random
from pytmx.util_pygame import load_pygame #importing thing for tiled
from pygame.math import Vector2
pygame.init()
Game_font = pygame.font.Font("Fonts/E1234.ttf", 20)
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos:tuple,surf,groups,Tiles:bool,Name:str = "Tile"):
        super().__init__(groups)
        self.Name = Name
        if Tiles == "Saw":surf = pygame.transform.scale_by(surf,1/11)
        elif Tiles == True:surf = pygame.transform.scale_by(surf,1/8)
        else: surf = pygame.transform.scale_by(surf,1/4)
        self.image = surf
        self.rect = self.image.get_rect(topleft = (pos))

class RoboBullets(pygame.sprite.Sprite):
    def __init__(self, pos_x:int,pos_y:int,Direction:pygame.math.Vector2,Surface:tuple = (10,3),Color = (255,0,0)):
        super().__init__()
        self.Direction = Direction
        self.image = pygame.Surface(Surface)
        self.image.fill(Color)
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

    def update(self,slowdown):
        self.rect.x += self.Direction.x*slowdown 
        self.rect.y += self.Direction.y*slowdown

class Enemies(pygame.sprite.Sprite):
    def __init__(self,pos:tuple,surf,groups,Scale:int = 5,Direction:Vector2 = (-1,0),Name:str = "Tile",Surface:tuple = (10,3),Color = (255,0,0)):
        super().__init__(groups)
        self.Name = Name
        self.Direction = Direction
        self.Surface = Surface
        surf = pygame.transform.scale_by(surf,1/Scale)
        self.Color = Color
        self.image = surf
        self.rect = self.image.get_rect(topleft = (pos))
    
    def Bullet(self):
        return RoboBullets(self.rect.x,self.rect.y,self.Direction,self.Surface,self.Color)

class KeyCodeButtons:
    def __init__(self, pos, Number):
        self.Button = pygame.Rect((pos),(50,50))
        self.Number = Number
        self.Touched = False
        self.pressed = False
        self.Interface = Game_font.render(str(Number),True,"Black")
        self.Interface_rect = self.Interface.get_rect(center = self.Button.center)
    
    def Draw(self):
        pygame.draw.rect(pygame.display.get_surface(),"azure4",self.Button)#"azure4"
        pygame.display.get_surface().blit(self.Interface,self.Interface_rect)
        self.Press()
    
    def Press(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.Button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.Touched = True
                    self.pressed = False

class InputBoxes:
    def __init__(self, Input, pos):
        self.Rect = pygame.Rect((pos),(50,50))
        self.Input = Input
        self.Input_display = Game_font.render(str(self.Input),True,"Black")
        self.Input_display_rect = self.Input_display.get_rect(center = self.Rect.center)
    
    def Draw(self):
        self.Input_display = Game_font.render(str(self.Input),True,"Black")
        self.Input_display_rect = self.Input_display.get_rect(center = self.Rect.center)
        pygame.draw.rect(pygame.display.get_surface(),"Green",self.Rect)
        pygame.display.get_surface().blit(self.Input_display,self.Input_display_rect)

class LV13BoxShooters(pygame.sprite.Sprite):
    def __init__(self, pos:tuple,groups,Direction:int|float = 3):
        super().__init__(groups)
        self.pos = pos
        self.group = groups
        self.Direction = Direction
        self.image = pygame.image.load('Maps\Orginal_Set\Objects\Box.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image,1/3)
        self.rect = self.image.get_rect(topleft = pos)
    
    def NewBlock(self):
        return LV13BoxShooters(self.pos,self.group)

    def update(self,slowdown:int|float):
        self.rect.y += self.Direction * slowdown
        if self.rect.y > pygame.display.get_surface().get_height():
            self.kill()


N1 = KeyCodeButtons((258,352), 1)
N2 = KeyCodeButtons((358,352), 2)
N3 = KeyCodeButtons((458,352), 3)

N4 = KeyCodeButtons((258,432), 4)
N5 = KeyCodeButtons((358,432), 5)
N6 = KeyCodeButtons((458,432), 6)

N7 = KeyCodeButtons((258,532), 7)
N8 = KeyCodeButtons((358,532), 8)
N9 = KeyCodeButtons((458,532), 9)
N0 = KeyCodeButtons((358,600), 0)

I1 = InputBoxes("-",(270,264))
I2 = InputBoxes("-",(330,264))
I3 = InputBoxes("-",(390,264))
I4 = InputBoxes("-",(450,264))
class Level:
    def __init__(self):
        self.Lv1PasswordPaper = pygame.Surface((62,5))
        self.Lv1PasswordPaper.fill("White")
        self.Lv1PasswordPaper_rect = self.Lv1PasswordPaper.get_rect(topleft = (671,541))
        self.Numbers = '0123456789'
        self.Index = 0
        self.pressed = False
        self.LV1Success = False
        self.Exit = False
        self.Frame = pygame.Rect(100,100,100,100)
        self.Lv1Password = "".join(random.sample(self.Numbers, 4))
        self.RewindSymbol = pygame.image.load("Chrono_imgs/Rewind_Symbol.png").convert_alpha()
        self.RewindSymbol = pygame.transform.scale_by(self.RewindSymbol,1/3)
        self.RewindSymbol_rect = self.RewindSymbol.get_rect(center = self.Frame.center)
        self.ForwardSymbol = pygame.transform.flip(self.RewindSymbol,True,False)
        self.ForwardSymbol_rect = self.ForwardSymbol.get_rect(center = (141,489))
        self.Lv1Password_Text = Game_font.render(f"{self.Lv1Password}",True,"Black")
        self.Lv1Password_Text_rect = self.Lv1Password_Text.get_rect(center = (pygame.display.get_surface().get_width()/2,pygame.display.get_surface().get_height()/2))
        self.Back = pygame.Rect(359,150,100,50)
        self.TPunlocked = False
        self.TimeSlow = pygame.image.load("Chrono_Imgs/Time_Slow.png").convert_alpha()
        self.TimeSlow = pygame.transform.scale_by(self.TimeSlow,1/3)
        self.TimeSlow_rect = self.TimeSlow.get_rect(center = (163,102))
        self.TimeStop = pygame.image.load("Chrono_imgs\Time Stop.png").convert_alpha()
        self.TimeStop = pygame.transform.scale_by(self.TimeStop,1/3)
        self.TimeStop_rect = self.TimeStop.get_rect(center = (124,506))
        self.TimeLoop = pygame.image.load('Chrono_imgs/Time Loop.png').convert_alpha()
        self.TimeLoop = pygame.transform.scale_by(self.TimeLoop,1/3)
        self.TimeLoop_rect = self.TimeLoop.get_rect(center = (134,126))
        self.Back_Text = Game_font.render("Back",True, "Black")
        self.Back_Text_rect = self.Back_Text.get_rect(center = self.Back.center)
        self.BackSpace = pygame.Rect(458,600,100,50)
        self.Check = pygame.Rect(258,600,100,50)
        self.BackSpace_Text = Game_font.render("Delete", True, "Black")
        self.BackSpace_Text_rect = self.BackSpace_Text.get_rect(center = self.BackSpace.center)
        self.Check_Text = Game_font.render("Check",True,"Black")
        self.Check_Text_rect = self.Check_Text.get_rect(center = self.Check.center)
        self.Level1_puzzleSolved =False
        self.Paper = False
        self.PaperCutscene = False
        self.CaveEntered = False
        self.Level_1_Completed = False
        self.Level_1_map = load_pygame('Maps/Level_1.tmx')
        self.LV1_Cave_map = load_pygame('Maps/Level1_Cave.tmx')
        self.Lv2_map = load_pygame('Maps/Level_2.tmx')
        self.LV2_WC_map = load_pygame('Maps/Level_2_Wrong_Choice.tmx')
        self.LV3_map = load_pygame('Maps/Level_3.tmx')
        self.LV4_map = load_pygame("Maps/Level_4.tmx")
        self.LV5_map = load_pygame('Maps/Level_5.tmx')
        self.LV6_map = load_pygame('Maps/Level_6.tmx')
        self.LV7_map = load_pygame('Maps/Level_7.tmx')
        self.LV8_map = load_pygame('Maps/Level_8.tmx')
        self.LV9_map = load_pygame('Maps/Level_9.tmx')
        self.LV10_map = load_pygame('Maps/Level_10.tmx')
        self.LV11_map = load_pygame('Maps/Level_11.tmx')
        self.LV12_map = load_pygame('Maps/Level_12.tmx')
        self.LV13_map = load_pygame('Maps/Level_13.tmx')
        self.LV14_map = load_pygame('Maps/Level_14.tmx')
        self.LV15_map = load_pygame('Maps/Level_15.tmx')
        self.LV15W_map = load_pygame('Maps/Level_15W.tmx')
        self.LV15R_map = load_pygame('Maps/Level_15R.tmx')
        self.LV16_map = load_pygame('Maps/Level_16.tmx')
        self.LV17_map = load_pygame('Maps/Level_17.tmx')
        self.LV18_map = load_pygame('Maps/Level_18.tmx')
        self.LV19_map = load_pygame('Maps/Level_19.tmx')
        self.LV20_map = load_pygame('Maps/Level_20.tmx')
        self.Level_1 = pygame.sprite.Group()
        self.Lv1Locks = pygame.sprite.Group()
        self.Lv1Doors = pygame.sprite.Group()
        self.Lv1ClosedDoors = pygame.sprite.Group()
        self.Lv1OpenDoors = pygame.sprite.Group()
        self.LV1CaveOpenDoors = pygame.sprite.Group()
        self.LV1_Cave = pygame.sprite.Group()
        self.Level_2 = pygame.sprite.Group()
        self.Lv2Locks = pygame.sprite.Group()
        self.Lv2Doors = pygame.sprite.Group()
        self.Lv2ClosedDoors = pygame.sprite.Group()
        self.Lv2OpenDoors = pygame.sprite.Group()
        self.LV2_DeadlyBlocks = pygame.sprite.Group()
        self.LV2_WC = pygame.sprite.Group()
        self.LV2_WC_Doors = pygame.sprite.Group()
        self.Level_3 = pygame.sprite.Group()
        self.Lv3Doors = pygame.sprite.Group()
        self.Lv3Locks = pygame.sprite.Group()
        self.Lv3ClosedDoors = pygame.sprite.Group()
        self.Lv3OpenDoors = pygame.sprite.Group()
        self.LV3_DeadlyBlocks = pygame.sprite.Group()
        self.Level_4 = pygame.sprite.Group()
        self.Lv4Locks = pygame.sprite.Group()
        self.LV4MovingBlocks = pygame.sprite.Group()
        self.Lv4Doors = pygame.sprite.Group()
        self.Lv4ClosedDoors = pygame.sprite.Group()
        self.LV4DeadlyBlocks =  pygame.sprite.Group()
        self.Lv4OpenDoors = pygame.sprite.Group()
        self.Level_5 = pygame.sprite.Group()
        self.Lv5Doors = pygame.sprite.Group()
        self.Lv5Locks = pygame.sprite.Group()
        self.LV5WrongBlocks = pygame.sprite.Group()
        self.Lv5ClosedDoors = pygame.sprite.Group()
        self.Lv5OpenDoors = pygame.sprite.Group()
        self.LV5MovingBlocks = pygame.sprite.Group()
        self.LV5DeadlyBlocks = pygame.sprite.Group()
        self.Level_6 = pygame.sprite.Group()
        self.Lv6Locks = pygame.sprite.Group()
        self.LV6MovingBlocks1 = pygame.sprite.Group()
        self.LV6MovingBlocks2 = pygame.sprite.Group()
        self.LV6MovingBlocksSquare = pygame.sprite.Group()
        self.Lv6Doors = pygame.sprite.Group()
        self.Lv6ClosedDoors = pygame.sprite.Group()
        self.Lv6OpenDoors = pygame.sprite.Group()
        self.LV6DeadlyBlocks = pygame.sprite.Group()
        self.Level_7 = pygame.sprite.Group()
        self.LV7Locks = pygame.sprite.Group()
        self.Lv7Doors = pygame.sprite.Group()
        self.Lv7ClosedDoors = pygame.sprite.Group()
        self.Lv7OpenDoors = pygame.sprite.Group()
        self.LV7MovingBlocks = pygame.sprite.Group()
        self.LV7DeadlyBlocks = pygame.sprite.Group()
        self.Lv7Shooters = pygame.sprite.Group()
        self.Lv7Shooters_Bottom = pygame.sprite.Group()
        self.Level_8 = pygame.sprite.Group()
        self.LV8Locks = pygame.sprite.Group()
        self.LV8MovingBlocks = pygame.sprite.Group()
        self.Lv8Doors = pygame.sprite.Group()
        self.Lv8ClosedDoors = pygame.sprite.Group()
        self.Lv8OpenDoors = pygame.sprite.Group()
        self.Level_9 = pygame.sprite.Group()
        self.LV9Locks = pygame.sprite.Group()
        self.Lv9Doors = pygame.sprite.Group()
        self.Lv9ClosedDoors = pygame.sprite.Group()
        self.Lv9OpenDoors = pygame.sprite.Group()
        self.LV9MovingBlocks1 = pygame.sprite.Group()
        self.LV9MovingBlocks2 = pygame.sprite.Group()
        self.Lv9FakeBlocks = pygame.sprite.Group()
        self.LV9DeadlyBlocks = pygame.sprite.Group()
        self.Lv9Shooters = pygame.sprite.Group()
        self.Lv9Shooters_Bottom = pygame.sprite.Group()
        self.Level_10 = pygame.sprite.Group()
        self.Lv10Doors = pygame.sprite.Group()
        self.LV10Locks = pygame.sprite.Group()
        self.Lv10ClosedDoors = pygame.sprite.Group()
        self.Lv10OpenDoors = pygame.sprite.Group()
        self.LV10DeadlyBlocks = pygame.sprite.Group()
        self.LV10SawDisplay = False
        self.LV10MovingBlocks = pygame.sprite.Group()
        self.LV10Saws1 = pygame.sprite.Group()
        self.LV10Saws2 = pygame.sprite.Group()
        self.Level_11 = pygame.sprite.Group()
        self.LV11DeadlyBlocks = pygame.sprite.Group()
        self.LV11Locks = pygame.sprite.Group()
        self.Lv11Doors = pygame.sprite.Group()
        self.Lv11ClosedDoors = pygame.sprite.Group()
        self.Lv11OpenDoors = pygame.sprite.Group()
        self.LV11Saws = pygame.sprite.Group()
        self.LV11Saw = pygame.sprite.GroupSingle()
        self.Level_12 = pygame.sprite.Group()
        self.Lv12Locks = pygame.sprite.Group()
        self.LV12WhiteMovingBlocks = pygame.sprite.Group()
        self.LV12BlackMovingBlocks = pygame.sprite.Group()
        self.LV12BlackActiver = pygame.sprite.GroupSingle()
        self.LV12WhiteActiver = pygame.sprite.GroupSingle()
        self.LV12MovingBlocks1,self.LV12MovingBlocks2 = pygame.sprite.Group(),pygame.sprite.Group()
        self.Lv12Doors = pygame.sprite.Group()
        self.Lv12ClosedDoors = pygame.sprite.Group()
        self.LV12Black_on = True
        self.LV12DeadlyBlocks =  pygame.sprite.Group()
        self.Lv12OpenDoors = pygame.sprite.Group()
        self.Level_13 = pygame.sprite.Group()
        self.Lv13Doors = pygame.sprite.Group()
        self.LV13Locks = pygame.sprite.Group()
        self.Lv13ClosedDoors = pygame.sprite.Group()
        self.Lv13OpenDoors = pygame.sprite.Group()
        self.LV13DeadlyBlocks = pygame.sprite.Group()
        self.LV13Boxes = pygame.sprite.Group()
        self.LV13Box1 = LV13BoxShooters((103,-110),(self.LV13Boxes,self.Level_13))
        self.LV13Box2 = LV13BoxShooters((190,-110),(self.LV13Boxes,self.Level_13))
        self.LV13Box3 = LV13BoxShooters((277,-110),(self.LV13Boxes,self.Level_13))
        self.LV13Box4 = LV13BoxShooters((364,-110),(self.LV13Boxes,self.Level_13))
        self.LV13Box5 = LV13BoxShooters((451,-110),(self.LV13Boxes,self.Level_13))
        self.LV13Box6 = LV13BoxShooters((538,-110),(self.LV13Boxes,self.Level_13))
        self.Level_14 = pygame.sprite.Group()
        self.LV14Locks = pygame.sprite.Group()
        self.Lv14Doors = pygame.sprite.Group()
        self.Lv14ClosedDoors = pygame.sprite.Group()
        self.Lv14OpenDoors = pygame.sprite.Group()
        self.LV14MovingBlocks = pygame.sprite.Group()
        self.LV14DeadlyBlocks = pygame.sprite.Group()
        self.Lv14Shooters = pygame.sprite.Group()
        self.LV14FastShooters = pygame.sprite.Group()
        self.Level_15 = pygame.sprite.Group()
        self.Lv15Locks = pygame.sprite.Group()
        self.Lv15Doors = pygame.sprite.Group()
        self.Lv15DoorNames = ['1','2','3','4']
        self.Lv15ClosedDoors = pygame.sprite.Group()
        self.Lv15OpenDoors = pygame.sprite.Group()
        self.Level_15W = pygame.sprite.Group()
        self.Lv15WClosedDoors = pygame.sprite.Group()
        self.LV15WDeadlyBlocks = pygame.sprite.Group()
        self.Lv15ROpenDoors = pygame.sprite.Group()
        self.Level_15R = pygame.sprite.Group()
        self.LV15RDeadlyBlocks = pygame.sprite.Group()
        self.Level_16 = pygame.sprite.Group()
        self.Lv16Doors = pygame.sprite.Group()
        self.Lv16Locks = pygame.sprite.Group()
        self.LV16WrongBlocks = pygame.sprite.Group()
        self.Lv16ClosedDoors = pygame.sprite.Group()
        self.Lv16OpenDoors = pygame.sprite.Group()
        self.LV16MovingBlocks = pygame.sprite.Group()
        self.LV16DeadlyBlocks = pygame.sprite.Group()
        self.LV16Boxes = pygame.sprite.Group()
        self.LV16Box = LV13BoxShooters((630,-200),(self.LV16DeadlyBlocks,self.LV16Boxes))
        self.Level_17 = pygame.sprite.Group()
        self.Lv17Doors = pygame.sprite.Group()
        self.LV17Locks = pygame.sprite.Group()
        self.Lv17ClosedDoors = pygame.sprite.Group()
        self.Lv17OpenDoors = pygame.sprite.Group()
        self.LV17DeadlyBlocks = pygame.sprite.Group()
        self.Lv17Shooters = pygame.sprite.Group()
        self.Level_18 = pygame.sprite.Group()
        self.LV18DeadlyBlocks = pygame.sprite.Group()
        self.LV18Locks = pygame.sprite.Group()
        self.Lv18Doors = pygame.sprite.Group()
        self.Lv18ClosedDoors = pygame.sprite.Group()
        self.Lv18OpenDoors = pygame.sprite.Group()
        self.LV18Saws = pygame.sprite.Group()
        self.LV18Saws2 = pygame.sprite.Group()
        self.Level_19 = pygame.sprite.Group()
        self.LV19Locks = pygame.sprite.Group()
        self.Lv19Doors = pygame.sprite.Group()
        self.Lv19ClosedDoors = pygame.sprite.Group()
        self.Lv19OpenDoors = pygame.sprite.Group()
        self.LV19MovingBlocks = pygame.sprite.Group()
        self.Lv19FakeBlocks = pygame.sprite.Group()
        self.LV19DeadlyBlocks = pygame.sprite.Group()
        self.Lv19Shooters = pygame.sprite.Group()
        self.Level_20 = pygame.sprite.Group()
        self.Lv20Doors = pygame.sprite.Group()
        self.LV20Locks = pygame.sprite.Group()
        self.Lv20ClosedDoors = pygame.sprite.Group()
        self.Lv20OpenDoors = pygame.sprite.Group()
        self.LV20DeadlyBlocks = pygame.sprite.Group()
        self.Lv20FakeBlocks = pygame.sprite.Group()
        self.BackGround = pygame.sprite.Group()
        self.Bullets = pygame.sprite.Group()
        self.LV9FastShooter = pygame.sprite.Group()
        self.DoorText = Game_font.render("1:00", True, "Black")
        self.DoorTextBox = pygame.Rect(400,200,100,100)
        self.DoorText_rect = self.DoorText.get_rect(center = self.DoorTextBox.center)
        self.Player_pos = (0,0)
        self.Load_Level_1()
        self.Load_LV1_Cave()
        self.Load_LV2()
        self.Load_LV2_WC()
        self.Load_LV3()
        self.Load_LV4()
        self.Load_LV5()
        self.Load_LV6()
        self.Load_LV7()
        self.Load_LV8()
        self.Load_LV9()
        self.Load_LV10()
        self.Load_LV11()
        self.Load_LV12()
        self.Load_LV13()
        self.Load_LV14()
        self.Load_LV15()
        self.Load_LV15W()
        self.Load_LV15R()
        self.Load_LV16()
        self.Load_LV17()
        self.Load_LV18()
        self.Load_LV19()
        self.Load_LV20()
    
    def Load_Level_1(self):
        for layer in self.Level_1_map.layers:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name == "BackGround": Tile((x*32,y*32),surf,self.BackGround,True)
                    else: Tile((x*32,y*32),surf,self.Level_1,True)

        for obj in self.Level_1_map.objects:
            if obj.image:
                if obj.name == "Start_Door":Tile((52,430),obj.image,(self.Lv1Doors,self.Lv1ClosedDoors),False,"Start_Door"); self.Player_pos = (72,430)
                elif obj.name == "Cave_Door":Tile((703,328),obj.image,(self.Lv1OpenDoors,self.Lv1Doors),False,"Cave_Door")
                elif obj.name == "Finish_Door":Tile((319,428),obj.image,(self.Lv1Doors,self.Lv1ClosedDoors),False,"Finish_Door")
                elif obj.name == "KeyCode":Tile((202,481),obj.image,self.Lv1Locks,False,"KeyCode")
                else:Tile((638,392),obj.image,self.Lv1Locks,False)
    
    def Load_LV1_Cave(self):
        for layer in self.LV1_Cave_map.layers:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name == "BackGround": pass
                    else: Tile((x*32,y*32),surf,self.LV1_Cave,True)
        
        for obj in self.LV1_Cave_map.objects:
            self.Player_pos = (35,348)
            if obj.image:
                if obj.name == "Cave_Door":Tile((35,297),obj.image,self.LV1CaveOpenDoors,False,"Cave_Door")
    
    def Load_LV2(self):
        for layer in self.Lv2_map.layers:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name == "BackGround": pass
                    else: Tile((x*32,y*32),surf,self.Level_2,True)
        
        for obj in self.Lv2_map.objects:
            if obj.name == "Start_Door":Tile((18,430),obj.image,(self.Lv2Doors,self.Lv2ClosedDoors),False,"Start_Door")
            elif obj.name == "Choice1":Tile((260,430),obj.image,(self.Lv2Doors,self.Lv2OpenDoors),False,"Choice1")
            elif obj.name == "Choice2":Tile((456,430),obj.image,(self.Lv2Doors,self.Lv2OpenDoors),False,"Choice2")
            else:
                Tile((382,481),obj.image,self.Lv2Locks,False,"Doorint")

    def Load_LV2_WC(self):
        for layer in self.LV2_WC_map.layers:
            if hasattr(layer, "data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround":
                        if  self.LV2_WC_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Acid (1).png':
                            Tile((x*32,y*32),surf,self.LV2_DeadlyBlocks,True)
                        else:
                            Tile((x*32,y*32),surf,self.LV2_WC,True)
        
        for obj in self.LV2_WC_map.objects:
            if obj.name == "Start_Door":Tile((25,210),obj.image,(self.LV2_WC_Doors),False,"Start_Door")
        
    def Load_LV3(self):
        for layer in self.LV3_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV3_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Acid (1).png':
                            Tile((x*32,y*32),surf,(self.LV3_DeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_3,True)
        #
        for obj in self.LV3_map.objects:
            if obj.name == "Start_Door":Tile((5,430),obj.image,(self.Lv3Doors,self.Lv3ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((644,380),obj.image,(self.Lv3Locks),False,"Timer")
            else:
                Tile((716,330),obj.image,(self.Lv3OpenDoors,self.Lv3Doors),False,"Finish_Door")

    def Load_LV4(self):
        for layer in self.LV4_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV4_map.get_tile_properties(x,y,1)['source'] == 'Orginal_Set/Tiles/Tile (12).png':
                            Tile((x*32,y*32),surf,(self.Level_4,self.LV4MovingBlocks),True)
                        elif self.LV4_map.get_tile_properties(x,y,1)['source'] == 'Orginal_Set/Tiles/Acid (1).png':
                            Tile((x*32,y*32),surf,(self.LV4DeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_4,True)
        
        for obj in self.LV4_map.objects:
            if obj.name == "Start_Door":Tile((23,430),obj.image,(self.Lv4Doors,self.Lv4ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((676,221),obj.image,(self.Lv4Locks),False,"Timer")
            else:
                Tile((730,170),obj.image,(self.Lv4OpenDoors,self.Lv4Doors),False,"Finish_Door")

    def Load_LV5(self):
        for layer in self.LV5_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV5_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Spike.png'):
                            Tile((x*32,y*32),surf,(self.LV5DeadlyBlocks),True)
                        elif self.LV5_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Tile (13).png','Orginal_Set/Tiles/Tile (15).png'):
                            Tile((x*32,y*32),surf,self.LV5WrongBlocks,True)
                        elif self.LV5_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (12).png':
                            Tile((x*32,y*32),surf,(self.Level_5, self.LV5MovingBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_5,True)
        
        for obj in self.LV5_map.objects:
            if obj.name == "Start_Door":Tile((28,40),obj.image,(self.Lv5Doors,self.Lv5ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((2, 475),obj.image,(self.Lv5Locks),False,"Timer")
            else:
                Tile((99,425),obj.image,(self.Lv5OpenDoors,self.Lv5Doors),False,"Finish_Door")

    def Load_LV6(self):
        for layer in self.LV6_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV6_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Spike.png','Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Spike(R).png'):
                            Tile((x*32,y*32),surf,(self.LV6DeadlyBlocks),True)
                        elif self.LV6_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (12).png':
                            Tile((x*32,y*32),surf,(self.Level_6, self.LV6MovingBlocks1),True)
                        elif self.LV6_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (14).png':
                            Tile((x*32,y*32),surf,(self.Level_6, self.LV6MovingBlocks2),True)
                        elif self.LV6_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (13).png':
                            Tile((x*32,y*32),surf,(self.Level_6, self.LV6MovingBlocksSquare),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_6,True)
                
        for obj in self.LV6_map.objects:
            if obj.name == "Start_Door":Tile((6,50),obj.image,(self.Lv6Doors,self.Lv6ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((677, 220),obj.image,(self.Lv6Locks),False,"Timer")
            else:
                Tile((706,167),obj.image,(self.Lv6OpenDoors,self.Lv6Doors),False,"Finish_Door")

    def Load_LV7(self):
        for layer in self.LV7_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV7_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Spike.png','Orginal_Set/Tiles/Spike(L).png','Orginal_Set/Tiles/Spike(R).png'):
                            Tile((x*32,y*32),surf,(self.LV7DeadlyBlocks),True)
                        elif self.LV7_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (13).png':
                            Tile((x*32,y*32),surf,(self.Level_7, self.LV7MovingBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_7,True)
        
        for obj in self.LV7_map.objects:
            if obj.name == "Start_Door":Tile((28,42),obj.image,(self.Lv7Doors,self.Lv7ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((677,92),obj.image,(self.LV7Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((705,430),obj.image,(self.Lv7OpenDoors,self.Lv7Doors),False,"Finish_Door")
            elif obj.name == "Bottom-Gun-Head":Enemies((233,464),obj.image,(self.Lv7Shooters,self.LV7DeadlyBlocks),Name="Bottom-Gun-Head",Direction=Vector2(0,-4),Surface=(3,10))
            elif obj.name == "Bottom-Gun-Bottom":Enemies((219,509),obj.image,(self.Lv7Shooters_Bottom,self.LV7DeadlyBlocks),Name="Bottom-Gun-Bottom")
            elif obj.name == "Bottom-Gun2-Head":Enemies((488,464),obj.image,(self.Lv7Shooters),Name="Bottom-Gun2-Head",Direction=Vector2(0,-4),Surface=(3,10))
            elif obj.name == "Bottom-Gun2-Bottom":Enemies((474,509),obj.image,(self.Lv7Shooters_Bottom,self.LV7DeadlyBlocks),Name="Bottom-Gun2-Bottom")

    def Load_LV8(self):
        for layer in self.LV8_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround":
                        if self.LV8_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (12).png':
                            Tile((x*32,y*32),surf,(self.Level_8, self.LV8MovingBlocks),True,"K4")
                        elif self.LV8_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (13).png':
                            Tile((x*32,y*32),surf,(self.Level_8, self.LV8MovingBlocks),True,"K1")
                        elif self.LV8_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (14).png':
                            Tile((x*32,y*32),surf,(self.Level_8, self.LV8MovingBlocks),True,"K3")
                        elif self.LV8_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (15).png':
                            Tile((x*32,y*32),surf,(self.Level_8, self.LV8MovingBlocks),True,"K2")
                        else:
                            Tile((x*32,y*32),surf,self.Level_8,True)
        
        for obj in self.LV8_map.objects:
            if obj.name == "Start_Door":Tile((3,430),obj.image,(self.Lv8Doors,self.Lv8ClosedDoors),False,"Start_Door")
            elif obj.name == "K1": Tile((450,481),obj.image,(self.LV8Locks),False,"K1")
            elif obj.name == "K2":Tile((520,481),obj.image,(self.LV8Locks),False,"K2")
            elif obj.name == "K3":Tile((590,481),obj.image,(self.LV8Locks),False,"K3")
            elif obj.name == "K4":Tile((673,481),obj.image,(self.LV8Locks),False,"K4")
            else:
                Tile((727,430),obj.image,(self.Lv8ClosedDoors,self.Lv8Doors),False,"Finish_Door")

    def Load_LV9(self):
        for layer in self.LV9_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV9_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Acid (2).png','Orginal_Set/Tiles/Spike.png'):
                            Tile((x*32,y*32),surf,(self.LV9DeadlyBlocks),True)
                        elif self.LV9_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (13).png':
                            Tile((x*32,y*32),surf,(self.Level_9, self.LV9MovingBlocks2),True)
                        elif self.LV9_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (3).png':
                            Tile((x*32,y*32),surf,(self.Level_9, self.LV9MovingBlocks1),True)
                        elif self.LV9_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (6).png':
                            Tile((x*32,y*32),surf,(self.Lv9FakeBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_9,True)
        
        for obj in self.LV9_map.objects:
            if obj.name == "Start_Door":Tile((3,41),obj.image,(self.Lv9Doors,self.Lv9ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((160,481),obj.image,(self.LV9Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((2,425),obj.image,(self.Lv9OpenDoors,self.Lv9Doors),False,"Finish_Door")
            elif obj.name == "Top-Gun-Bottom":Enemies((703,121),obj.image,(self.Lv9Shooters_Bottom,self.LV9DeadlyBlocks),Name="Top-Gun-Bottom")
            elif obj.name == "Top-Gun-Head":Enemies((685,115),obj.image,(self.LV9FastShooter,self.LV9DeadlyBlocks),Name="Top-Gun-Head",Direction=Vector2(-6,0),Surface=(6,3))
            elif obj.name == "Bottom-Gun2-Head":Enemies((694,240),obj.image,(self.Lv9Shooters,self.LV9DeadlyBlocks),Name="Bottom-Gun2-Head",Direction=Vector2(-4,0),Surface=(6,3))
            elif obj.name == "Bottom-Gun2-Bottom":Enemies((710,249),obj.image,(self.Lv9Shooters_Bottom,self.LV9DeadlyBlocks),Name="Bottom-Gun2-Bottom")

    def Load_LV10(self):
        for layer in self.LV10_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV10_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Acid (2).png','Orginal_Set/Tiles/Spike.png'):
                            Tile((x*32,y*32),surf,(self.LV10DeadlyBlocks),True)
                        elif self.LV10_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (15).png':
                            Tile((x*32,y*32),surf,(self.LV10MovingBlocks,self.Level_10),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_10,True)
        
        for obj in self.LV10_map.objects:
            if obj.name == "Start_Door":Tile((4,427),obj.image,(self.Lv10Doors,self.Lv10ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((678,100),obj.image,(self.LV10Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((721,50),obj.image,(self.Lv10OpenDoors,self.Lv10Doors),False,"Finish_Door")
            elif obj.name == "1a":Tile((181,526),obj.image,(self.LV10Saws1),"Saw","1a")
            elif obj.name == "1b":Tile((230,526),obj.image,(self.LV10Saws2),"Saw","1b")
            elif obj.name == "1c":Tile((316,526),obj.image,(self.LV10Saws1),"Saw","1c")
            elif obj.name == "2a":Tile((370,526),obj.image,(self.LV10Saws2),"Saw","2a")
            elif obj.name == "2b":Tile((447, 526),obj.image,(self.LV10Saws1),"Saw","2b")
            elif obj.name == "2c":Tile((503, 526),obj.image,(self.LV10Saws2),"Saw","2c")

    def Load_LV11(self):
        for layer in self.LV11_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV11_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Spike.png','Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Spike(R).png'):
                            Tile((x*32,y*32),surf,(self.LV11DeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_11,True)
        
        for obj in self.LV11_map.objects:
            if obj.name == "Start_Door":Tile((6,45),obj.image,(self.Lv11Doors,self.Lv11ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((677, 223),obj.image,(self.LV11Locks),False,"Timer")
            elif obj.name == "Finish_Door":Tile((706,173),obj.image,(self.Lv11OpenDoors,self.Lv11Doors),False,"Finish_Door")
            elif obj.name == "a":Tile((178,178),obj.image,(self.LV11Saws),"Saw","a")
            elif obj.name == "b":Tile((320,211),obj.image,(self.LV11Saws),"Saw","b")
            elif obj.name == "c":Tile((416,243),obj.image,(self.LV11Saws),"Saw","c")
            elif obj.name == "d":Tile((498,176),obj.image,(self.LV11Saws),"Saw","d")
            elif obj.name == "e":Tile((576,118),obj.image,(self.LV11Saws),"Saw","e")

    def Load_LV12(self):
        for layer in self.LV12_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround":
                        if self.LV12_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (10).png':
                            Tile((x*32,y*32),surf,(self.Level_12, self.LV12BlackActiver),True,)
                        elif self.LV12_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (13).png':
                            Tile((x*32,y*32),surf,(self.Level_12, self.LV12WhiteActiver),True,)
                        elif self.LV12_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (11).png':
                            Tile((x*32,y*32),surf,(self.Level_12, self.LV12BlackMovingBlocks),True)
                        elif self.LV12_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (14).png':
                            Tile((x*32,y*32),surf,(self.Level_12, self.LV12MovingBlocks2),True,)
                        elif self.LV12_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (12).png':
                            Tile((x*32,y*32),surf,(self.Level_12, self.LV12MovingBlocks1),True)
                        elif self.LV12_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (15).png':
                            Tile((x*32,y*32),surf,(self.Level_12, self.LV12WhiteMovingBlocks),True)
                        elif self.LV12_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Spike.png','Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Spike(R).png'):
                            Tile((x*32,y*32),surf,(self.LV12DeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_12,True)
        
        for obj in self.LV12_map.objects:
            if obj.name == "Start_Door":Tile((7,78),obj.image,(self.Lv12Doors,self.Lv12ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((677, 223),obj.image,(self.Lv12Locks),False,"Timer")
            else:
                Tile((709,166),obj.image,(self.Lv12OpenDoors,self.Lv12Doors),False,"Finish_Door")

    def Load_LV13(self):
        for layer in self.LV13_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV13_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png'):
                            Tile((x*32,y*32),surf,(self.LV13DeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_13,True)
        
        for obj in self.LV13_map.objects:
            if obj.name == "Start_Door":Tile((6,43),obj.image,(self.Lv13Doors,self.Lv13ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((690,371),obj.image,(self.LV13Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((710,330),obj.image,(self.Lv13OpenDoors,self.Lv13Doors),False,"Finish_Door")

    def Load_LV14(self):
        for layer in self.LV14_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV14_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png'):
                            Tile((x*32,y*32),surf,(self.LV14DeadlyBlocks),True)
                        elif self.LV14_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Tile (1).png'):
                            Tile((x*32,y*32),surf,(self.LV14MovingBlocks,self.Level_14),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_14,True)
        
        for obj in self.LV14_map.objects:
            if obj.name == "Start_Door":Tile((3,490),obj.image,(self.Lv14Doors,self.Lv14ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((674,125),obj.image,(self.LV14Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((734,45),obj.image,(self.Lv14OpenDoors,self.Lv14Doors),False,"Finish_Door")
            elif obj.name == "Top-Gun": Enemies((261,32),obj.image,(self.Lv14Shooters,self.LV14DeadlyBlocks),Name="Top-Gun",Direction=Vector2(0,4),Surface=(6,3),Scale=7)
            elif obj.name == "Right-FastGun": Enemies((617,259),obj.image,(self.LV14FastShooters,self.LV14DeadlyBlocks),Name="Right-FastGun",Direction=Vector2(-6,0),Surface=(6,1),Scale=7)
            elif obj.name == "Bottom-Gun": Enemies((356,493),obj.image,(self.Lv14Shooters,self.LV14DeadlyBlocks),Name="Bottom-Gun",Direction=Vector2(0,-3),Surface=(1,6),Scale=7)
            elif obj.name == "Bottom-FastGun": Enemies((424,493),obj.image,(self.LV14FastShooters,self.LV14DeadlyBlocks),Name="Bottom-FastGun",Direction=Vector2(0,-6),Surface=(1,6),Scale=7)
            elif obj.name == "Left-FastGun": Enemies((0,330),obj.image,(self.LV14FastShooters,self.LV14DeadlyBlocks),Name="Left-FastGun",Direction=Vector2(6,0),Surface=(6,1),Scale=7)

    def Load_LV15(self):
        name = ''
        for layer in self.LV15_map.layers:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround":Tile((x*32,y*32),surf,self.Level_15,True)

        for obj in self.LV15_map.objects:
            if obj.image:
                if obj.name == "Start_Door":Tile((4,45),obj.image,(self.Lv15Doors,self.Lv15ClosedDoors),False,"Start_Door")
                elif obj.name == "Door4":
                    name = random.choice(self.Lv15DoorNames)
                    Tile((703,328),obj.image,(self.Lv15OpenDoors,self.Lv15Doors),False,f"Door{name}")
                    self.Lv15DoorNames.remove(name)
                elif obj.name == "Door4Timer":Tile((675,378),obj.image,self.Lv15Locks,False)
                elif obj.name == "Door1":
                    name = random.choice(self.Lv15DoorNames)
                    Tile((0,430),obj.image,(self.Lv15OpenDoors,self.Lv15Doors),False,f"Door{name}")
                    self.Lv15DoorNames.remove(name)
                elif obj.name == "Door1Timer":Tile((83,480),obj.image,self.Lv15Locks,False)
                elif obj.name == "Door2":
                    name = random.choice(self.Lv15DoorNames)
                    Tile((177,430),obj.image,(self.Lv15OpenDoors,self.Lv15Doors),False,f"Door{name}")
                    self.Lv15DoorNames.remove(name)
                elif obj.name == "Door2Timer":Tile((260,480),obj.image,self.Lv15Locks,False)
                elif obj.name == "Door3":
                    name = random.choice(self.Lv15DoorNames)
                    Tile((354,430),obj.image,(self.Lv15OpenDoors,self.Lv15Doors),False,f"Door{name}")
                    self.Lv15DoorNames.remove(name)
                elif obj.name == "Door3Timer":Tile((437,480),obj.image,self.Lv15Locks,False)
        
    def Load_LV15W(self):
        for layer in self.LV15W_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV15W_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Acid (1).png':
                            Tile((x*32,y*32),surf,(self.LV15WDeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_15W,True)
        #
        for obj in self.LV15W_map.objects:
            if obj.name == "Fake":Tile((729,52),obj.image,(self.Lv15WClosedDoors),False,"Fake")     

    def Load_LV15R(self):
        for layer in self.LV15R_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV15R_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Acid (1).png':
                            Tile((x*32,y*32),surf,(self.LV15RDeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_15R,True)
        #
        for obj in self.LV15R_map.objects:
            if obj.name == "Finish":Tile((729,52),obj.image,(self.Lv15ROpenDoors),False,"Finish_Door") 

    def Load_LV16(self):
        for layer in self.LV16_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV16_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png','Orginal_Set/Tiles/Spike.png'):
                            Tile((x*32,y*32),surf,(self.LV16DeadlyBlocks),True)
                        elif self.LV16_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Tile (2).png'):
                            Tile((x*32,y*32),surf,self.LV16WrongBlocks,True)
                        elif self.LV16_map.get_tile_properties(x,y,1)["source"] == 'Orginal_Set/Tiles/Tile (13).png':
                            Tile((x*32,y*32),surf,(self.Level_16, self.LV16MovingBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_16,True)
        
        for obj in self.LV16_map.objects:
            if obj.name == "Start_Door":Tile((28,40),obj.image,(self.Lv16Doors,self.Lv16ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((2, 475),obj.image,(self.Lv16Locks),False,"Timer")
            else:
                Tile((99,425),obj.image,(self.Lv16OpenDoors,self.Lv16Doors),False,"Finish_Door")

    def Load_LV17(self):
        for layer in self.LV17_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV17_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png'):
                            Tile((x*32,y*32),surf,(self.LV17DeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_17,True)
        
        for obj in self.LV17_map.objects:
            if obj.name == "Start_Door":Tile((6,43),obj.image,(self.Lv17Doors,self.Lv17ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((678,510),obj.image,(self.LV17Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((728,468),obj.image,(self.Lv17OpenDoors,self.Lv17Doors),False,"Finish_Door")
            elif obj.name == "Middle-Gun-Head":Enemies((665,276),obj.image,(self.Lv17Shooters),Surface=(30,3),Direction=Vector2(-3,0),Name=obj.name,Color=(0,255,0))
            elif obj.name == "Middle-Gun-Bottom":Enemies((680,275),obj.image,(self.LV17DeadlyBlocks),Name=obj.name)
            elif obj.name == "Bottom-Gun-Head":Enemies((40,495),obj.image,(self.Lv17Shooters),Surface=(30,3),Direction=Vector2(3,0),Name=obj.name,Color=(0,255,0))
            elif obj.name == "Bottom-Gun-Bottom":Enemies((26,514),obj.image,(self.LV17DeadlyBlocks),Name=obj.name)

    def Load_LV18(self):
        for layer in self.LV18_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV18_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png'):
                            Tile((x*32,y*32),surf,(self.LV18DeadlyBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_18,True)
        
        for obj in self.LV18_map.objects:
            if obj.name == "Start_Door":Tile((6,45),obj.image,(self.Lv18Doors,self.Lv18ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((677, 223),obj.image,(self.LV18Locks),False,"Timer")
            elif obj.name == "Finish_Door":Tile((706,173),obj.image,(self.Lv18OpenDoors,self.Lv18Doors),False,"Finish_Door")
            elif obj.name == "a":Tile((320,122),obj.image,(self.LV18Saws,self.LV18DeadlyBlocks),"Saw","a")
            elif obj.name == "b":Tile((320,272),obj.image,(self.LV18Saws,self.LV18DeadlyBlocks),"Saw","b")
            elif obj.name == "c":Tile((526,122),obj.image,(self.LV18Saws2,self.LV18DeadlyBlocks),"Saw","c")
            elif obj.name == "d":Tile((526,272),obj.image,(self.LV18Saws2,self.LV18DeadlyBlocks),"Saw","d")

    def Load_LV19(self):
        for layer in self.LV19_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV19_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png'):
                            Tile((x*32,y*32),surf,(self.LV19DeadlyBlocks),True)
                        elif self.LV19_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Tile (13).png'):
                            Tile((x*32,y*32),surf,(self.LV19MovingBlocks,self.Level_19),True)
                        elif self.LV19_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Tile (6).png'):
                            Tile((x*32,y*32),surf,(self.Lv19FakeBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_19,True)
        
        for obj in self.LV19_map.objects:
            if obj.name == "Start_Door":Tile((6,330),obj.image,(self.Lv19Doors,self.Lv19ClosedDoors),False,"Start_Door")
            elif obj.name == "Timer":Tile((690,380),obj.image,(self.LV19Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((710,330),obj.image,(self.Lv19OpenDoors,self.Lv19Doors),False,"Finish_Door")
            elif obj.name == "Right-Gun":Enemies((592,201),obj.image,(self.Lv19Shooters),5,Vector2(-12,6),"Right-Gun")

    def Load_LV20(self):
        for layer in self.LV20_map:
            if hasattr(layer,"data"):
                for x,y,surf in layer.tiles():
                    if layer.name != "BackGround": 
                        if self.LV20_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Acid (1).png'):
                            Tile((x*32,y*32),surf,(self.LV20DeadlyBlocks),True)
                        elif self.LV20_map.get_tile_properties(x,y,1)["source"] in ('Orginal_Set/Tiles/Tile (4).png'):
                            Tile((x*32,y*32),surf,(self.Lv20FakeBlocks),True)
                        else:
                            Tile((x*32,y*32),surf,self.Level_20,True)
        
        for obj in self.LV20_map.objects:
            if obj.name == "Timer":Tile((677,534),obj.image,(self.LV20Locks),False,"Timer")
            elif obj.name == "Finish_Door": Tile((726,532),obj.image,(self.Lv20OpenDoors,self.Lv20Doors),False,"Finish_Door")

    def L1_KeyCode(self, Screen):
        Screen.fill("goldenrod1")
        if self.LV1Success:
            Screen.fill("Green")
            self.Lv1Locks.sprites()[0].image = self.Lv1Locks.sprites()[1].image
        inputBoxes = [I1, I2, I3, I4]
        KeyButton = [N1,N2,N3,N4,N5,N6,N7,N8,N9,N0]
        pygame.draw.rect(Screen,"azure4",(258,250,300,400))
        pygame.draw.line(Screen,"Black",(258,332),(558,332),8)
        pygame.draw.rect(Screen, "Green",(258,250,300,78))
        pygame.draw.rect(Screen, "Red", self.BackSpace)
        pygame.draw.rect(Screen,"Green",self.Check)
        pygame.draw.rect(Screen, "Silver",self.Back)
        Screen.blit(self.BackSpace_Text,self.BackSpace_Text_rect)
        Screen.blit(self.Check_Text,self.Check_Text_rect)
        Screen.blit(self.Back_Text,self.Back_Text_rect)
        for Box in inputBoxes: Box.Draw()
        for Button in KeyButton:
            Button.Draw()
            if Button.Touched:
                inputBoxes[self.Index].Input = Button.Number
                Button.Touched = False
                if self.Index <= 2:
                    self.Index += 1
        self.Check_Delete_Click(inputBoxes)
        self.Check_Check_Click(inputBoxes)
        self.Check_Back_Click()

    def Check_Delete_Click(self, InputBoxes):
        mouse_pos = pygame.mouse.get_pos()
        if self.BackSpace.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    if InputBoxes[self.Index].Input == "-" and self.Index - 1 >= 0:
                        InputBoxes[self.Index - 1].Input = "-"
                    else: InputBoxes[self.Index].Input = "-"
                    if self.Index != 0: self.Index -= 1
                    self.pressed = False
    
    def Check_Check_Click(self, InputBoxes):
        mouse_pos = pygame.mouse.get_pos()
        if self.Check.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    Guess = ""
                    for Box in InputBoxes:
                        Guess += str(Box.Input)
                    if Guess == self.Lv1Password:self.LV1Success = True
                    else: pygame.display.get_surface().fill("Red")
                    self.pressed = False

    def Check_Back_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.Back.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    self.Exit = True

    def LV1Cave_Paper(self):
        if self.Paper:
            pygame.display.get_surface().fill("White")
            pygame.display.get_surface().blit(self.Lv1Password_Text,self.Lv1Password_Text_rect)
            pygame.draw.rect(pygame.display.get_surface(),"Gray",self.Frame,3)
            pygame.display.get_surface().blit(self.RewindSymbol,self.RewindSymbol_rect)

    def Draw_Level(self,Map:pygame.sprite.Group,Slowdown = 1):
        self.BackGround.draw(pygame.display.get_surface())
        Map.draw(pygame.display.get_surface())
        if Map == self.Level_1:
            self.Lv1Doors.draw(pygame.display.get_surface())
            self.Lv1Locks.draw(pygame.display.get_surface())
        elif Map == self.LV1_Cave:
            self.LV1CaveOpenDoors.draw(pygame.display.get_surface())
            pygame.display.get_surface().blit(self.Lv1PasswordPaper,self.Lv1PasswordPaper_rect)
        elif Map == self.Level_2:
            self.Lv2Doors.draw(pygame.display.get_surface())
            self.Lv2Locks.draw(pygame.display.get_surface())
            self.Lv2OpenDoors.draw(pygame.display.get_surface())
        elif Map == self.LV2_WC:
            self.LV2_WC_Doors.draw(pygame.display.get_surface())
            self.LV2_DeadlyBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_3:
            self.Lv3Doors.draw(pygame.display.get_surface())
            self.Lv3Locks.draw(pygame.display.get_surface())
            self.LV3_DeadlyBlocks.draw(pygame.display.get_surface())
            pygame.draw.rect(pygame.display.get_surface(),"White",self.DoorTextBox)
            pygame.draw.rect(pygame.display.get_surface(),"fuchsia",(400,200,100,100),5)
            self.DoorText = Game_font.render("Jump", True, "Blue")
            pygame.display.get_surface().blit(self.DoorText,self.DoorText_rect)
        elif Map == self.Level_4:
            self.Lv4Doors.draw(pygame.display.get_surface())
            self.Lv4Locks.draw(pygame.display.get_surface())
            self.LV4MovingBlocks.draw(pygame.display.get_surface())
            self.LV4DeadlyBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_5:
            self.Lv5Doors.draw(pygame.display.get_surface())
            self.Lv5Locks.draw(pygame.display.get_surface())
            self.LV5DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV5WrongBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_6:
            self.Lv6Doors.draw(pygame.display.get_surface())
            self.Lv6Locks.draw(pygame.display.get_surface())
            self.LV6DeadlyBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_7:
            self.Lv7Doors.draw(pygame.display.get_surface())
            self.Lv7Shooters.draw(pygame.display.get_surface())
            self.LV7DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV7Locks.draw(pygame.display.get_surface())
            self.Lv7Shooters_Bottom.draw(pygame.display.get_surface())
        elif Map == self.Level_8:
            self.Lv8Doors.draw(pygame.display.get_surface())
            self.LV8Locks.draw(pygame.display.get_surface())
        elif Map == self.Level_9:
            self.LV9DeadlyBlocks.draw(pygame.display.get_surface())
            self.Lv9Doors.draw(pygame.display.get_surface())
            self.Lv9FakeBlocks.draw(pygame.display.get_surface())
            self.LV9Locks.draw(pygame.display.get_surface())
        elif Map == self.Level_10:
            self.LV10DeadlyBlocks.draw(pygame.display.get_surface())
            self.Lv10Doors.draw(pygame.display.get_surface())
            self.LV10Locks.draw(pygame.display.get_surface())
            if self.LV10SawDisplay:self.LV10Saws1.draw(pygame.display.get_surface())
            else: self.LV10Saws2.draw(pygame.display.get_surface())
            if not self.TPunlocked:
                pygame.display.get_surface().blit(self.TimeStop,self.TimeStop_rect)
        elif Map == self.Level_11:
            self.LV11Locks.draw(pygame.display.get_surface())
            self.Lv11Doors.draw(pygame.display.get_surface())
            self.LV11DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV11Saw.draw(pygame.display.get_surface())
        elif Map == self.Level_12:
            self.Lv12Locks.draw(pygame.display.get_surface())
            self.Lv12Doors.draw(pygame.display.get_surface())
            self.LV12DeadlyBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_13:
            self.LV13Locks.draw(pygame.display.get_surface())
            self.Lv13Doors.draw(pygame.display.get_surface())
            self.LV13DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV13Boxes.update(Slowdown)
        elif Map == self.Level_14:
            self.LV14Locks.draw(pygame.display.get_surface())
            self.Lv14Doors.draw(pygame.display.get_surface())
            self.LV14DeadlyBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_15:
            self.Lv15Locks.draw(pygame.display.get_surface())
            self.Lv15Doors.draw(pygame.display.get_surface())
        elif Map == self.Level_15W:
            self.LV15WDeadlyBlocks.draw(pygame.display.get_surface())
            self.Lv15WClosedDoors.draw(pygame.display.get_surface())
        elif Map == self.Level_15R:
            self.LV15RDeadlyBlocks.draw(pygame.display.get_surface())
            self.Lv15ROpenDoors.draw(pygame.display.get_surface())
        elif Map == self.Level_16:
            self.Lv16Doors.draw(pygame.display.get_surface())
            self.Lv16Locks.draw(pygame.display.get_surface())
            self.LV16DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV16WrongBlocks.draw(pygame.display.get_surface())
            self.LV16Boxes.update(Slowdown)
        elif Map == self.Level_17:
            self.LV17Locks.draw(pygame.display.get_surface())
            self.Lv17Doors.draw(pygame.display.get_surface())
            self.Lv17Shooters.draw(pygame.display.get_surface())
            self.LV17DeadlyBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_18:
            self.LV18Locks.draw(pygame.display.get_surface())
            self.Lv18Doors.draw(pygame.display.get_surface())
            self.LV18DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV18Saws.draw(pygame.display.get_surface())
        elif Map == self.Level_19:
            self.LV19Locks.draw(pygame.display.get_surface())
            self.Lv19Doors.draw(pygame.display.get_surface())
            self.LV19DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV19MovingBlocks.draw(pygame.display.get_surface())
            self.Lv19Shooters.draw(pygame.display.get_surface())
            self.Lv19FakeBlocks.draw(pygame.display.get_surface())
        elif Map == self.Level_20:
            self.LV20DeadlyBlocks.draw(pygame.display.get_surface())
            self.LV20Locks.draw(pygame.display.get_surface())
            self.Lv20Doors.draw(pygame.display.get_surface())
            self.Lv20FakeBlocks.draw(pygame.display.get_surface())